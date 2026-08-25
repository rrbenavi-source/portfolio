# The clock that isn't yours

*They will sell you the move to Business Data Cloud with a date in red. If you are already on BW/4HANA, that date isn't yours — and the document you actually should read is published, free, and almost nobody opens it.*

**Brújula · Edition 08 · W35**
*Data Architecture · SAP*

---

Every deck opens the same way. A timeline, a date in red, an arrow pointing up:
**December 31, 2027**, end of mainstream maintenance for SAP BW on NetWeaver 7.5. The date
is real and the problem is enormous — at Sapphire 2025 SAP's own product management put
**20,000 to 30,000 customers** still on that version. For them the offer is a good one:
move the system as it stands into **SAP BW, private cloud edition** inside BDC and buy
three years, through the end of 2030, with no conversion project.

If you are already on **BW/4HANA**, that isn't your date. And this needs careful reading,
because the fact travels badly in both directions.

SAP aligned **the BW/4HANA product line** with S/4HANA through the end of **2040**, and
that commitment covers the on-premise deployment. But it is written as a commitment to a
line, delivered *"through a sequence of releases."* Your **release** has its own date:
BW/4HANA **2023** reached general availability on **October 30, 2023**, and its mainstream
maintenance ends on **December 31, 2030**. That isn't interpretation — it's what the
Product Availability Matrix says, and the PAM is the official source and the only one that
counts here. Seven years of cycle, of which nearly three are gone.

And if you also run **BPC**, the two travel as a pair. SAP BPC 2021 for BW/4HANA shipped in
November 2021 and BW/4HANA 2023 two years later, yet **both end on the same day: December
31, 2030**. Two products, one clock.

How it got there explains the mechanism. In January 2023 the PAM table SAP published on its
own blog gave BPC 2021 a date of **31.12.2027**, with a promise to announce closer to 2027
which version would carry on. Today the PAM says 2030: the promise was kept by **extending
the date on the release that already existed**, not by shipping a new one. There is no "BPC
2023." And that is exactly what a line commitment delivered *"through a sequence of
releases"* means: your date is real, and it is also revisable by whoever set it.

Neither the panic of 2027 nor the calm of 2040. **Four years and four months of runway on
what you already have**, and a committed path beyond it through successive upgrades.

And here is what the timeline in red hides: **a BW/4HANA upgrade is a technical project. A
move to Business Data Cloud is a change of contract, of consumption model, and of the
regime your data lives under.** They are not the same category, and choosing the second out
of fear of the first is expensive.

Strip out the borrowed urgency and three questions are left that do matter: **where your
data will come from, what you are signing, and what it actually costs.**

## What you genuinely gain, said plainly

I start here because the rest is uncomfortable and I don't want it read as a posture.

**You keep the asset.** The move is a *lift* **as-is**: the system is picked up and set
down in SAP's cloud exactly as it is, with nothing converted. Fifteen years of business
logic and of rules nobody ever documented in full are still there. **And BPC moves along
with the system** — precisely the piece that usually derails these projects, and here it
doesn't.

**The infrastructure finally shrinks.** The bulk volume drops to the object store — cheap
file storage, outside memory — and the machine gets sized for actual use. SAP documents the
case of going from 8 TB of memory to 2 TB.

**You move capacity without renegotiating.** BW services inside BDC fall under the BDC
contract rather than under RISE: shrinking BW and reallocating what it frees up to
Datasphere, SAC or Databricks is self-service.

**And the technical gap closes fast.** In January 2026 the most-cited complaint was that
*data products* — the curated data packages BDC publishes — travel as Parquet, a format
that carries no meaning. On April 30 the synchronization of semantic metadata into Unity
Catalog, Databricks' governance catalog, went generally available: four months between the
criticism and the close. Any purely technical objection I write today has an expiry date.

The two that haven't moved in eighteen months are the other two.

## Where the data comes from: the door almost nobody checks

