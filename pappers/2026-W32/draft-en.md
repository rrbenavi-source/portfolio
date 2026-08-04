---
title: AI already writes near-perfect SQL. Whose semantics is it using?
subtitle: Three years of the same exam, and the lesson vendors have already conceded
format: opinion
date: 2026-08-04
---

There's a number that has been circulating for a few months and still hasn't
landed in how companies are buying their data copilots — the AI/BI Genie or
Copilot-style assistants that answer business questions in natural language by
generating SQL over your data. In April, dbt Labs
published the 2026 update of its text-to-SQL benchmark: today's most advanced AI
models — they tested Claude Sonnet 4.6 and GPT-5.3 Codex — working alone against
the database, get 84–90% of analytical questions right. The same
models, answering on top of a well-modeled semantic layer, climb to 98.2% and
even 100%.

Read that twice, because it closes a years-long debate. What separates a copilot
that impresses in the demo from one you can put in production is no longer the
model. It's whether someone modeled the semantics it answers on. Which opens the uncomfortable question this
piece wants to develop: who does the modeling — and where does that semantics
come from?

## Three years, same exam

To understand why this result matters, go back to the origin. In November 2023,
Juan Sequeda, Dean Allemang and Bryon Jacob published the study that started
this discussion: 43 business questions over an enterprise insurance schema — the
now well-known ACME dataset. GPT-4, working directly against the SQL, answered
**16.7%** correctly. With a knowledge representation on top — ontology,
mappings, business context — it climbed to **54.2%**. Three times better, and
still a failing grade.

The 2026 dbt benchmark runs on that same dataset — same terrain, different
grounding tool: a knowledge graph then, a semantic layer now — with a subset of
11 questions and 20 runs per configuration. Putting the two moments side by side
tells the whole story:

- **2023:** raw 16.7% → grounded 54.2%
- **2026:** raw 84–90% → grounded 98–100%

(Over the full question set, dbt reports a lower raw aggregate: 64.5%. The
figures above are for the two models named, on the subset.)

What improved over three years is the model — from failing to solid. What didn't
change is who wins: in both moments, semantic grounding takes the difference.
And notice where that difference lives now: no longer 37 points in the middle of
the scale, but 8 to 16 points at the top — exactly the points that separate
"impressive" from "trustworthy". The last points are always the expensive ones.

## 90% sounds high until you put it in operation

On an executive dashboard answering a hundred questions a day, 90% accuracy
means ten wrong numbers daily — served with the same confidence as the right
ones. Nobody who has ever signed off on a financial close accepts that rate.

And there's a detail in the benchmark more revealing than the headline figure:
the two approaches don't fail the same way. When text-to-SQL gets it wrong, it
tends to return a plausible, incorrect number — with full confidence. When the
semantic layer can't answer, it says so: explicit error, out of scope. One lies
to you confidently; the other tells you it doesn't know. In an environment where
someone signs off on the number before it reaches an executive, that difference
is worth more than the accuracy points. A visible error gets fixed; a plausible
false number travels.

## The real exam is even harder

Here it pays to be honest about scale, because the ACME dataset is a controlled
experiment: eleven questions, one semi-complex insurance schema. Academia has
already measured what happens when the exam looks like a real company.

A quick introduction to the three examiners. **Spider 1.0** (Yale, 2018) is the
classic academic benchmark: self-contained questions over small, clean databases
— the exam models have already mastered. **BIRD** (2023) raised the difficulty:
larger databases, dirty data, and questions that require business knowledge, not
just the schema. And **Spider 2.0** (2024) is the enterprise exam: 632 problems
derived from real use cases, databases with over a thousand columns on BigQuery
and Snowflake, multiple SQL dialects, chained transformations — the kind of work
a data team does on any given Tuesday.

When Spider 2.0 came out in late 2024, the best model of the moment — one that
scored 91.2% on Spider 1.0 and 73% on BIRD — solved roughly **20%**. Today, the
best models hover around **70%** on Spider 2.0-AIFunc, the benchmark's 2026 enterprise
extension — a different task set, not the original exam. Seventy, not
ninety-eight.

The obvious reading is that raw text-to-SQL at real enterprise scale remains far
from production — the headline 90% is earned in the lab, not in your warehouse.
But the interesting reading is the other one: the 98–100% on ACME shows what
curation buys *within a bounded scope*. The path to production isn't waiting for
a bigger model to master the chaos; it's shrinking the chaos with semantics
until the model operates in a space where it can actually be trusted.

## The fine print: semantics can't be downloaded

The dbt benchmark has an honesty worth acknowledging. To make pure text-to-SQL
competitive, the authors loaded the entire database schema as model context —
and they themselves warn this isn't practical for larger datasets. Now think
about that from a SAP operation: thousands of tables, names like VBAK, VBAP,
KONV, logic scattered across extractors and user routines. No context window can
hold that, and even if one could, the schema doesn't contain what matters: it
tells you a field exists, not which business rule fills it.

