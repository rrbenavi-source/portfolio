# We removed BW. The engine stayed.

## A client switched off BW and BusinessObjects when it moved to S/4HANA, and today it reports straight into SAP Analytics Cloud. It works. But every query still runs on BW's analytic engine, now inside the ERP. And the work the BO universe used to do did not disappear: it has to be written again, in CDS views, with annotations, and tested in RSRT before anyone opens a dashboard.

A client we work with came from the most common picture in industry here in Nuevo León, and
in half the country: ECC as the ERP, BW 7.3 as the data warehouse and BusinessObjects as the
reporting layer. Three systems, and in each one a different place where a number could change
its meaning. BW 7.3 has been out of mainstream maintenance since the end of 2020, and
BusinessObjects 4.3 reaches the end of its own on December 31 this year, so the S/4HANA
migration was also the moment to decide what to do with the other two.

They decided something I see more and more often around here: **remove both**. No BW, no BO.
S/4HANA exposes the data through CDS views and SAP Analytics Cloud (SAC) consumes it, most of
the time over a *live* connection, a few times by *import*. One source system, and the ERP as
the only truth.

It is a decision that defends itself, and I would sign it again. But there are two things worth
saying out loud before signing, because neither shows up in the vendor's deck. The first is that
the BW engine did not go anywhere. The second is that the BusinessObjects universe did not go
anywhere either: it stayed, only now as debt.

## What happens when you flag a view

In S/4HANA, a CDS view becomes consumable from SAC the moment you put one annotation on it:
`@Analytics.query: true`. The SAC documentation says it straight: only views carrying that
annotation appear in the *live* connection. What it does not say as loudly is what happens
behind it.

When the view is activated, the system generates a **transient query**, an analytical query you
never designed in any editor, living under the name `2C` plus the SQL name of your view. That
query is not executed by HANA directly. It is executed by the **analytic engine** embedded in
every S/4HANA: the same OLAP engine that runs BEx queries in a BW. SAC talks to it over the
**InA** protocol, the one Design Studio and the BusinessObjects tools already used to query HANA
and BW. And the transaction to test it is **RSRT**, the one any BW consultant has opened ten
thousand times.

That is why I say we removed BW and the engine stayed. It is not a metaphor. It is the
architecture. What left is the **persistence** (the InfoProviders, the nightly loads, the
separate system) and the **language** (BEx Query Designer). What arrived in its place is a new
language, CDS annotations, to talk to the same engine.

This has a practical consequence worth more than any diagram, and I have run into it right when
it was time to validate: **if you execute an analytical view with F8 from Eclipse, the result is
not what SAC is going to see.** F8 asks HANA; SAC asks the engine. Exception aggregations, query
formulas, texts and hierarchies of the characteristics are all resolved in the engine. If the
test does not go through RSRT, you did not test what the user is going to see. You tested
something else.

## Three layers

The most expensive mistake I have seen in these projects is writing one giant view, with every
join, every calculation and the query annotation on top, and calling it "the report". It works
the first time. The second time, when someone asks for one more field, the view breaks or gets
duplicated.

SAP organizes its own views in a three-layer **Virtual Data Model**, and the practice we applied
with this client was to respect those layers in custom development too. I name them with the
prefixes we use (`ZI_` for interface, `ZC_` for consumption) because the prefix is part of the
discipline.

**Layer 1: basic views and dimensions.** One view per business entity, with no reporting logic.
Dimensions carry `@Analytics.dataCategory: #DIMENSION` and declare which field is the key and
which is the text. This is the layer that makes SAC show "Customer 1000 · Comercial del Norte"
instead of a bare number.

```abap
@AbapCatalog.sqlViewName: 'ZICUSTOMER'
@VDM.viewType: #BASIC
@Analytics.dataCategory: #DIMENSION
@ObjectModel.representativeKey: 'Customer'
@EndUserText.label: 'Customer (dimension)'
define view ZI_Customer as select from kna1
{
  key kunnr as Customer,
  @Semantics.text: true
      name1 as CustomerName,
      land1 as Country
}
```

**Layer 2: the cube.** This is where the facts live: the billing item, the material movement,
the transport document. It is annotated as `#CUBE`, which SAP defines as factual data that may
contain redundancy, and that is why it is the right place for associations to the dimensions.
Every amount declares its currency, every quantity its unit, and every measure says how it
aggregates. Without that, SAC adds things up however it can.