BDC's premium content is the **SAP-managed data products** and the **Intelligent
Applications**. And they exist under a condition that doesn't make the cover slides: **your
ERP has to be in SAP's cloud.**

The official FAQ says it without hedging. BDC supports the cloud editions of S/4HANA —
private cloud edition and public cloud — and there the managed data products are
*"exclusively available."* On everything else: *"there are no immediate plans to extend
support to on-premise S/4HANA systems."* On-premise systems get a customer-managed option
instead: they connect and push their own data in, but the managed catalog does not apply to
them.

This is not a theoretical limitation. There is KBA **3786663**: *"S/4HANA on premise system
is not listed in formation."* A *formation* is the grouping of systems registered together
so BDC recognizes them as a landscape, and the on-premise system simply **does not appear**
there. Among the KBA's keywords is *integration not supported*: this is not a configuration
problem, it's design.

**And ECC appears nowhere as a source for managed data products.** It appears on the
roadmap: catalog crawling in Q2-2026, direct ingestion into SAP Databricks in 2026. Both,
plan.

Everything else comes in through a different pipe. Datasphere's connectivity does accept
S/4 on-premise, ECC, Z fields — the ones your own people added to the standard tables —
custom CDS views, and non-SAP sources: Oracle, SQL Server, Salesforce, object stores,
Snowflake, BigQuery. But all of that lands as **your own data product**, in Datasphere's
object store, which is a different store from Foundation Services, where SAP keeps its own.
Two worlds that don't cross.

The size of the catalog is worth a look too. In early 2026 there were **259 standard data
products** generally available, **mostly master data**, with **three source systems**:
S/4HANA private, S/4HANA public and SuccessFactors. The pitch also mentions Ariba, Concur
and Fieldglass; the inventory doesn't. And you don't have to take anyone's word for it: SAP
publishes the catalog in the Discovery Center, it can be browsed without asking for a quote,
and the only thing to do is filter by your source system **before** looking at the total.

### The one clock that is yours, and it expires this year

To understand why the architecture looks like this, you have to look at the door that closed
before — and the one closing right now.

ODP — *Operational Data Provisioning* — is the framework through which, for more than a
decade, every external tool pulled data out of an ABAP system: ECC's extractors, BW's
DataSources, everything came out that way. Note **3255746** dates back to 2022, when SAP
warned that those APIs were internal and unsupported. In its February 2024 version it went
from warning to prohibition — customers and third-party applications **are no longer
permitted** to use them — and pointed customers at Datasphere for replication into
third-party tools. The note is now on its **version 11, dated April 21, 2026**.

And in **June 2026 the prohibition stopped being contractual and became technical**: a
security patch validates incoming calls and **blocks** the ones coming from unauthorized
applications against S/4HANA, BW and ECC. There is a **temporary opt-out that keeps those
calls alive only through the end of 2026**, and since **April 13, 2026** SAP has published a
self-assessment tool — note **3439624** — that inventories all ODP-RFC usage across the
landscape.

Read that against the rest of this piece. The date in red they show you is 2027 or 2030,
and it is somebody else's release clock; **this one has your name on it and expires in
December**. This week's exercise isn't drawing a roadmap to 2030: it's running 3439624 and
counting how many of your own pipes depend today on a door that is already shut and propped
open by an opt-out.

The historic route for pulling ABAP data into a lake of your own closed first; the new one
comes with a contract, a metric and a price. That order is not an accident, and it explains
everything that follows.

## The document nobody opens

BDC's terms are public and download from the Trust Center without registration. The current
version — the seventh of 2026 — has paragraphs worth more than any demo. I'll start with the
one that decides architecture, section 3.3:

> *"Customer may allow Third-Party Connectors to temporarily store or materialize Data
> Products on such Third Party Connectors' systems solely for performance optimization
> purposes. For the avoidance of doubt, Customer may not allow Third-Party Connectors'
> systems to distribute Data Products to systems other than SAP Business Data Cloud."*

