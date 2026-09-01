# What gets silently skipped

*A sales query's journey from BW to Business Data Cloud, stop by stop — and what to validate at each one before a director discovers it in a meeting.*

**Brújula · Issue 09 · W36**
*Data Architecture · SAP*

---

The last issue ended at the decision: what you sign when you move to Business Data Cloud,
where your data is allowed to come from, and what it actually costs. This one starts where
that one stopped. Assume the decision has been made. **What happens to your report?**

Three-box diagrams —*lift*, *shift*, *innovate*— don't answer that. So let's take something
concrete and thoroughly ordinary: a **sales query** built on a **CompositeProvider** —the BW
object that joins several sources into a single view for reporting—, with a commercial
hierarchy, a couple of *restricted key figures* —prior year, same period—, a variance
formula, period and company code variables, and authorizations by sales organization. It is
consumed two ways: a story in SAC for commercial management, and Analysis for Office in
Excel for the controllers who reconcile.

That object, or one nearly identical to it, exists in practically every manufacturing and
consumer-goods BW in the country. Let's walk it stop by stop.

## Stop 1 — The lift: nothing happens, and that's the point

The system moves *as-is*. The query is still the same query, SAC's live connection still
points at the same system, Analysis for Office still works. Nothing breaks because nothing
changed: the datacenter changed, and the contract.

**What to validate:** that your release qualifies —BW/4HANA 2021 SP4 or higher, or 2023 SP0
or higher—. That the cleanup happened **first**: a lift carries everything, including what
you didn't want to carry, and a BW with fifteen years of dead objects lifted as-is is the
same BW, now rented by capacity unit. And something that rarely shows up in the proposal:
**extraction from your ERP now crosses the network.** If your source stays on-premise, the
daily load windows that run inside your datacenter today start traveling to SAP's cloud. You
have to size the link and re-measure the timings with real volume, not with a sample.

## Stop 2 — The query becomes an analytic model

Here's the news. In SAP's Architecture Center, the **Query Template Generator** —the tool
that turns BW queries into Datasphere analytic models— was marked *(planned)*. On **July 30,
2026**, SAP published the course that documents it, with transaction, authorizations and
configuration steps. The two official pages contradict each other; the more recent one wins.

It works in two steps. You create a **query template** from the existing query —in BW
Modeling Tools 1.27 PL3, or in SAP GUI with `RSDWCTG_ADMIN`— and pick the Datasphere **HANA
space** where the objects will be born. Then you generate: the system reads the query's full
definition, **formulas and variables included**, and creates **dimensions** for every
InfoObject with texts or hierarchies —reusing compatible ones that already exist—, a **fact
view** on the CompositeProvider limited to the fields the query references, and an **analytic
model** that mirrors the query's structure.

Two details matter: it reads from **BW private cloud edition inside BDC**, meaning it
requires stop 1 to have happened; and it does not use the object store but a HANA space, a
different path from the Data Product Generator's — the two tools' targets can't even see
each other.

If you don't want to move the system yet, the equivalent on-premise path has existed for
years: you release the query with `RSDWC_QUERY` and import it from Datasphere's Semantic
Onboarding with **BW/4HANA Model Transfer**. A case documented by SAP shows what it
produces: a single query generated **63 objects** across dimensions, texts, hierarchies,
fact view and analytic model.

### And here is the document that decides your project

SAP note **2932647** —version 18, December 18, 2025— lists, for Model Transfer from
BW/4HANA and from BW bridge, which query features are supported and which are not. The
general rule is written like this:

> *"If not indicated otherwise, unsupported features do not prevent the BW analytic query
> from being transferrable from SAP BW/4HANA to SAP Datasphere, but are simply skipped and
> removed from the transferred object during the process."*

There are two ways to lose, and only one of them warns you.

**The one that warns you.** Four situations in which the model **is not transferred**: if the
query isn't built on a **CompositeProvider (HCPR)** —in BW/4HANA scenarios it is the only
admissible InfoProvider—, or if that CompositeProvider carries a **temporal join**, an
**ambiguous join**, or **input parameters from HANA views**. Annoying, but honest: you find
out on day one.