```abap
@AbapCatalog.sqlViewName: 'ZISALESCUBE'
@VDM.viewType: #COMPOSITE
@Analytics.dataCategory: #CUBE
@EndUserText.label: 'Sales (cube)'
define view ZI_SalesCube as select from ZI_BillingItem as Item
  association [0..1] to ZI_Customer as _Customer
    on $projection.Customer = _Customer.Customer
{
  key Item.BillingDocument,
  key Item.BillingDocumentItem,
      Item.BillingDate,
      @ObjectModel.foreignKey.association: '_Customer'
      Item.Customer,
      Item.DistributionChannel,
      @Semantics.amount.currencyCode: 'TransactionCurrency'
      @DefaultAggregation: #SUM
      Item.NetAmount,
      @Semantics.currencyCode: true
      Item.TransactionCurrency,
      @Semantics.quantity.unitOfMeasure: 'BaseUnit'
      @DefaultAggregation: #SUM
      Item.BillingQuantity,
      @Semantics.unitOfMeasure: true
      Item.BaseUnit,
      _Customer
}
```

**Layer 3: the query.** This is the view SAC sees. It brings no new joins and no business
logic: it brings **presentation decisions**. What goes in rows by default, what goes in columns,
which formulas the engine calculates, which variables it asks for on opening. And the one
annotation that makes it visible.

```abap
@AbapCatalog.sqlViewName: 'ZCSALESQ'
@VDM.viewType: #CONSUMPTION
@Analytics.query: true
@EndUserText.label: 'Sales by customer (query)'
define view ZC_SalesQuery as select from ZI_SalesCube
{
  @AnalyticsDetails.query.axis: #ROWS
  @AnalyticsDetails.query.display: #KEY_TEXT
  Customer,
  @AnalyticsDetails.query.axis: #FREE
  DistributionChannel,
  @AnalyticsDetails.query.axis: #COLUMNS
  NetAmount,
  BillingQuantity,
  @AnalyticsDetails.query.formula: 'NetAmount / BillingQuantity'
  @EndUserText.label: 'Average price'
  0 as AveragePrice
}
```

Three views, three responsibilities. If Sales asks tomorrow for price per ton instead of per
piece, you touch the query. If Finance asks for local currency, you touch the cube. If master
data changes the customer's name, you touch nothing.

One detail that sounds minor and is not: the query's `@AbapCatalog.sqlViewName` annotation is
what defines the name under which it exists in the engine. In the example, the transient query
is called `2CZCSALESQ`, and the cube underneath is the provider `2CZISALESCUBE`. In RSRT you look
them up together, `2CZISALESCUBE/2CZCSALESQ`, and the query name is the one that shows up in SAC
when you create the model.

## The annotations that actually matter

There are hundreds of CDS annotations. For reporting in SAC, the short list, the one that
simply cannot be missing, is this.

1. `@Analytics.dataCategory` with `#DIMENSION` on master data and `#CUBE` on facts. It tells the
   engine what is the star and what is the center.
2. `@Analytics.query: true`, only on the consumption layer. It is the door into SAC.
3. `@ObjectModel.representativeKey` on every dimension, so the engine knows which field is the
   key when the view has several.
4. `@Semantics.text: true` on the description field, and `@ObjectModel.text.association` when
   the text lives in another view. Without this, SAC shows you nothing but codes.
5. `@Semantics.amount.currencyCode` and `@Semantics.quantity.unitOfMeasure` on every measure,
   with their partner `@Semantics.currencyCode: true` or `@Semantics.unitOfMeasure: true`. This
   is what keeps pesos from being added to dollars, or pieces to tons.
6. `@DefaultAggregation` on every measure (`#SUM`, `#MAX`, `#NONE`). Without it, every figure
   inherits a default behavior nobody chose.
7. `@AnalyticsDetails.query.axis`, `.display`, `.totals` and `.formula` on the query. They are
   the equivalent of what used to be configured in BEx: initial layout, key or text, totals,
   formulas calculated in the engine.
8. `@AccessControl.authorizationCheck: #CHECK` with its DCL. In BW, security came from the
   analysis authorization; here you set it yourself, view by view, and the engine applies it on
   every request from SAC.

There is a ninth one that is not for SAC but is worth knowing: `@Analytics.dataExtraction.enabled:
true`. It marks the view as fit for **replication** through ODP into a warehouse or a lake. It
is another door, with other rules and another contract, and I wrote about that one in the last
issue.

## RSRT before SAC

