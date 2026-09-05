# How to validate an extractor migration to S/4HANA

## What the build phase revealed in an ECC → S/4HANA migration: failures that produce no error, and scope that was in no specification

A few editions ago I closed a papper on extractor migration with a practice that felt obvious to
me: *an extractor isn't finished when it runs, it's finished when the data reconciles against the
source*. Easy to write.

These past weeks I had to live up to it. We're in build and data validation in development,
migrating the classic extractors of an ECC system into CDS views in S/4HANA, and the first load I
put up for reconciliation came out green. No errors, no rejected records, no warnings. And with
fewer rows than the source had.

It wasn't an isolated case. It turned out to be the characteristic failure mode of this
architecture, and it forced me to revisit something more uncomfortable than a mapping: **the
criterion by which we call a load good**. This edition is what we found, and why I think it changes
what belongs in a work plan — and, if you sign the budget, in a contract.

## A declarative model fails differently

In ECC, an extractor was essentially a program. Code that knew which tables to read, in what order
and with what logic. When a program gets it wrong, you usually notice: it aborts, it leaves a log,
someone sees it in red.

In S/4HANA, the extractor is a CDS view with annotations. Annotations are declarations — they start
with `@` — and they are not documentation: they are instructions. They tell the provisioning
framework — ODP, the layer that exposes SAP data to the analytical world — what kind of data you're
publishing, and the target system builds its half out of that declaration.

For a view to be extractable you need two declarations, not one. The first is the switch:
`@Analytics.dataExtraction.enabled`. Without it the view exists, it can be queried and reported on
perfectly well, but it is invisible to extraction. The second is the family of the data, and here
comes the first oddity: **the four families do not live in the same annotation.** Master data and
transactional data are declared with `@Analytics.dataCategory`; texts and hierarchies, with
`@ObjectModel.dataCategory`. Searching for "the category annotation" hands you half the map and no
sign that the other half is missing.

That the target container is derived from this is not a metaphor. The object that gets published
carries the technical name of the view plus a suffix that comes out of that declaration: `$P` for
master data attributes, `$T` for texts, `$H` for hierarchies, `$F` for transactional data. The type
of whatever is born on the other side is literally in the name, and it isn't chosen afterwards.

And all of that is when the key is a single field. Cost centre attributes, which is the object we
were working on, don't have a key: they have three — controlling area, cost centre and validity
date — and a compound key multiplies what you have to declare. The rule is that **exactly one field
of the key is the representative one**, the one that "is" the entity, and it's marked with
`@ObjectModel.representativeKey`. In SAP's own example: a city dimension keyed on country + city
has the city as its representative field, not the country. For cost centre, the representative is
the cost centre; the controlling area is the prefix that makes it unique.

That annotation looks like analytical modelling and it isn't: without it the framework won't
publish the view — it complains that it can't find a representative field — and there is no
extraction. It also points at the field's **alias**, not its source name: if you renamed it in the
projection, the annotation has to point at the new name or it won't resolve. From there come three
more obligations, and none of them is cosmetic:

- **Every other key field needs an association** to its own master data view. The controlling area
  can't travel loose.
- **The validity date is the exception, and it brings two rules.** The "valid to" field has to be
  part of the key and carry the end-date semantics; the "valid from" goes outside the key. And the
  "valid to" field **cannot** have an association, nor appear in the condition of any other one.
- **The text is associated to the representative field**, not to the whole key — even though the
  association's condition does have to include every key field, and the text view has to have
  exactly the same key.

The target inherits that shape: a compound key in the source becomes a compounded object on the
other side — the cost centre hanging off the controlling area — and which hangs off which is
decided by the field you declared representative. If that derivation can't be resolved, at least it
speaks up: when another view tries to associate, activation fails with `RSODP056`, *cannot derive
InfoObject name*. It is one of the very few times in this whole phase that the system stopped us.