**The one that doesn't.** Everything else transfers, and the unsupported feature disappears
from the object. The list is not exotic in the slightest. You lose:

- **Any formula beyond `+ - * /`.** The note enumerates what doesn't travel, and there,
  almost in its entirety, is BW's formula language: `IF`, `AND`, `OR`, the comparators, `%`,
  `%A`, `%GT`, `%CT`, `SUMCT`, `SUMGT`, `NODIM`, `NOERR`, `NDIV`, `COUNT`, `DELTA`, `LEAF`,
  `FRAC` and every mathematical function.
- **Two-structure queries** — the classic design of a commercial report.
- **The default filter**: only the global filter survives.
- **Exit variables, replacement path variables and authorization variables.**
- **Unit conversion**, **non-cumulative key figures**, **stock coverage key figures**,
  **business volume elimination** and **display attributes**.

Go back to the example at the top. That query had a variance formula —and a variance
protected against division by zero is written with `NOERR` or `NDIV`—, period variables that
in practice are almost always exit variables, and authorizations resting on authorization
variables. Three of its pieces are on the list. **I didn't invent a hard case: I invented
the typical one.**

And two behaviors that reorder the entire roadmap. First: *"By design, any transferred model
is disconnected from any changes applied in SAP BW/4HANA after the model was transferred."*
The transfer **is not a live bridge: it is a snapshot of the metadata.** Every change to the
original query forces you to run the process again. Second: **hierarchies are flattened and
materialized** down to their leaf values, and updates in BW **are not reflected** in models
already transferred. Your commercial hierarchy is frozen on the day you transferred it; a
territory reorganization does not arrive on its own.

**What to validate, and this is the most important line in this paper:** not that the object
exists. That **the number matches**, cell by cell, against the original query, with the same
variables and on the same day. A model with half a formula removed looks perfectly healthy.

And there is a question that has no public answer today. Note 2932647 covers **Model
Transfer** and **BW bridge**. For the **Query Template Generator** no equivalent published
list exists. It may be better, because SAP says it reads the full definition *"including
formulas and variables"*. It may inherit the same limits, because the destination is the same
analytic model and several of the losses belong to the target model, not to the transport.
Nobody should sign a roadmap covering thousands of queries without that list. **Ask for it by
name.**

And a warning the note gives about itself: it is "on-going development, released in multiple
waves", it is on version 18, and it is updated frequently. Today's list will not be your
project's list.

## Stop 3 — Where the number lives now

The engine changed. With Model Transfer, BW remains a remote source and **the calculation is
done by Datasphere's HANA engines**. With the Query Template Generator, the objects live in
a Datasphere HANA space. In both cases, the execution plan you spent years tuning
—aggregates, partitions, OLAP cache— is no longer the one running.

**What to validate:** response times at production volume and with the full hierarchy
expanded. Currency conversion against the same exchange rate type and the same reference
date. Fiscal year variant. Texts in the languages you actually use. And if you carry
inventory, remember that non-cumulative key figures don't even arrive: they have to be
rebuilt, and they are the classic place where the annual total stops being the sum of the
months.

## Stop 4 — Where the report is consumed

The SAC story is the easy part: you create a **live SAC connection to Datasphere** and there
you can build anew or **substitute the BW source in existing stories and models**. It's work,
not drama.

**The problem is the controllers.** Per KBA **3297935** and the Analysis for Office
connection matrix, the tool reaches Datasphere **views and perspectives**, but **not analytic
models** —precisely the object both stop-2 tools produce—. The supported path to get an
analytic model into Excel is the **SAP Analytics Cloud add-in for Microsoft Excel**: a
different product, which does consume Datasphere models, BW queries and S/4HANA queries, does
live planning, and **requires an SAC BI or planning license** — that is, capacity units per
user per month.

