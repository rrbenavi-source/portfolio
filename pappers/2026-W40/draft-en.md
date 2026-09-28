# It reconciled at go-live. What about today?

## Almost every data platform now lets you put a "certified" checkmark on a model. None of them makes you prove it still deserves it today. Projects reconcile the number on go-live day and then leave nothing behind to keep reconciling it. This edition is about that missing control, and about who should sign for it.

I didn't plan this edition. A question asked for it.

In edition 09, "What gets dropped in silence", I wrote about what gets lost when a BW query is moved to
Business Data Cloud: formulas, variables and authorizations that don't make the trip, with nobody
raising a flag. A reader who works on the cost-control side left a comment there that explained the
underlying problem better than I had:

> "A dashboard built on SAP HANA still looks healthy (it opens, it returns numbers) even if the query
> behind it lost a variance formula or an authorization variable along the way. The controller has no
> way to tell from the dashboard; the only way to catch it is to reconcile manually against the
> source, cell by cell, which in practice almost nobody does after the initial go-live."

Then she asked whether the edition covered periodic validation, not just the migration. It didn't.
This is the other half.

The more I dug, the clearer it became that this isn't an SAP problem. It doesn't matter whether the
data lives in BW/4HANA, Databricks or Snowflake, or whether you consume it in SAP Analytics Cloud, in
Power BI or by asking an assistant like Genie in plain language. The business question is the same,
and almost no project answers it: **how do I know the number I'm deciding with today is the right
one?**

## The dashboard that looks healthy

Here's an illustrative scenario. It isn't a client; it's the sum of what I've seen across several
go-lives.

A cost dashboard goes live in March. Before releasing it, the team reconciles it against the general
ledger, the accounting book where the official figure lives: company code by company code, month by
month, to the peso. The controller's office signs off, the project closes and everyone is happy. With
good reason: the number reconciled.

In May, a transport (the package that moves a change from development to production) fixes a query
filter and, without meaning to, changes the base of the year-over-year variance. In July the sales
regions are reorganized and the model's hierarchy keeps the old structure. In August a new company
code is created that doesn't fall inside the view's filter. In September an upgrade lands.

None of that breaks the dashboard. It opens fast and returns numbers that look reasonable. Nobody gets
an alert, because technically everything works. What broke was the meaning.

One day in October, in the budget meeting, someone on the committee brings a printout of the ledger
figure and it doesn't match the screen. From that moment nobody is discussing the budget anymore;
they're discussing which of the two numbers is right. The trust that took a whole project to build is
gone in ten minutes.

Numbers drifting isn't strange; systems change. What's strange is that the project reconciled once and
left nothing behind to keep reconciling. **It didn't leave a witness**: a control that compares the
number against its source again every time something changes, without anyone having to remember.

## A checkmark is not a reconciliation

Here comes the uncomfortable part for those of us who sell and build platforms. Almost all of them
already ship some kind of "certification" or quality mechanism. It's worth reading what each one
actually certifies.

**Power BI and Microsoft Fabric** have *endorsement*, a badge you put on the model: *Promoted* or
*Certified*. According to Microsoft's documentation, *Certified* means an authorized reviewer in the
organization attested that the item *"meets the organization's quality standards"*, and only people
designated by the administrator can grant it. In other words, it certifies that someone reviewed it at
some point. If the model changes tomorrow, the badge stays where it was.

**Databricks** has a system tag in Unity Catalog, its governance layer: `system.certification_status`.
The value `certified` indicates the asset *"has met internal standards for accuracy, completeness and
trust"* and puts a checkmark next to the table, dashboard or Genie space. It can be set by hand or by
automation rules that look at usage, owner or age of the asset. None of those rules checks whether the
number reconciles.

**Genie**, the Databricks assistant that answers business questions in natural language and writes its
own SQL, is the closest thing to a witness I found. It has *benchmarks*: up to 500 test questions, each
with the SQL that returns the correct answer, against which Genie grades what it generates as good,
bad or "manual review". Why that isn't enough on its own, I explain further down.

**Snowflake** ships *Data Metric Functions*, functions that measure something about a table (nulls,
duplicates, freshness) and that, paired with an *expectation*, return a pass or fail on their own
schedule, hourly by default. It's the closest thing to a continuous control and requires Enterprise
Edition. But it measures data quality, not whether the KPI reconciles against the books. That function
you write yourself.

**In SAP**, the Datasphere catalog lets you document a KPI with its formula in a glossary and publish
assets as trusted. Without a single definition there's nothing to reconcile, so it's necessary. But a
well-written definition doesn't prove today's number meets it. In the case from the comment, a model
that lost half a formula in the migration, the glossary is intact and the number no longer is.