Seen from a distance, all of this sounds like a simplification. Less code, less surface for error.
But the risk didn't disappear: **it moved from the logic to the metadata**. And a metadata error
almost never produces an abort. It produces an extraction that runs, that delivers a dataset with
the right shape, and that is incomplete.

It's a difference of nature, not of degree. A badly written program fails loudly. A badly placed
declaration hands you less, in green.

## The field nobody was watching

The case that teaches it best is also the silliest, which is exactly what makes it dangerous.

Back to that cost centre attributes extractor. Among some seventy-odd fields, the view carried the
language field. One more attribute, of no analytical relevance; nobody reports on it. Nobody was
watching it.

The target system assigns the *language field* flag to any column whose data type is `LANG`. By the
type, not by what you declare — we established that by elimination: switching off the semantic
annotation changed nothing, and reading the field from the table instead of the standard view
didn't either. And with that flag, the load process assumes the data is multilingual and **adds a
filter of its own**: it requests only the languages installed in the target system and discards
everything else. No error, no warning, no line in the log.

It's worth noticing where the criterion ended up living. How many rows arrive is not decided by the
extractor, nor the view, nor the functional specification: it's decided by a list of languages
configured in **another system**, which nobody on the source side has any reason to open.

SAP documents it in KBA 3219389. We almost didn't find it: the title talks about a *text
datasource*, so you dismiss it when your problem is in an attributes view. The real cause has
nothing to do with texts — it's the type of the field — but the title sends you somewhere else.

And then came the part that is genuinely an architecture decision. **SAP documents the fix only on
the target side**: change that field flag by hand. It works. The problem is that this metadata is
regenerated every time the source is replicated, so the correction erases itself. It's a perpetual
manual step, one that survives only as long as the person who knows about it stays on the project,
and that someone will forget in production on exactly the day it matters.

We preferred to solve it at the source. The line that worked breaks the type with a string function
and pins it back down as a plain character, and it also renames the field: if the type is already
corrected but the name is still the standard one, the target detects it again by name. They are two
different mechanisms and you have to disable both.

The mapping of the renamed field lives in the transformation, which is an object of its own, gets
transported, and survives replication.

That's what changed: we didn't eliminate the manual work, we **moved it from a place that gets
erased to one that persists**. The price is that the technical name no longer matches the original
extractor's, and it has to be written down in the mapping matrix. That strikes me as a cheap trade.

## The permission that returns less data

The second finding has a different shape and the same ending.

SAP's standard views carry access controls of their own, written in a separate language — DCL, the
dialect in which authorisations over a view are declared — and embedded in the model. When the view
activates them, the system doesn't reject the query: it **trims the result** down to what that user
is entitled to see. The standard authorisation profiles for extraction don't cover them: they
enable the mechanism, not the content.

If the technical user on the connection is missing the **business** authorisations — a controlling
area, a chart of accounts — the extraction doesn't fall over. It returns fewer rows. Or zero.

Think about what that means in an integration test. The technical team runs the load, it comes out
green, the activity is marked closed. The functional user opens the report weeks later and sees a
smaller figure. Nobody has any reason to suspect the permission, because the permission never said
no.

## What the two failures have in common

A language field nobody reports on, and a business authorisation. They look nothing alike, except
in the only thing that matters: **neither of them produced an error**. Both delivered a plausible
result.

That's where this edition's thesis comes from, and it's uncomfortable because it questions a habit
we had running just fine: **"the load ran without errors" has stopped being evidence of anything.**
It was a reasonable signal when the extractor was a program. In a declarative model, it is barely
confirmation that the mechanism executed.

The evidence now is quantitative. Row counts against the source, full load, no filters and no
*delta* — no incremental loading, bring everything — before comparing a single value. SAP has its
own data transition validation tool precisely because reconciliation against the source is the
test, not an optional assurance step.