In short: you can share a data product with your own Databricks, and it can sit there copied
**temporarily and only so queries run faster**. What that Databricks cannot do is **pass it
along**. Power BI, Tableau, an external lake, another tenant: all of them land on the wrong
side of that sentence. Your lakehouse stops being the layer everything is served from and
becomes an authorized consumer, not a redistributor.

Watch the consequence for anyone already moving data with their own tooling: **swapping your
pipeline for *zero-copy*** — sharing the data where it already sits, without moving or
duplicating it — **isn't changing pipes, it's changing the regime the data lives under.**
What is yours today and freely redistributed is a licensed object tomorrow.

The argument circulating among consultants to get around the restriction is that data
transformed heavily enough stops being a data product. I wish. Section 1.11 defines *Data
Product* as *"enriched data or enriched Customer Data, where enrichment is any type of
reorganization, semantics, summarization, reporting or metadata."* Enrichment is not what
gets you out of the definition: it's what puts you in it. SAP may well accept that reading
in your case; it isn't in the text. If your architecture depends on it, get it in writing
before you design.

Three more paragraphs before the datasheet:

- **3.5.** SAP declares itself the owner of the intellectual property in the data products;
  you hold a license to use them.
- **3.6.** Using a third-party connector **is consent** for SAP and that third party to
  exchange usage information, *"including identifying Customer."* Databricks' documentation
  — updated August 4, 2026 — is more specific: it can disclose to SAP the volume of BDC data
  and its ratio against non-BDC data, and **the effective price your organization pays for
  Databricks consumption**, by workload and un-anonymized.
- **2.6.4.** BDC Connect services are classified as **Group 2**: if SAP deprecates a Group 1
  service you keep using it for the remainder of your subscription; if it's Group 2, when the
  six-month notice expires **you lose access**. The bridge to your own Databricks is, by
  contract, the switchable-off piece.

## Capacity units don't roll over

BDC is sold in **capacity units**: chips reallocatable across Datasphere, SAC, BW in private
cloud and Databricks. Inward, the flexibility is real. Outward, three rules.

**What you don't spend is lost.** One sentence — *"Unused Capacity Units may not be carried
over into any subsequent month"* — plus the clarification that they aren't prorated for
partial months either. This isn't the annual expiry of BTP credits: it's monthly. You budget
by the year and consume by the month. I'm citing this clause from the **October 2025**
Supplement, not from the current version; the document changes several times a year, so
confirm this one in the exact version they put in front of you to sign.

**The contract ships with a declared erratum.** Section 2.4 clarifies that where the Order
Form says the usage metric shows the maximum usable over twelve months, it *"includes a
drafting error"* and should read **one month**.

Before the numbers, the thing that makes them readable: **SAP does not publish the price of a
capacity unit.** What follows isn't dollars, it's chips — good for comparing one product
against another and one tier against another, not for estimating an invoice.

**And SAP Analytics Cloud is back to being priced per user:** **25.60** capacity units per BI
user per month in the 25-to-200 tier, dropping to **10.54** above 5,000. The planning numbers
are another league: **72.85** per user for standard planning and **820.43** for professional
planning. If your horizon includes moving planning from BPC to SAC — which is SAP's declared
direction, and which **is not a migration but a reimplementation** — those are the lines that
decide the case. On top of that, BDC Core *"must always be sold in conjunction with at least
one Intelligent Application,"* and the minimum viable implementation SAP itself presents
starts at **640 capacity units**.

Cross that rule with the previous section and something uncomfortable falls out: every
Intelligent Application SAP publishes has a cloud product as its source application. A
customer with an on-premise ERP is obliged to buy at least one intelligent application **that
its ERP cannot feed**. That is an inference of mine, drawn across two documents, not a
statement by SAP — and it is exactly the question to ask in writing.

## And from here, this looks different

I write from Monterrey, and the case I just described isn't an edge case: it's the case for a
good part of the region's installed base. Large manufacturing and consumer-goods operations,
ECC still on the floor, an S/4 migration planned for 2027 or 2028, and twenty years of
business rules living inside BW queries — how a sale is recognized, how freight is allocated,
what counts as a return.