[ FIGURE 1 — "A checkmark is not a reconciliation": five tools, the badge each one offers, what it
really certifies and what it doesn't do. ]

I don't say this as a criticism of vendors; the tools do what they promise. The gap is elsewhere. **A
badge says who thought the data was trustworthy. A reconciliation proves it is today.** And projects
deliver the badge, reconcile once to earn it, and leave.

## This is already solved, just in another industry

What surprised me most is that there's nothing to invent. Two worlds have been forced to solve this
for years, and they wrote it down.

**The first is audit.** The PCAOB is the body that oversees the auditors of companies listed in the
United States. Its evidence standard, AS 1105, says that when the auditor uses information produced
by the company itself (a system report, for example; in the trade it's called IPE, and the PCAOB calls
it IPC) they must *"test the accuracy and completeness of the information, or test the controls over
the accuracy and completeness of that information"*. Accuracy: every row says the right thing.
Completeness: no row is missing and the totals tie out.

When the PCAOB inspects an audit and finds a deficiency, it notifies the firm in a *comment form*. In
April 2024 it reported that in roughly 17% of the comment forms from its 2021 and 2022 cycles the issue
was exactly this: the auditor didn't sufficiently test the accuracy and completeness of company
reports and data, or the controls over them. Almost one in six, in a profession with a standard that
requires it. A BI project has none.

The same report describes what firms that do get it right have in place: a central repository of
reports, with the application each one comes from, how it's tested and with what conclusion.
Literally, an inventory of witnesses.

And this hits closer to home than it seems. Many companies in northeastern Mexico, especially in
manufacturing and shared service centers, report to a parent company listed in the United States. The
dashboard the controller opens here on Monday is often the same report that ends up in the monthly
close package up there. That's my own observation, not a statistic; I don't know of a figure for
Mexico and I'm not going to make one up.

**The second world is banking.** In 2013 the Basel Committee on Banking Supervision published BCBS 239,
its principles so that large banks could trust their own risk reports after the 2008 crisis. They're
written for banks, but it's the best text I know on this problem. I take three ideas from it:

1. **Reconcile against the books.** Principle 3 asks that data be *"reconciled with bank's sources,
   including accounting data where appropriate"*, and defines reconciliation as *"the process of
   comparing items or outcomes and explaining the differences"*. Comparing isn't enough.
2. **An inventory of rules and exception reports.** Principle 7 asks, at a minimum, for defined
   processes to reconcile reports, reasonableness checks with an inventory of the validation rules,
   and exception reports that identify and explain errors.
3. **Materiality as the yardstick.** Basel asks for accuracy to be measured with a criterion *"similar
   to accounting materiality"*: if the error could change the decision of whoever reads the report,
   it's material. Not everything has to reconcile to the cent; it has to reconcile within a tolerance
   that someone on the business side signed.

Neither source mentions Databricks, SAC or Genie. It doesn't need to: they describe a control, not a
tool.

## The witness

With that, the practice I'm proposing fits in six points. None of them is expensive. They get skipped
because none of them is in the project proposal.

**1. Control totals, defined by the business.** A control total is a known, independent total the
report is compared against: the ledger balance by company code and period, units invoiced in the
month, total payroll. For each critical KPI you write down what it reconciles against, at what level
and with what tolerance. IT doesn't set the tolerance; the owner of the number sets it and signs it.

**2. Reconciliation by event, not just by calendar.** Running the check every month is fine, but the
dashboard in the scenario didn't break on a date: it broke with a transport, a reorganization and an
upgrade. The witness has to run after every load, every change to the semantic model (the layer where
KPI definitions live), every transport and every upgrade. In edition 09 we saw it with BW's *model
transfer*: every re-transfer is a new migration.

**3. Witness cells and a canary user.** You don't need to reconcile cell by cell. Pick the few
intersections that break first: the year-over-year variance, a KPI with restricted filters, the total
by company code, and a closed period that should never move. Authorizations fail more quietly than
formulas, so for them there's a canary user per profile: a test user with the permissions of, say, a
regional manager, who runs the same report every cycle and compares what they see against what they
should see.

**4. An inventory of rules and reports.** A simple table: which report, which control total, which
rule, how often, last result. It's the repository the PCAOB calls good practice and the inventory
Basel asks for. And it's the first thing an auditor will ask you for.

**5. Exceptions with an explanation.** When the witness doesn't reconcile, the difference is logged,
assigned to someone and explained. An unexplained difference is a finding, however small.

**6. Reconciliation status, visible on the dashboard.** This point answers the reader's question
directly. If the controller has no way to tell from the dashboard whether the number reconciles, let
the dashboard tell them: "Reconciled against control totals on Sep 23: 4 of 4 OK". And if it didn't
reconcile yesterday, let it say that too. The checkmark is earned every day.

The witness doesn't need a new tool. You can get it running with what you already have: a query that
compares the model's KPI against the ledger total and writes the result to a control table.

```sql
-- Witness: net sales from the semantic model against the ledger, by company code and period.
-- Starts from the ledger, not the model: a company code missing from the model shows up as EXCEPTION.
INSERT INTO control.reconciliation (run_ts, kpi, company_code, period,
                                    model_value, source_value, difference, status)
SELECT CURRENT_TIMESTAMP,
       'NET_SALES',
       f.company_code,
       f.period,
       COALESCE(m.net_sales, 0),
       f.ledger_balance,
       COALESCE(m.net_sales, 0) - f.ledger_balance,
       CASE WHEN ABS(COALESCE(m.net_sales, 0) - f.ledger_balance)
                 <= t.tolerance_pct * ABS(f.ledger_balance)
            THEN 'OK' ELSE 'EXCEPTION' END
FROM (
       -- In the ledger (ACDOCA) revenue is posted as a negative, a credit:
       -- flip the sign to compare it against the KPI, which is positive.
       SELECT company_code, period, -1 * balance AS ledger_balance
       FROM   source.ledger_balances
       WHERE  account_group = 'NET_SALES'
     ) f
LEFT JOIN model.sales_by_company  m ON m.company_code = f.company_code
                                   AND m.period       = f.period
JOIN      control.tolerances      t ON t.kpi = 'NET_SALES';
```

[ FIGURE 2 — "The witness, in code": the annotated query (the control total, the tolerance the
business signs, the status that gets published) and below it how the result looks on the dashboard. ]

The query is the least of it. Notice three things, plus a sign detail: it starts from the ledger and
not the model, so the company code that fell outside the filter shows up as an exception instead of
vanishing; `control.tolerances` is a business decision stored as data; and the `status` column is the
one that ends up on the dashboard. The detail: in accounting, sales are credits and in ACDOCA they live
with a negative sign, so the witness flips the ledger sign before comparing. Without that, everything
comes out as an exception on day one and the witness loses credibility right away. In Snowflake this
can live as a custom *Data Metric Function*, scheduled to run whenever the table changes; in
Databricks, as a job after every load. If the report comes from an S/4HANA CDS view, the source for
the reconciliation is ACDOCA, the system's accounting line-item table.

## Who signs?

This is the other question the comment leaves open, and I suspect it's the one that will spark the
most debate.

My short answer: **IT is accountable for the witness existing and running. The business owns the
number meaning what it says.** Certification is signed by the data owner, not the platform
administrator, and internal audit reviews that the control works.

This isn't my invention. BCBS 239 asks banks to define data ownership and quality roles *"for both the
business and IT functions"*, and puts the business owner in charge of keeping data aligned with its
definitions. In data governance, practice built on DAMA-DMBOK, the most cited framework, draws the
same line: the *data owner*, on the business side, is accountable for the data in their domain; the
*data steward* looks after definitions and quality day to day; the *data custodian*, in IT, handles
the technical side.

Put into a responsibility matrix (who does it, who answers for the result, who is consulted and who is
informed), with one more role that does show up in projects: the data product owner, who answers for
the whole deliverable, from model to dashboard.

| Activity | Business owner (e.g. Controller) | Data product owner | Engineering / IT | Internal audit |
|---|---|---|---|---|
| Define the KPI and its control total | Accountable | Does | Consulted | Informed |
| Set the tolerance | Accountable and does | Consulted | Informed | Consulted |
| Build and run the witness | Informed | Accountable | Does | Informed |
| Explain exceptions | Accountable if business | Does | Does if technical | Informed |
| Keep the KPI aligned to the business | Accountable | Does | Consulted | Informed |
| Review that the control works | Consulted | Consulted | Informed | Accountable and does |

[ FIGURE 3 — "Who signs?": the simplified matrix, with the line "IT builds the witness; the business
owns the meaning". ]

There's a trap almost all of us who come from the technical side fall into: assuming that because we
built the dashboard, it's on us to guarantee the number is right. It sounds responsible, but it doesn't
work. From IT I can guarantee the calculation does what the spec says. I can't guarantee the spec is
still what the business needs after a reorganization that the sales leadership decided. That's why
keeping the KPI aligned belongs to the business and the mechanism that watches it belongs to IT. If
either one is missing, the checkmark hangs from nobody.

## And with conversational analytics, even more so

With a dashboard there's at least something fixed to look at. When the business asks an assistant a
question in plain language and the assistant writes the query every time, there's no report to
reconcile: there's a new answer for every way of asking.

That's where Genie's *benchmarks* are the right tool, with two conditions. First, the reference SQL has
to be reconciled against the same control totals as the dashboard, because if that SQL is wrong, the
benchmark grades one answer against another answer. Second, they have to run after every change to the
space. Today the documentation frames them as something a user with edit permission launches whenever
they want, and so they run when someone remembers.

## What to take away if you sign

If you sign the budget or the contract for a data project, three concrete things:

1. **Put the witness in the SOW and in the Definition of Done.** The SOW is the scope the vendor signs;
   the *Definition of Done*, the list of what has to be true to call a deliverable finished. Ask in
   the proposal for control totals, event-driven automatic reconciliation, the witness inventory and
   status visible on the dashboard, with their own hours and cost, not as an unbudgeted "best
   practice". And make the acceptance criterion the first reconciled month-end close after go-live,
   not go-live.
2. **Give every critical KPI an owner with a name.** Not "Finance": a person who signs the tolerance
   and who receives the exceptions.
3. **Make the dashboard say whether it reconciles.** It's the cheapest way to give the business back
   the certainty that today only the person reconciling by hand has.

None of this is new technology. It's discipline that audit and banking already imposed on themselves
and that we haven't adopted in data projects, because nobody asks for it in the proposal.

Thanks to whoever asked the question. The go-live reconciliation is a photo; the witness is what turns
it into a film.

---

## Sources

- PCAOB — *AS 1105: Audit Evidence*, ¶.10 (information produced by the company: test accuracy and
  completeness or the controls over them).
  https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105
- PCAOB — *Spotlight: Inspection Observations Related to Auditor Use of Data and Reports*, April 2024:
  ~17% of comment forms from the 2021 and 2022 cycles with deficiencies in the accuracy and
  completeness of company information; Staff Practice Alert 11; good practice of a central report
  repository.
  https://assets.pcaobus.org/pcaob-dev/docs/default-source/documents/data-and-reports-spotlight.pdf
- Basel Committee on Banking Supervision — *Principles for effective risk data aggregation and risk
  reporting* (BCBS 239), January 2013: Principle 3(c) and footnote 17 (reconciliation), ¶34 (business
  and IT roles), ¶37 (dictionary), Principle 7 and ¶53 (inventory of rules, exception reports), ¶56
  (materiality).
  https://www.bis.org/publications/201301-guidelines-principles-effective-risk-data-aggregation-and-risk-reporting.pdf
- Microsoft Learn — *Endorse Fabric and Power BI items* (Promoted, Certified, Master data; reviewers
  authorized by the administrator).
  https://learn.microsoft.com/en-us/fabric/fundamentals/endorsement-promote-certify
- Databricks — *Flag data as certified or deprecated* (`system.certification_status`; manual
  assignment or automation rules on usage, owner, age and tags).
  https://docs.databricks.com/aws/en/data-governance/unity-catalog/certify-deprecate-data
- Databricks — *Genie benchmarks* (up to 500 questions; Good / Bad / Manual review grading; on-demand
  runs).
  https://docs.databricks.com/aws/en/genie/benchmarks
- Snowflake — *Introduction to data quality checks* (Data Metric Functions, expectations, schedule,
  Enterprise Edition).
  https://docs.snowflake.com/en/user-guide/data-quality-intro
- Snowflake — *Use SQL to set up data metric functions* (`DATA_METRIC_SCHEDULE`: every N minutes,
  cron or `TRIGGER_ON_CHANGES`) and BCR 2025_07 (one-hour default schedule).
  https://docs.snowflake.com/en/user-guide/data-quality-working
  https://docs.snowflake.com/en/release-notes/bcr-bundles/2025_07/bcr-2101
- SAP Help — *Governing and Publishing Data in the Catalog* (SAP Datasphere: glossary, KPIs,
  publishing assets).
  https://help.sap.com/doc/5957319bdc7e4939a36ef363f844c60d/cloud/en-US/9a51a8731756457c935a49b5d510f63e.pdf
- DAMA International — *DAMA-DMBOK* (via Dataversity summary), data owner, data steward and data
  custodian roles.
  https://www.dataversity.net/data-concepts/what-is-the-data-management-body-of-knowledge-dmbok/
