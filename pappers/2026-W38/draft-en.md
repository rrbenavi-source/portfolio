# The customs house

## Leaving SAP on the analytics side is a legitimate decision. Since June 2026 it is also a contractual one: the door your data leaves through has an owner, a meter, and no shut-off valve.

A client we work with made a decision I expect to see many more times over the next three years.
They came from ECC with reporting on BW 7.5 —the previous generation of SAP's data warehouse, the
one still running in half the industry— and moved to S/4HANA. So far, the familiar movie.

The interesting part happened on the other side. When the time came to pick the analytics
platform, they did not take the house route. No BW/4HANA, no SAC. They went to **Microsoft
Fabric** and a data lake. The integration looks like this: **CDS views** in S/4HANA —the views
that expose ERP data already carrying business context, rather than as raw tables— consumed by
**SAP Datasphere replication flows** that land it ready for Fabric.

It is a defensible architecture and I think it is well built. But it holds a paradox worth saying
out loud: **in order to leave SAP analytics, they had to buy an SAP analytics product.**

That is not an accident of this project. It is the shape the market took this year, and very few
people have it in their business case.

## Until recently, the door was free

For fifteen years the answer to "how do I get my data out of SAP?" was practically universal:
**ODP** —*Operational Data Provisioning*, the layer that exposes SAP data to the analytical
world— and specifically its RFC interface, **ODP-RFC**. Every integration tool on the market
connected through it. It was the service entrance: not in the brochure, but open, and everyone
used it.

SAP closed it. Not abruptly, and not quietly.

Note **3255746** —*Unpermitted usage of ODP Data Replication APIs*— was published in 2022, saying
those APIs were for internal use and unsupported for third parties. It is now on **version 12,
released on 9 June 2026**, and the wording leaves no interpretive room:

> "Any use of ODP-RFC by customer or third-party applications to access SAP ABAP applications that
> contain one of the following components (PI\_BASIS, SAP BW, SAP BW/4HANA) that run on-premise or
> in private-cloud setup is **prohibited**."

And it did not stop at policy. The same note announces the mechanism: a security note —**3748819**,
from the June 2026 Patch Day, with the code corrections in **3635619**— that validates incoming
calls against permitted subscriber types and **blocks** the ones that are not.

There is an escape valve, and its full terms are worth reading. Note **3731818** ships a report,
`RODPS_REPL_SECUREACCESS_OPTOUT`, that temporarily suspends the block. SAP describes it as
strictly time-limited, intended only to mitigate short-term operational disruption, and applied
**at the customer's own risk**. It closes like this:

> "This temporary exception will expire end of 2026. Upon expiration, SAP will release an SAP note
> that will reinstate mandatory secure-by-default protections … which will permanently disable the
> temporary exception mechanism and **will be enforced without exception**."

*Enforced without exception.* That is not a target date. It is an expiry date.

And there are two more lines in 3255746 that a CIO should read before any architecture diagram:

> "SAP reserves the right to modify ODP-RFC modules at any time without prior notification to
> customers."

> "Any issues or incidents resulting from ODP-RFC implementation outside the scope of SAP's
> prescribed guidelines remain the sole responsibility of the customer."

The second one is not a technical warning. It is a transfer of liability.

The sign that none of this is consulting folklore: **Microsoft documents it in its own guidance.**
Its SAP CDC connector carries this verbatim caveat:

> "While Microsoft fully supports the SAP CDC connector as a reliable solution for data
> extraction, before using the SAP CDC connector, consult the relevant SAP Note: *3255746 -
> Unpermitted usage of ODP Data Replication APIs* to determine if it's relevant for your current
> SAP licensing."

And the guide opens, ahead of any technical content, with this:

> "Before you begin any data extractions from SAP systems, always verify your organization's SAP
> licensing entitlements. Certain extraction methods can require other licenses or specific usage
> rights."

When the vendor of the destination reminds you to check the licence of the source, that tells you
where the real risk sits.

It is worth reading the change without drama: **this is not a technical deprecation, it is a
decision about ownership.** SAP stopped treating extraction as an infrastructure detail and
started treating it as a product. That is legitimate. But it changes the nature of the question:
"how do I get my data out" stopped being an ETL topic and became an architecture and contract
topic.

## The inventory that does not exist yet

SAP also shipped the tool to find out who is touching that door today: note **3439624**, on
version 34 as of 9 September 2026, installs the report `RODPS_REPL_SUBSCRIBER_ASSESS`, which
classifies every call into four states: permitted, unpermitted, *unclear* (reserved for SAP Data
Services and HANA Smart Data Integration, which you then have to verify by hand), and no
assessment info.

It has two properties that completely change **when** you need to act.