For that profile, BDC delivers its premium value **after** the S/4 migration, not before. The
reference architecture is written for a landscape most of them don't have yet. Which makes
Business Data Cloud, for much of the local market, **a 2028 decision dressed up as a 2026
urgency**.

That doesn't mean standing still. It means separating the clocks: your release's, your ERP's,
and the ones for tools that genuinely do have a short date. They are rarely the same.

## What to ask for before signing

Four things worth more than the discount:

1. **The reading of "enriched," in writing.** If your architecture depends on transformed data
   ceasing to be a data product, let the contract say so, not a call.
2. **What you get today with the ERP you have today.** If your ERP is on-premise, have them
   list by name the managed data products you would actually have access to. And have them
   explain which Intelligent Application you're buying and what will feed it.
3. **Cost modeled over 24 months with the monthly expiry built in**, including the planning
   population if BPC is headed for SAC.
4. **A portability clause for the semantics.** Forrester said it in May more bluntly than I
   would: SAP is building a data *control plane* for AI — the layer that decides who can read
   what, and with what meaning — and the window to negotiate is twelve to twenty-four months,
   before agents freeze those decisions into systems of work.

Business Data Cloud is probably the destination. The part you decide is the calendar — with
one exception, the one we opened halfway through: the piece of calendar you no longer decide
is ODP, and that one expires in December.

*The next edition follows one concrete sales query — from BW to SAC — station by station, with
what has to be validated at each one and what gets lost along the way without anyone saying so.*

---

## Sources

- **SAP.** *Product Availability Matrix — SAP BW/4HANA 2023.* **Official and primary source
  for the dates.** Release to Customer and general availability on 30-Oct-2023; end of
  mainstream maintenance **31-Dec-2030**. Requires an SAP for Me session.
  https://userapps.support.sap.com/sap/support/pam
- **SAP.** *Product Availability Matrix — SAP BPC 2021, for SAP BW/4HANA.* RTC and general
  availability on 01-Nov-2021; end of mainstream maintenance **31-Dec-2030**, the same date as
  BW/4HANA 2023. Contrast with the PAM table SAP published in January 2023, which gave
  31.12.2027 for that same product: the extension was made on the existing release. Requires an
  SAP for Me session.
  https://userapps.support.sap.com/sap/support/pam
- **SAP.** *SAP BW/4HANA to extend maintenance in alignment with SAP Business Suite and SAP
  S/4HANA.* The BW/4HANA **product line** is maintained through the end of 2040, aligned with
  S/4HANA and including on-premise, delivered through a sequence of releases. The 2040
  commitment is to the line; the release date is in the PAM, above.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-bw-4hana-to-extend-maintenance-in-alignment-with-sap-business-suite-and/ba-p/13457952
- **SAP.** *Maintenance timelines for SAP Business Planning and Consolidation (SAP BPC)*,
  official blog. PAM dates by version and the explanation of the successive-release mechanism:
  *"as we approach 2027, we will share which version of SAP BPC for SAP BW/4HANA will be
  available beyond 2027."*
  https://community.sap.com/t5/financial-management-blog-posts-by-sap/maintenance-timelines-for-sap-business-planning-and-consolidation-sap-bpc/ba-p/13551547
- **SAP.** *SAP Business Planning and Consolidation (SAP BPC) Strategy Update*, October 8,
  2025. BPC 10.1 NW and BPC 2021 can move to private cloud **together with** the BW system; BPC
  2021 supports BW/4HANA 2021 and 2023 with end of maintenance on 31-Dec-2030.
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-business-planning-and-consolidation-sap-bpc-strategy-update/ba-p/14237803
- **SAP.** *SAP Business Data Cloud — FAQs*, official blog. Supported S/4HANA editions and the
  phrase *"SAP-managed Data Products are exclusively available"* for private and public cloud,
  with *"no immediate plans to extend support to on-premise S/4HANA systems."*
  https://community.sap.com/t5/technology-blog-posts-by-sap/sap-business-data-cloud-faqs/ba-p/14022781