That is where the technical roadmap collides with the cost strategy. If your analytics
licensing savings came from moving consumption toward Analysis for Office —a common and
correct move— migrating the query pushes those people back into the SAC family. Nobody is
going to put both facts on the same slide for you.

**And Power BI?** There are three paths and they are not equivalent:

- **OData** —a query protocol over HTTP, with a native connector in Power BI— is the only
  one of the three that reaches **analytic models** and not just views, and the only one that
  respects the two things that make that model valuable. Its **aggregation**: the model does
  not merely sum, it also defines exceptions —inventory taken as the last value of the
  period, headcount counted without accumulating— and over OData the Datasphere engine
  applies that rule before handing you the number. And its **associations**: the joins already
  defined toward the dimensions, which bring the text and the hierarchy attached to the key.
  The price is authentication: **three-legged OAuth** —user, client application and
  authorization server—, where the person authorizes Power BI to read on their behalf. Good
  for security, because the token carries their identity and Data Access Controls apply per
  person; awkward for operations, because tokens expire and scheduled refresh depends on
  someone re-authenticating.
- **ODBC/JDBC** via the Open SQL schema is simpler, but SQL returns two-dimensional results:
  against an analytic model **you lose associations and hierarchies, and the data arrives
  un-aggregated**, so Power BI sums it again with the wrong rule —annual inventory comes out
  as the sum of twelve months instead of the December balance—. For the OLAP world you're
  bringing from BW, it puts you back at the start.
- **Premium Outbound Integration** is the bulk exit with an explicit price: 20 GB blocks on a
  tiered rate. The detail that sinks budgets is that you're charged for the volume that
  leaves, not the size of the table; public measurements on BSEG-type tables produced a
  **factor close to 30** against the original size.

And on top of that sits the contractual boundary, which has two doors with two different
rules. It's worth not confusing them, because people quote whichever one suits them.

**Taking data out of Datasphere** toward a third-party tool is governed by that capability's
terms: SAP's APIs may not be used to extract into third-party applications, with the phrase
*"Use of OData APIs for data extraction is prohibited"* and a cap of 2,000 OData calls per GB
of compute memory per tenant per month.

**Taking data out of the BW** now running in SAP's cloud is governed by section 6 of the
current Supplement, the one covering *BW Capacity Services*, and the wording there is harder.
§6.2.5 —inside the clause governing the HANA runtime edition your system sits on— says
*"Customer is expressly prohibited from performing the mass extraction of any data"*, except
through licensed SAP tools and **only toward six enumerated destinations**: HANA enterprise
edition, HANA standard edition, SAP Cloud Platform's HANA service, HANA Cloud, HANA EE Cloud
and the Datasphere capacity services. All six are SAP. A third-party lakehouse is not on the
list.

The practical line, at both doors, sits between **consuming** —reporting live, within the
caps— and **extracting**. The caps are, in fact, the governor: they let you report, not drain.

If your corporate reporting destination is Power BI, the path SAP and Microsoft are building
is called **BDC Connect for Microsoft Fabric**: bidirectional zero-copy sharing into OneLake.
Its general availability is planned for the **third quarter of 2026** —the one now running,
which closes in September—, so as of this writing it remains a promise with a calendar, not
something you can test. Ask for it by name, and ask for the date in writing.

## Stop 5 — Authorizations don't travel on their own

Your query filters by sales organization through analysis authorizations, and we already saw
that **authorization variables do not survive the transfer**. Datasphere has no analysis
authorizations either: it has **Data Access Controls**. There is a bridge: transaction
`RSDWC_DAC_RSEC_GEN` exports your authorizations into table `RSDWC_RSEC_DAC`, which is
imported into Datasphere and generates a filter clause where the BW user is replaced by the
Datasphere user —by email, with a BAdI if your logic differs—, plus a permissions view and
the DAC.

**What to validate:** the **wildcards**. BW uses them liberally and Data Access Controls do
not support them; every pattern-based authorization has to be resolved into values. The
granularity: within a single space you cannot restrict an analytic model to a group of users,
so separation happens **by space**, and that reorders your design. And the test nobody runs:
log in as a regional manager and confirm they see exactly what they used to see, not one row
more.