Even the tool you test with changed, and in a way worth telling. The classic extractor checker —
`RSA3`, the first reflex of anyone coming from ECC — doesn't work with CDS views. You have to use
another report, `RODPS_REPL_TEST`, and that report brings a trap of its own: it doesn't simulate.
Initialising or running a delta from there opens a real subscription in the operational delta queue,
which someone then has to go and clean up. The diagnostic tool modifies the state you're
diagnosing, and it doesn't announce that either.

There's a sequencing corollary we learned the hard way, and it's worth more than a lot of
methodologies: **delta goes last.** Turning on incremental loading before the full load
reconciles introduces time-window differences that get confused with mapping errors, and you lose
days chasing a defect that doesn't exist. First you prove the data is correct; then you optimise
how it arrives.

## The scope that was in no specification

And here comes the second kind of surprise from the build phase, which is no longer about quality
but about scope.

The hierarchies — cost centres, chart of accounts — turned out to be the most expensive object and
the worst estimated. Three reasons.

The first is that a hierarchy is not a flat table: declaring it as a hierarchy makes the object be
born **with segments**. Five, in our case — header, header texts, nodes, node texts and intervals —
and that format is derived from the annotation. Declaring the wrong family doesn't produce an
error: it produces the wrong container, which you then have to delete and rebuild. It doesn't even
all come from the same view: the node texts are not delivered by the hierarchy view but by a
different one, so a single cost centre hierarchy already needs three views on the source side.

The second is that there are two hierarchy syntaxes in CDS and the one that shows up first in any
search is the wrong one. The new one — an entity of its own, declared with `DEFINE HIERARCHY` —
serves analytical consumption and **not** extraction; the extraction path is still the
`@ObjectModel.dataCategory: #HIERARCHY` annotation. We verified it the hard way: the 244 pages of
SAP's official guide on ABAP data models do not mention extraction into the analytical world even
once — neither the annotation that enables it, nor the framework. It's correct information applied
to the wrong scenario, which is the hardest class of error to catch because everything you read is
true.

The third is the one that changes the plan, and it follows directly from the first. Because the
node texts arrive separately, migrating those hierarchies the way SAP recommends means **you have
to modify objects in the target system**: adding two characteristics to the cost centre that don't
exist today — one for the hierarchy identifier and one for the node text, compounded to the former
— with fixed lengths and mapped segment by segment. That isn't configuration: it's modelling. We
checked it against the system: in two of the three hierarchies in scope, that configuration is
literally empty.

None of the functional specifications mentioned it. And not out of carelessness: **they are written
from the source side**. They describe with precision what data has to come out of S/4HANA, because
that's where the novelty is and where the analysis concentrated. The target is taken for granted,
because "it already exists and it already works".

That assumption is the one to break. In a migration like this, the system you are *not* migrating
also has work to do, and that work doesn't appear in any document until someone tries to load the
first tree.

## What I would ask of a work plan

Four concrete things, and the last two are for whoever signs the scope and the budget, not for
whoever runs the team:

- **That the definition of "done" is a number, not a colour.** A count against the source, full
  load, no delta. If the activity can be closed with a green screenshot, the criterion is badly
  written.
- **That delta is planned as a later phase**, not as part of the build. It's a sequencing decision
  that saves weeks of false diagnosis.
- **That the scope explicitly covers the target system.** If your specifications only describe the
  source, you have half a scope and a contingency calculated on half the work. It's worth asking,
  before signing: *what has to be modified on the other side?*
- **That the authorisation test is a business test, not a technical one.** That the connection user
  can connect proves nothing about what data it can actually see. This gets requested in writing
  and measured with a count.

I say this from a region where none of it is hypothetical. A good share of the operations of the
multinationals installed in the northeast runs on SAP platforms that are, or are about to be, in
this same transition. The conversation about how a migration gets tested is not an implementation
detail: it's the difference between finding a shortfall in development and finding it in a close.

## True north

