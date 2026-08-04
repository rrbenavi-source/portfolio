---
title: AI already writes near-perfect SQL. Whose semantics is it using?
subtitle: The benchmark that moved the bottleneck from the model to the modeling
format: opinion
date: 2026-08-04
---

There's a number that has been circulating for a few months and still hasn't
landed in how companies are buying their data copilots. In April, dbt Labs
published the 2026 update of its text-to-SQL benchmark: frontier models, working
alone against the database, get 84–90% of analytical questions right. The same
models, answering on top of a well-modeled semantic layer, climb to 98.2% and
even 100%.

Read that twice, because it closes a debate that ran for years. The model that
"couldn't write SQL" barely exists anymore: Claude Sonnet 4.6 went from 90.0 to
98.2; GPT-5.3 Codex, from 84.1 to 100. What separates a demo copilot from a
production one is no longer the model. It's whether someone modeled the semantics
it answers on.

That's the debate that closed. The one that opens is more uncomfortable: who does
the modeling?

## 90% sounds high until you put it in operation

On an executive dashboard answering a hundred questions a day, 90% accuracy means
ten wrong numbers daily — served with the same confidence as the right ones.
Nobody who has ever signed off on a financial close accepts that rate. The jump
from 90 to 98–100 isn't incremental; it's the difference between an impressive
demo and something you can put in front of a CFO.

And there's a detail in the benchmark more revealing than the headline figure:
the two approaches don't fail the same way. When text-to-SQL gets it wrong, it
tends to return a plausible, incorrect number — with full confidence. When the
semantic layer can't answer, it says so: explicit error, out of scope. One lies
to you confidently; the other tells you it doesn't know. In an environment where
someone signs off on the number before it reaches an executive — which is how any
serious platform should operate — that difference is worth more than the accuracy
points. A visible error gets fixed; a plausible false number travels.

## The fine print: semantics can't be downloaded

The benchmark has an honesty worth acknowledging. To make pure text-to-SQL
competitive, the authors loaded the entire database schema as model context —
and they themselves warn this isn't practical for larger datasets. Now think
about that from a SAP operation: thousands of tables, names like VBAK, VBAP,
KONV, logic scattered across extractors and user routines. No context window can
hold that, and even if one could, the schema doesn't contain what matters. The
schema tells you a field exists; it doesn't tell you why in 2019 someone decided
that returns from a certain channel get netted differently.

It's also fair to state the size of the test: eleven questions, twenty runs per
configuration, on a semi-complex insurance dataset. That is not the scale of a
real operation. But the direction of the result is consistent with what anyone
who operates data platforms has seen firsthand: semantic grounding isn't a
luxury — it's the condition for a number being defensible.

And that's the full fine print: the semantic layer that produces that jump can't
be downloaded. It has to be built. Someone had to sit down and define what "net
sales" means, which exchange rate it converts against, which channel it includes
and which it excludes, at what moment an order becomes a sale. The model doesn't
contribute that semantics. It consumes it.

## In a SAP shop, the semantics already exists. That's exactly the problem

This is where the benchmark lands on my turf. In a twenty-year SAP operation,
that semantic layer is already defined — with a precision any modern semantic
layer would envy. Every business rule has been through audits, closes, and users
who push back when the number doesn't reconcile. The catch is where it lives:
buried in extractors, in user exits, in the thousand lines of a Z report that
calculates "net sales" in a way no document describes.

A few weeks ago I wrote that migrating a Z report isn't translating ABAP — it's
an autopsy. Business logic doesn't live in the code; it lives in the accumulated
decisions the code crystallized. The dbt benchmark puts a number on that thesis.
If semantic grounding is worth 8 to 16 accuracy points — plus the difference
between lying confidently and admitting you don't know — then the autopsy of your
SAP layer isn't technical debt. It's the asset that decides whether your data
copilot tells the truth.

## The buying mistake that's coming

A wave of projects is coming that will buy the copilot and skip the modeling. The
pitch is irresistible: connect it to the warehouse and ask in natural language.
And it will work — in the demo, with the easy questions, on the clean tables. In
production, the CFO's question isn't easy: it crosses channel, price segment,
currency, and an adjustment that only exists because someone decided it seven
years ago and no longer works at the company.

The right sequence is the boring one. First, extract the semantics from where it
lives — and in industrial operations in this part of the world, it lives in SAP.
Then model it into a layer the model can consume: metrics defined once, governed,
with an owner. And at the end — only at the end — connect the copilot. It's the
same order the benchmark implies and that twenty years of data discipline
confirm: the ceiling is set by the source, not the destination.

## The cheap test before you buy

Before evaluating any data copilot, run a test that costs no licenses: take your
three most contested metrics and ask two business people to define them in
writing. If the definitions don't match — and in my experience, they don't — your
next step isn't the copilot. It's the modeling. The copilot will only answer,
with great confidence, the version of the metric nobody agreed on.

---

**Sources:**
- Ganz, J. & Perigaud, B. (dbt Labs) — *Semantic Layer vs. Text-to-SQL: 2026
  Benchmark Update*, Apr 7, 2026. Figures, methodology (11 questions × 20 runs,
  ACME Insurance dataset) and the schema-as-context caveat.
  https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- Solid — *Text2SQL vs. Semantic Layer? The real question is who does the
  modeling*. The same argument from the modeling angle.
  https://journey.getsolid.ai/p/text2sql-vs-semantic-layer-the-real
- Atlan — *Text-to-SQL for Enterprise: Metric Drift and Context Layer* (2026).
  Metric drift and context layers in enterprise environments.
  https://atlan.com/know/ai-agent/data-for-ai/text-to-sql-for-enterprise/