With this client, the unit test of an analytical view is not done in SAC. It is done in RSRT,
with the `2C` name of the query, and with three concrete checks: that the **free
characteristics** are the expected ones, that **texts** come out next to the keys, and that
attributes derived from a dimension (for example region, line and channel hanging off a sales
office) arrive with the right value for every key.

The reason is the one above: SAC is a thin client, it asks and it shows, it neither calculates
nor persists. If the number is wrong in SAC, the number is wrong in the query, and the query is
debugged in RSRT, where you can see the plan, switch the cache on and off, look at the
statistics and compare against the result of a standard transaction. When a story gets slow, the
cause is almost always in the cube (too many joins) or in the query (too many formulas in the
engine), not in SAC. SAC only delivers what it is given.

And there is a figure from SAP worth keeping at hand. The embedded analytics Quick Sizer assumes
a query takes at most **10 seconds**. If a view takes 60, the problem is not only that the user
waits: the system sizing assumed six times less resource for that request. Reporting on top of
the ERP means every badly built query is charged to the ERP, and the ERP charges it to everyone
else.

## The hidden universe

When this client started comparing the new SAC reports against the old BusinessObjects ones,
page by page, three kinds of difference showed up. None of them was a SAC fault.

The first: **filters the BO report applied that nobody had written down.** Figures that matched
in recent years and not in others, tables where SAC brought back more than BO did, and one
sentence that sums up the whole problem, written by the person validating: *"there are filters
we could not identify in order to apply them in the SAC query"*. Those filters lived in the BO
universe or in the report itself, not in the data. When BO was switched off, they were switched
off with it.

The second: **rounding.** BO rounded to whole numbers in several tables; SAC showed the decimals
the CDS brought. It was the same number. It looked like two.

The third: **one full historical year that did not match.** All the later years matched; the
oldest one did not. The most likely explanation is not a lost filter: it is data that existed in
BW because BW loaded it at the time, and that is no longer the same in S/4HANA. That is the case
SAP describes when it explains what embedded analytics is **not** for: snapshots, master data
historization, long retention. A data warehouse keeps the photo; an ERP keeps the state.

And there was a fourth one that did not come out of the comparison but out of reading the
stories: in one of them, the distribution center label was resolved with a chain of "if the
planning point is 01 then North, if it is 06 then Center". Business logic written in the front
end. It works, and it works well. But the next story that needs the same mapping will write it
again, and at some point the two versions will diverge.

The thesis is this: **the semantic layer does not disappear when you switch off the tool that
held it.** In BusinessObjects it lived in the universe; in BW, in the BEx query and the
InfoObjects. When you remove both, that meaning has exactly two places it can land: the CDS
view, once, with annotations everyone consumes; or every story, every time, by hand. Whatever
you do not annotate in layer 2 or layer 3, you will find rewritten in the front end, right when
it matters, in triplicate.

That is why the three-layer discipline is not an architect's preference. It is the only way the
hidden universe gets a visible place to live.

## Live or import

One last decision worth understanding before signing, because it changes which objects you are
going to build.

The **live** connection is the one that consumes analytical queries. SAC asks, the engine
answers, nothing is copied. It is the one that respects the ERP's security, the one with no lag,
and the one that hits the ERP with every click.

The **import** connection does not consume CDS views. The SAC documentation says it literally:
it consumes **OData services**. That means that to import you need another annotation
(`@OData.publish: true`), another object activated in Gateway, and you accept that one-to-many
relationships are not followed. In exchange, the data stays in SAC, it can be blended with other
sources and it does not hit the ERP on every query.

With this client the rule ended up simple: live by default, import only when the report needs
to be blended with something that is not in S/4HANA (a budget that comes from somewhere else,
for example) or when the volume and frequency of use do not justify hitting the ERP on every
open. And one SAP-documented warning that surprises more than a few: **blending** between a live
S/4HANA model and another one was not available in the optimized story mode in the versions the
support note describes, and SAP has been enabling it piece by piece in later versions. If the
design depends on blending, test it on the version you have before promising it.

## True north

I would sign this client's architecture again. One ERP, one front end, CDS views as the contract
and no intermediate copy to maintain. For a company of its size, with operational reporting and
an analysis horizon of two or three years, it is the right decision, no second-guessing.

What I would ask of anyone about to make the same decision are three things, and none of them is
a license.

**Budget the rebuild of the semantic layer as a deliverable, not as a consequence.** The
filters, the rounding rules, the mappings and the hierarchies that today live in BO universes
and BEx queries have to be inventoried before switching anything off, and they have to land in
layers 2 and 3, with annotations. If the plan only says "migrate reports", that work will show
up anyway, but in the validation phase, with the clock running.