The first: **it assesses calls from the moment it is installed, and it does not assess historical
calls.** Your ODP-RFC usage inventory is not waiting for you in some log. It starts existing the
day you implement the note. Every week you postpone is a week of blindness you cannot recover
backwards, against a deadline that sits in December. And in a BW 7.5 landscape this is not a
click: it arrives as a support package, which means your inventory depends on a basis maintenance
window and on its calendar, not yours.

The second is an admission SAP deserves credit for, because it is precisely the one that prevents
a false sense of safety. Verbatim:

> "Please note that the above report does not provide conclusive results of the non-existence of
> unpermitted calls to the ODP-RFC interface."

The report can tell you it **found** unpermitted calls. It cannot tell you there **are none**. A
green dashboard there is not evidence of compliance; it is evidence that nothing showed up in the
observed window. And because ODP-RFC is client-dependent, you have to run it in every relevant
client of every system, not once per landscape.

It is, once again, the failure mode I wrote about in edition 10: the system does not stop you. It
hands you green.

## Four doors and their toll

If today you need to move data out of an ABAP system —ECC or S/4HANA— toward a platform that is
not SAP's, the legitimate options fit on one hand. They are worth seeing side by side, because
most projects pick the first one they were shown.

**1. SAP Datasphere with Premium Outbound Integration.** This is the door this client took. A
*replication flow* reads from the source —in our case the container is literally called
`CDS_EXTRACTION`, the CDS views enabled for extraction— and writes to external storage. You pay by
outbound volume.

**2. The ODP OData API.** The same ODP layer, but through its REST interface instead of RFC. It is
one of only two alternatives note 3255746 names explicitly. It works well for moderate volumes and
for transactional integration; for loading an entire lake, throughput is a different conversation.

**3. A certified partner connector, with Open Mirroring.** *Open Mirroring* is the set of native
Fabric APIs that let a third party keep a synchronised copy inside OneLake. Microsoft lists five
SAP-certified solutions for this route —DAB, ASAPIO, Theobald, Simplement and SNP Glue. You trade
SAP's toll for a software licence, and extraction leans on permitted interfaces instead of
ODP-RFC.

**4. SAP Business Data Cloud.** The other route the note names, with a *zero-copy* architecture
—sharing data without duplicating it. It is SAP's strategic bet and deserves its own analysis; I
covered it in edition 08.

There is a detail that gets overlooked and that holds up this entire edition's argument: **note
3255746 does not mention Datasphere among the alternatives.** That is not an oversight. Datasphere
does not appear as an alternative because it is not an alternative *for you*: it is an SAP
application, and its traffic is therefore permitted by definition. The prohibition was never about
the protocol. It was about who is standing on the other end of the cable.

All four doors are defensible. What is not defensible is arriving at the fourth design meeting
without having written down **why** one was chosen. Because each one's toll is different, and two
of them charge it on a recurring basis.

## The meter

This is where the business case usually breaks, and the mechanics are in SAP's public
documentation.

To use **any non-SAP target** in a Datasphere replication flow —Azure Data Lake Storage Gen2,
Amazon S3, Google Cloud Storage, BigQuery, Kafka, SFTP— you need **Premium Outbound Integration**,
and your administrator has to allocate at least one block. The unit is explicit:

> "Each block gives you 20 GB of data volume for transfer."

One block, 20 GB, per month. Microsoft confirms it from the destination side, on its SAP mirroring
page: *"SAP Datasphere Premium Outbound Integration pricing applies when mirroring SAP data via
SAP Datasphere."*

And now the line that in my judgement belongs on the first slide of any migration plan of this
kind. It is SAP's, verbatim, on what happens when you go past your allocated volume:

> "If you exceed the assigned volume, your data integration processes (such as replication flow
> runs) continues running to avoid interrupting critical integration scenarios, which can result
> in additional costs (depending on your plan)."

Read it again. **The meter has no shut-off.** And it is well designed that way: cutting a
company's integration in the middle of a month-end close would be worse. But it means the cost of
leaving is **recurring, variable and technically uncapped**, and the only protection is
organisational: somebody has to be watching consumption.

There is a second-order consequence almost nobody models. **This cost grows with the success of
the project.** Every new use case in Fabric, every table someone asks for "just in case", every
history reload because a rule changed, crosses the door and gets charged. In BW, serving one more
report cost effectively zero at the margin. In this architecture, it does not.

Looked at squarely, that is not only a risk: it is also a healthy incentive. It is the first time
in my career that extraction design carries a **direct, visible price**. Extracting what is used,
at the grain it is used, stopped being an engineering best practice and became a budget line.
Teams already working that way will not notice the change. Teams that extracted whole tables "so
everything is available" will notice it on the third month's invoice.