Edition 02 of this newsletter argued that design *is* the migration. I still hold to that. But the
build phase taught me something design alone can't solve: **even with the right specification, the
way of proving the data arrived complete had to change.**

Migrating to a declarative model didn't remove the risk: it left it without symptoms. And a risk
without symptoms is the argument for making validation stricter, not lighter. Less code doesn't
mean fewer tests. It means different tests: less reviewing logic and more counting rows.

If you're about to enter this phase, the cheapest change you can make today doesn't cost a single
line of code. It's rewriting the acceptance criterion of your load activities so that it demands a
number. Everything else in this edition we discovered because that number didn't add up.

---

### Sources

- SAP Learning — *Working with ODP Context: CDS view based extraction* (extractability conditions: `@Analytics.dataCategory` **or** `@ObjectModel.dataCategory` **and** `@Analytics.dataExtraction.enabled`; the `$P`/`$T`/`$H`/`$F` ODP suffixes): https://learning.sap.com/courses/upgrading-your-sap-bw-skills-to-sap-bw-4hana/working-with-odp-context-cds-view-based-extraction_f01df9a0-0e79-4d76-be38-d2cfac4dde42
- SAP Learning — *Working with Hierarchy Views* (the five views of a hierarchy: source, hierarchy, directory, directory texts and nodes; the hierarchy view admits no associations; recursive parent association, directory association and dimension associations by node type): https://learning.sap.com/courses/developing-analytical-models-with-cds-based-analytical-projection-views/working-with-hierarchy-views
- SAP Learning — *Working with Dimension and Text Views* (compound keys: a single `@ObjectModel.representativeKey`; every other key field requires an association; rules for `@Semantics.businessDate.to`/`.from`): https://learning.sap.com/courses/developing-analytical-models-with-cds-based-analytical-projection-views/working-with-dimension-and-text-views
- SAP Help — *Analytics Annotations* (`dataExtraction.enabled`, `dataCategory`, delta): https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/c2/dd92fb83784c4a87e16e66abeeacbd/content.htm
- SAP Help — *ObjectModel Annotations* (`dataCategory` for texts and hierarchies, `representativeKey`, `foreignKey.association`, `hierarchy.association`): https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/89/6496ecfe4f4f8b857c6d93d4489841/content.htm
- SAP KBA **3219389** — the load process automatically filters by the languages installed in the target system when the DataSource has a field flagged as *Language Field*; also valid for DataSources based on S/4HANA CDS views: https://userapps.support.sap.com/sap/support/knowledge/en/3219389
- SAP KBA **2754750** — `RSODP056`, *cannot derive InfoObject name*, when the target view of an association has a compounded characteristic (more than one key field, one of them the `representativeKey`): https://userapps.support.sap.com/sap/support/knowledge/en/2754750
- SAP KBA **3062210** — user-dependent access restrictions on CDS views via DCL and `@AccessControl.authorizationCheck`: https://userapps.support.sap.com/sap/support/knowledge/en/3062210
- SAP Help — *ABAP Data Models* (SAP's official ABAP data models guide; its hierarchies chapter does not cover extraction): https://help.sap.com/docs/abap-cloud/abap-data-models/abap-data-models
- SAP — *ABAP CDS: DEFINE HIERARCHY* (the hierarchy syntax for analytical consumption, distinct from the extraction path): https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abencds_f1_define_hierarchy.htm
- SAP Community (S. Kranig, SAP) — *CDS based data extraction, Part III: Miscellaneous* (hierarchies: node texts come in a separate view and force two external characteristics in the target; `RSA3` doesn't apply, you use `RODPS_REPL_TEST` and it is not a simulation): https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/cds-based-data-extraction-part-iii-miscellaneous/ba-p/13452148
- SAP Community (RIG) — *An Introduction to the Data Transition Validation Tool* (source-to-target reconciliation as the test of success): https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/an-introduction-to-the-data-transition-validation-tool/ba-p/13541524