And that's the full fine print: the semantic layer that produces the jump can't
be downloaded. It has to be built. Someone had to sit down and define what "net
sales" means, which exchange rate it converts against, which channel it includes
and which it excludes, at what moment an order becomes a sale. The model doesn't
contribute that semantics. It consumes it.

## The vendors have already voted

If there's any doubt where this is heading, look at what every platform is
building. dbt has its Semantic Layer with MetricFlow. Snowflake shipped Semantic
Views. Databricks brought Metric Views into Unity Catalog, the foundation of
what it calls Business Semantics, GA since April of this year. GA — general
availability — is the mark of a finished, supported product with a contract
behind it; the opposite of preview, which means "try it, but don't bet a project
on it". And at the Data + AI Summit it introduced Genie Ontology: a context
layer that learns from usage to feed Genie, still in preview. When every vendor
converges on the same piece, it stops being a feature and becomes a confession:
the model, alone, is not enough. It needs a curated layer of meaning — and every
platform wants to own that layer.

I see this in operation daily. The difference between a Genie space with curated
metrics and well-crafted instructions, and one wired straight to the tables, is
not subtle: it's the difference between answers the business uses and answers
the business stops consulting by the second week.

## SAP voted too — and there's the catch for those of us who live in that world

SAP understood the same thing, and its play is Business Data Cloud: managed data
products that travel "with their business context and semantics intact",
including semantic metadata sync into Unity Catalog via Delta Sharing, now GA
under the SAP–Databricks partnership. On paper, it's exactly the right answer:
let the semantics travel with the data.

But read closely *which* semantics travels. What BDC packages is the semantics
of the standard content — the domain model SAP defines and maintains. The
semantics of *your* operation is something else: it lives in modified
extractors, in user exits, in the thousand lines of the Z report that calculates
"net sales" in a way no document describes. A few weeks ago I wrote that
migrating a Z report is an autopsy, not a translation; this is the underlying
reason. Twenty years of business decisions crystallized in custom code don't
ship in any standard data product. That layer — the one that actually decides
whether your copilot tells the truth — nobody can sell it to you. It gets
extracted, documented and modeled. With work.

## The buying mistake that's coming

A wave of projects is coming that will buy the copilot and skip the modeling.
The pitch is irresistible: connect it to the warehouse and ask in natural
language. And it will work — in the demo, with the easy questions, on the clean
tables. In production, the CFO's question isn't easy: it crosses channel, price
segment, currency, and an adjustment that only exists because someone decided it
seven years ago and no longer works at the company.

The right sequence is the boring one. First, extract the semantics from where it
lives — and in industrial operations in this part of the world, it lives in SAP.
Then model it into a layer the model can consume: metrics defined once,
governed, with an owner — Metric Views, MetricFlow, whichever flavor your stack
speaks. And at the end — only at the end — connect the copilot. It's the order
three years of benchmarks imply and twenty years of data discipline confirm: the
ceiling is set by the source, not the destination.

## The cheap test before you buy

Before evaluating any data copilot, run a test that costs no licenses: take your
three most contested metrics and ask two business people to define them in
writing. If the definitions don't match — and in my experience, they don't —
your next step isn't the copilot. It's the modeling. The copilot will only
answer, with great confidence, the version of the metric nobody agreed on.

---

**Sources:**
- Ganz, J. & Perigaud, B. (dbt Labs) — *Semantic Layer vs. Text-to-SQL: 2026
  Benchmark Update*, Apr 7, 2026. 2026 figures, methodology (11 questions × 20
  runs, ACME dataset) and the schema-as-context caveat.
  https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- Sequeda, J., Allemang, D. & Jacob, B. — *A Benchmark to Understand the Role of
  Knowledge Graphs on LLM's Accuracy for Question Answering on Enterprise SQL
  Databases*, Nov 2023. The origin: 16.7% vs 54.2% over 43 questions.
  https://arxiv.org/abs/2311.07509
- Lei et al. — *Spider 2.0: Evaluating Language Models on Real-World Enterprise
  Text-to-SQL Workflows* (ICLR 2025). 632 real problems; 21.3% (o1-preview) vs
  91.2% on Spider 1.0. https://arxiv.org/abs/2411.07763
- *Spider 2.0-AIFunc: Extending Real-World Text-to-SQL to AI-Native SQL
  Workflows* (2026). Frontier proprietary models cluster at 67–70.3%.
  https://arxiv.org/abs/2607.06229
- Databricks — *What's new with Unity Catalog at Data + AI Summit 2026* (Metric
  Views, Business Semantics, Genie Ontology).
  https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026
- Databricks — *Unlocking SAP business context in Databricks with semantic
  metadata Delta Sharing* (GA of the SAP BDC → Unity Catalog semantic sync).
  https://www.databricks.com/blog/unlocking-sap-business-context-databricks-semantic-metadata-delta-sharing
- Solid — *Text2SQL vs. Semantic Layer? The real question is who does the
  modeling*. https://journey.getsolid.ai/p/text2sql-vs-semantic-layer-the-real
- Atlan — *Text-to-SQL for Enterprise: Metric Drift and Context Layer* (2026).
  https://atlan.com/know/ai-agent/data-for-ai/text-to-sql-for-enterprise/