## Datasphere as a customs house, not a warehouse

This is the reframe I want to leave behind, and the one I find most useful for anyone designing
something similar.

In this architecture, **Datasphere is not the data warehouse. It is the customs house.** It is the
transit layer where data proves it is allowed to leave, pays its duty, and moves on. It is not
where you model, not where you govern meaning, not where you report from. All of that lives on the
other side, in Fabric and the lake.

Saying it that way has two practical consequences.

First: **a customs house is a system in operation, not a passive component.** It has monitoring,
load windows, outages, an owner. On the diagram it is an arrow; in reality it is one more system
somebody is on call for. If the org chart of your new platform has nobody sitting there, you will
find out on the first Monday of a close.

The second is more uncomfortable: **you have to decide explicitly that the customs house will not
grow.** The default behaviour of any organisation that has already bought a tool is to start using
it. Somebody will propose "since we already have Datasphere, let's model this dimension here." Six
months later you have two semantic layers, each half-built, and the governance conversation you
thought you closed when you chose Fabric reopens, now with two owners. If you pick this
architecture, the discipline of keeping the customs house a customs house is a decision you write
down, communicate and defend. It does not hold on its own.

## The second toll: what does not travel

The toll nobody talks about is not charged in gigabytes. It is charged in person-months.

**A replication flow moves rows. It does not move meaning.** Part of the meaning does cross, and
that is why choosing CDS views as the extraction point is right: a CDS view already carries the
ERP's business context —the joins, the filters, the descriptions, the logic of what counts as an
open order. That is exactly what you do not have when you read raw tables.

But the other context, the one that lived in BW, does not travel. Twenty years of calculated and
restricted key figures, hierarchies, consolidation rules, analytical authorisations. None of that
is in the CDS view, and none of it fits in a Parquet file. Somebody has to write it again on the
other side.

In this case **the business rules were rebuilt by hand, and in many cases they were not fully
documented.** I want to be precise about what that means, because it sounds like a documentation
problem and it is something else: much of that work was not migration, it was **archaeology**.
Open the old query, read the formula, find whoever remembers why certain document types were
excluded back in 2014, and decide whether that rule is still correct or merely still alive.

And here is a clock almost nobody watches. **BW 7.5 has mainstream maintenance until the end of
2027 and extended maintenance until 2030.** While that system is still switched on, the
undocumented rules can still be read: they are in the queries, in the transformations, in the
heads of the people who maintain them. The day it is switched off, whatever was not written down
stops being recoverable. The window to do that archaeology with a safety net is finite, and it is
closing in parallel with the migration, not after it.

## What I would ask of a business case

Five concrete things. The first three are for whoever signs the contract, not for whoever runs the
technical team.

- **That egress is modelled as a recurring and growing expense, not a project cost.** With the
  figure from SAP's capacity estimator and at least three scenarios: year 1, year 3, and the year
  80% of your reports already live on the new platform. The right question is not how many GB
  cross today; it is how many will cross once the project has succeeded.
- **That the meter has an alarm and a named owner.** SAP has written down that it does not cut
  off. So the protection has to exist on your side: threshold, alert, and a person accountable for
  it.
- **That the choice of door is written down, with its reasoning.** Which of the four, why, and
  what happens if SAP moves the line again. It is a two-paragraph annex that saves you a six-month
  argument.
- **That the ODP-RFC self-assessment is installed this quarter, not next.** Do not ask for it as a
  compliance task; ask for it because it is the only way the inventory will **exist** — the report
  does not look backwards. And ask for it with the caveat attached: green there means "I saw
  nothing in the observed window", not "there is nothing". The temporary valve expires at the end
  of 2026 and SAP has already written that afterwards it is enforced *without exception*. If you
  have old integrations pointing at that interface, they will not degrade. They will stop.
- **That the reconstruction of business rules appears with a name, an estimate and a calendar**,
  and that it runs **while the source system is still switched on**. It is not a closing task. It
  is the task that depends most on the old system still existing.

I say this from a region where it is routine, not hypothesis. A large share of the operations of
the multinationals based in northeastern Mexico runs on SAP, and many of them are deciding right
now where their analytics will live. In those conversations, the exit door gets treated as an
implementation detail to be sorted out after signing. It is exactly the other way around: it is
one of the few decisions you negotiate well once, at the start, and pay for every month if you
negotiate it badly.

## True north

I think this client's architecture is right. CDS views as the extraction contract, a single
landing format, an open lake on the other side, and an analytics platform they chose for their own
reasons rather than vendor inertia. I would sign that design again.