- **SAP.** KBA **3786663**, *[BDC-FOS] S/4HANA on premise system is not listed in formation*.
  The on-premise system does not appear in the formation list; keyword *integration not
  supported*.
  https://userapps.support.sap.com/sap/support/knowledge/en/3786663
- **SAP.** Note **3255746**, *Unpermitted usage of ODP*. Prohibition on customers and third
  parties using the ODP APIs to reach ABAP sources, and redirection to Datasphere. Version 11,
  April 21, 2026. Requires an SAP for Me session.
  https://me.sap.com/notes/3255746
- **SAP.** Note **3439624**, self-assessment tool for ODP-RFC usage across the landscape,
  published April 13, 2026. Requires an SAP for Me session.
  https://me.sap.com/notes/3439624
- **SAPinsider.** *SAP Note 3255746: The June 2026 ODP-RFC Deadline Explained.* Industry
  publication, not a vendor: the date of the June 2026 security patch that blocks unauthorized
  ODP-RFC calls against S/4HANA, BW and ECC; the temporary opt-out in force through the end of
  2026; version 11 of the note and the reference to 3439624. ⚠️ Confirm the exact scope of the
  opt-out in the note itself before committing to it with a client.
  https://sapinsider.org/blogs/sap-note-3255746-odp-rfc-deadline-2026/
- **SAP.** *SAP Business Data Cloud — Supplemental Terms and Conditions*, version 7-2026,
  public document. Sections 1.11, 2.4, 2.6.4, 3.1–3.7 and 6.2.5.
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v7-2026.pdf
- **SAP.** *SAP Business Data Cloud Supplement*, version 10-2025, sections 3.2.2 and 3.2.4:
  *"Unused Capacity Units may not be carried over into any subsequent month."*
  https://assets.cdn.sap.com/agreements/product-use-and-support-terms/cls/en/sap-business-data-cloud-supplement-english-v10-2025.pdf
- **Raver, B. (SAP).** *Breaking Down the SAP BDC Pricing Model*, April 16, 2026, presentation
  to the SAP user groups. SAC capacity-unit values by tier, standard and professional planning,
  the rule of always selling with at least one Intelligent Application, and the 640 capacity
  unit minimum.
  https://assets.dm.ux.sap.com/sap-user-groups/pdfs/260416_breaking_down_the_sap_bdc_pricing_model.pdf
- **Expertum.** *SAP Business Data Cloud: Reflections After One Year of Data Products*, January
  8, 2026. Count of 259 standard data products, mostly master data, and the three supported
  source systems. Dated January 2026 and from an implementation partner, not SAP: cited in the
  text with its date, with the reader pointed at the official catalog.
  https://expertum.net/sap-bdc-reflections-after-one-year/
- **SAP.** *SAP BDC Catalog*, Discovery Center. Public catalog of data products, browsable
  without a quote and filterable by source system.
  https://discovery-center.cloud.sap/bdcCatalog
- **Databricks.** *Share data between SAP Business Data Cloud (BDC) and Databricks*, official
  documentation, last updated August 4, 2026.
  https://docs.databricks.com/aws/en/opensharing/sap-bdc/
- **Databricks.** *Unlocking SAP business context in Databricks with semantic metadata Delta
  Sharing*, April 30, 2026. Vendor source on its own product.
  https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing
- **SAPinsider.** *Modernizing SAP BW: The Path to Business Data Cloud*, May 21, 2025. Dominik
  Kurz (SAP) with the 20,000-to-30,000 figure for BW 7.5 customers and the 8 TB to 2 TB
  reduction example.
  https://sapinsider.org/analyst-insights/modernizing-sap-bw-the-path-to-business-data-cloud/
- **Forrester.** *SAP Is Targeting The AI Data Control Plane*, May 14, 2026.
  https://www.forrester.com/blogs/sap-is-targeting-the-ai-data-control-plane/