**Make RSRT the quality gate.** No query reaches SAC without going through it. It is cheap, the
engine understands it, and that is where performance problems are seen before a director sees
them.

**Do not retire the BW team: retrain it.** The engine, the protocol and the transaction are
still there. What changed is the language. A consultant who understands how the engine
aggregates, how exceptions behave and what a free characteristic is has most of the road done;
what is missing is annotation syntax, and that is learned in weeks, not years.

We removed BW. The engine stayed. It should be treated as what it is: the same engine, with a
different name on the door.

---

### Sources

- SAP Help Portal — *Live Data Connections to SAP S/4HANA* (SAP Analytics Cloud): "Only CDS
  Views containing the @Analytics.query: true annotation will appear in SAP Analytics Cloud";
  transient query named `2C<sqlViewName>`; Direct connection with CORS, Tunnel slower; refers to
  SAP Notes 2595552 and 2715030.
  https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/00f68c2e08b941f081002fd3691d86a7/d2a1edf7cda74315a2c5052de8a3a4eb.html
- SAP Help Portal — *Import Data Connection to SAP S/4HANA* (SAP Analytics Cloud): "SAP
  Analytics Cloud does not consume CDS views from SAP S/4HANA, it consumes OData services only";
  one-to-many navigation and complex type limitations.
  https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/00f68c2e08b941f081002fd3691d86a7/63140f17362947fe8bcd9c6960db23bc.html
- SAP Help Portal — *Analytics Annotations* (SAP NetWeaver 7.5): definitions of
  `Analytics.dataCategory` (#DIMENSION, #FACT, #CUBE, #AGGREGATIONLEVEL), `Analytics.query`,
  `Analytics.dataExtraction.enabled`, `Analytics.hidden`, `Analytics.planning.enabled`.
  https://help.sap.com/doc/saphelp_nw75/7.5.5/en-US/c2/dd92fb83784c4a87e16e66abeeacbd/content.htm
- SAP Community, Enterprise Architecture Knowledge Base — Peter Schmidt (SAP), *When to use SAP
  S/4HANA Embedded Analytics?*, Oct 17, 2022: "First choice should be SAP S/4HANA embedded
  analytics specifically for light-weight real-time data models"; criteria on snapshots,
  historization, retention, harmonization and cross-system.
  https://community.sap.com/t5/enterprise-architecture-knowledge-base/when-to-use-sap-s-4hana-embedded-analytics/ta-p/5154
- SAP Community — Masaaki Ishii (SAP), *Analytics in S/4HANA: real shape of embedded analytics
  and beyond embedded analytics*, 2019, updated 2023: the InA connection for SAC, the Quick
  Sizer expectation of 10 seconds and the resource impact of a 60-second view.
  https://community.sap.com/t5/enterprise-resource-planning-blog-posts-by-sap/analytics-in-s-4hana-real-shape-of-embedded-analytics-and-beyond-embedded/ba-p/13403536
- SAP Community — Pavan Kumar Reddy, *Step 2: Define the Analytical Query CDS View*, Feb 26,
  2017: testing the query in RSRT with the `2C` prefix and the warning that F8 execution does not
  reflect the analytic engine result.
  https://community.sap.com/t5/technology-blog-posts-by-sap/step-2-define-the-analytical-query-cds-view/ba-p/13349493
- SAP KBA 2591655 — *Performance analysis when using SAP HANA Live Data Connections in SAP
  Analytics Cloud*: InA endpoint and the method of isolating complex models.
  https://userapps.support.sap.com/sap/support/knowledge/E/2591655
- SAP KBA 3466290 — *Data blending for S/4HANA or BW models is not available in optimized mode
  of story in SAP Analytics Cloud*; and SAP KBA 3507024 on blended charts with BW live models in
  optimized stories from 2024 QRC3.
  https://userapps.support.sap.com/sap/support/knowledge/en/3466290
- SAP KBA 3763590 — *SAP BI Platform 4.3: End of Mainstream Maintenance 31 December 2026*.
  https://userapps.support.sap.com/sap/support/knowledge/en/3763590
- SAP Community — *SAP NetWeaver 7.5 Maintenance Strategy*: end of mainstream maintenance for
  SAP NetWeaver 7.3, 7.31 and 7.4 at the end of 2020.
  https://pages.community.sap.com/topics/abap/netweaver-maintenance-strategy