What changed is not the design. It is that **"we're leaving SAP on the analytics side" stopped
being a platform decision.** It is a decision about who owns the door your data will pass through
for the next ten years, what they charge to open it, and how much of the meaning stays on this
side when the data crosses.

If you are about to enter this discussion, there is one question that orders all the others, and
it is not technical: **how many gigabytes a month will cross your customs house in the year the
project has actually worked?** If nobody in the room can answer it, you do not have a business
case yet. You have a tool preference.

---

### Sources

- Microsoft Learn — *Microsoft Fabric Mirrored Databases From SAP* (the two-step process:
  Datasphere replication flow → ADLS Gen2 container → mirroring engine → OneLake; and "SAP
  Datasphere Premium Outbound Integration pricing applies when mirroring SAP data via SAP
  Datasphere"): https://learn.microsoft.com/en-us/fabric/mirroring/sap
- Microsoft Learn — *Tutorial: Configure Microsoft Fabric Mirrored Databases to Mirror SAP via SAP
  Datasphere* (Premium Outbound Integration as a prerequisite; `CDS_EXTRACTION` source container;
  Parquet target with *Group Delta* set to *None*; load types *Initial and Delta* or *Initial
  Only*): https://learn.microsoft.com/en-us/fabric/mirroring/sap-datasphere-tutorial
- Microsoft Learn — *Extract SAP data to Microsoft Fabric* (the licensing-entitlements warning
  ahead of any extraction; the SAP CDC connector note pointing to SAP Note 3255746; the
  connectivity options table; SAP-certified partners for Open Mirroring: DAB, ASAPIO, Theobald,
  Simplement, SNP Glue): https://learn.microsoft.com/en-us/azure/sap/workloads/extract-sap-data
- SAP Help / SAP-docs — *Premium Outbound Integration* (required for every non-SAP target: ADLS
  Gen2, Amazon S3, Google Cloud Storage, BigQuery, Kafka, Confluent, SFTP; one block per 20 GB):
  https://help.sap.com/docs/sap_datasphere/c8a54ee704e94e15926551293243fd1d/4e9c6acb5d6a43fa9a6471837399e71c.html
- SAP Help / SAP-docs — *Configure the Size of Your SAP Datasphere Tenant* ("Each block gives you
  20 GB of data volume for transfer", and the verbatim note that exceeding the volume lets
  processes keep running at additional cost):
  https://github.com/SAP-docs/sap-datasphere/blob/main/docs/Administering/Creating-and-Configuring-Your-Tenant/configure-the-size-of-your-sap-datasphere-tenant-33f8ef4.md
- SAP KBA **3456481** — *Replication Flow - There is no outbound volume available for this month*
  (the error raised when no POI blocks are allocated):
  https://userapps.support.sap.com/sap/support/knowledge/en/3456481
- SAP Note **3255746** — *Unpermitted usage of ODP Data Replication APIs*, **version 12, released
  9 June 2026** (component BC-BW-ODP). Prohibition on ODP-RFC use by the customer or third-party
  applications against ABAP systems containing PI\_BASIS, SAP BW or SAP BW/4HANA, on-premise or
  private cloud; SAP's reservation to modify the modules without prior notice; customer liability
  for incidents; named alternatives: SAP Business Data Cloud and the ODP OData API.
- SAP Note **3748819** — June 2026 Patch Day security note, validating incoming calls against
  permitted subscriber types and blocking unpermitted ones. Code corrections in SAP Note **3635619**.
- SAP Note **3731818** — *Temporary suspension for automated assessment of subscriber types*,
  **version 4, released 27 July 2026**. Report `RODPS_REPL_SECUREACCESS_OPTOUT`; temporary
  exception at the customer's own risk; expires end of 2026, enforced *without exception*
  thereafter.
- SAP Note **3439624** — *Self-Assessment for data access to ODP Data Replication APIs*,
  **version 34, released 9 September 2026**. Report `RODPS_REPL_SUBSCRIBER_ASSESS`; four
  assessment states; no assessment of historical calls; client-dependent; and the verbatim caveat
  that the report "does not provide conclusive results of the non-existence of unpermitted calls".
  Delivered for SAP BW 7.50 via Support Package 36.

  *(All four notes were consulted directly in SAP for Me on 9 September 2026; copies in
  `notas_sap/`.)*
- SAP Community — *SAP NetWeaver 7.5 Maintenance Strategy* (mainstream maintenance for NetWeaver
  7.5 and BW 7.5 through the end of 2027; extended maintenance through 2030):
  https://pages.community.sap.com/topics/abap/netweaver-maintenance-strategy
- Microsoft Fabric — FabCon 2026 announcement: mirroring for SAP via SAP Datasphere generally
  available.