## Stop 6 — And BPC?

Good news first: **BPC moves with BW**, in the same motion. SAP says so explicitly —*"along
with moving your SAP BW 7.50 or SAP BW/4HANA to a private cloud environment (PCE) in Business
Data Cloud, you can also move your SAP BPC 10.1 NW or SAP BPC 2021 at the same time"*—. That
is precisely what usually derails these projects, and here it doesn't. And a hybrid
architecture already works: an SAC planning application resting on **BPC Live Connection**
against BW in the private cloud; the user hits save in SAC and the data becomes available in
Datasphere, without duplication.

The uncomfortable part comes next. SAP's strategic direction is not BPC: it is **SAC for
planning** and **Group Reporting for statutory consolidation**. And from BPC to SAC there is
no migration, there is **reimplementation** —models, script logic and reports get rebuilt—.
Which leaves planning split across two programs: consolidation travels with the S/4 project,
planning with the analytics one, and **the BPC license is still required for as long as BPC
exists**. During the transition you pay twice.

**What to validate:** if you keep developing in BPC, use **modern aDSO structures compatible
with the Data Product Generator** —it's free to do it right now and expensive to discover
later—. And something contractual almost nobody reviews, which carries weight here.

The Supplement separates two categories with their own definitions. An **Add-on** adds new,
independent functionality *without modifying* existing SAP functionality (§1.1). A
**Modification** is a change to delivered source code or metadata, or any development that
customizes or alters existing functionality (§1.9). Script logic, BAdIs, exits and a good
share of the Z developments surrounding BPC fall on the Modification side.

The distinction is not academic. §6.7.2 enumerates the services in which the customer has the
right to develop and use Modifications, and they are the four SAP S/4HANA Cloud private
edition variants; *BW Capacity Services* are not on that list. For BW, what §6.7.1 grants is
the right to develop and use **Customer ABAP Add-ons**. It may be loose drafting —the
document uses the term *BW Capacity Services* elastically— or it may be exactly what it says.
The question has to be asked in writing before signing: **are my current developments around
BPC still admissible inside BW running in SAP's cloud, and under which category?**

What is written without ambiguity are the consequences. The SLA and the Support Schedule **do
not apply** to Customer ABAP Add-ons, and you are responsible for their installation, support,
compatibility and vulnerabilities (§6.7.2). The simplification and incompatibility checks at
every upgrade **are executed by you** (§6.10.2). And the intellectual property of every
Modification sits with SAP (§6.7.4).

## Stop 7 — And only then, the data for AI

Only here does the **Data Product Generator** come in, which is a different tool for a
different purpose: it publishes InfoProviders —InfoObjects, aDSOs, CompositeProviders,
MultiProviders, InfoCubes and queries used as InfoProviders— into read-only tables in the
object store, with a consolidation task that maintains consistency against the source and
deltas for CompositeProviders and MultiProviders. From there, via delta share, comes the data
for Databricks — with all the contractual restrictions we reviewed last issue.

And one we didn't review, because it lives in the development clauses: §6.7.2 reserves SAP's
right to restrict or require the removal of any Add-on or Modification that *"enable the
extraction of Data Products to non-SAP applications through any means not authorized via
SAP"*. The code you write inside that BW is also subject to the data boundary.

## What the person who signs takes away

Three numbers, and none of them is the server's:

1. **How many of your queries use features that will be silently skipped.** Not how many you
   have: how many are on the list. That is the project.
2. **How many of your Excel users touch objects that will end up as analytic models**, and
   what that population costs in capacity units.
3. **How often your queries and hierarchies change.** Because every change forces another
   transfer, and that recurring work appears in no proposal.

And one demand: **the list of unsupported features for the Query Template Generator**, which
today is not published. Without it, the stop-2 roadmap is a blank box.

None of this says don't move. It says the number that reaches the dashboard after the move
has to be the same one that reached it before — and that proving it is work, not an
assumption.
