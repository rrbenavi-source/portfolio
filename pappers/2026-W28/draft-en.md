---
title: Your semantic layer decides whether your data agents tell the truth
subtitle: Reliable generative BI is won in the context, not in the model
format: deep-dive
date: 2026-07-06
---

## There are two ways to fail, and one is far worse

A director asks: "how much did we sell to new customers last quarter?" The assistant
can fail in two ways. It can return an error. Or it can return a number that looks
flawless and is wrong.

The first is an inconvenience. The second ends up on a board slide and nudges a
decision in the wrong direction. And that is exactly how text-to-SQL fails when you
turn it loose on a real data warehouse with no context.

This is the point that gets lost in the generative-BI conversation: the problem is
almost never the language model. The model gets better every quarter and cheaper on
its own. What decides whether you can trust the answer is the context —what each
metric means, which table is the right one, which business rule applies— and the model
doesn't supply that context. You do, in the semantic layer.

## What the numbers say

dbt Labs' 2026 benchmark is the clearest read I've seen on this, and it puts two things
on the table.

First: text-to-SQL got dramatically better. Across the full question set it went from
32.7% to 64.5% accuracy —nearly double in one model generation. Anyone who declared
"this doesn't work" two years ago needs to revisit that stance.

Second —and this reframes everything—: for questions that fall within the scope of a
well-modeled semantic layer, accuracy approaches or hits 100%. Not because the model is
smarter, but because query generation becomes deterministic: if the metrics and
dimensions are already defined, the model can't slip in a subtly wrong result.

Keep the floor in mind. With no context layer at all, various cited measurements put
baseline text-to-SQL accuracy somewhere around 21-25%. From there, 64.5% with good
prompting is a huge jump; ~100% inside a semantic model is a different category
altogether.

And still, the percentage isn't what matters most. What matters most is how each one
fails. The semantic layer, when it can't answer, tells you so. Text-to-SQL hands you a
plausible, wrong answer without blinking. For loose exploration, that flexibility is
welcome. For a number headed to an auditor, an OKR, or a company KPI, the difference
between "I can't answer that" and a made-up figure wearing the face of truth is
everything.

## What a semantic layer actually does

Let's get concrete, because "semantic layer" sounds like jargon and is really a simple
idea.

It's a translation layer: it turns a cryptic, undocumented production schema into a
clean, documented, business-friendly interface the AI can reason over reliably. Instead
of exposing `raw_transactions` with twenty vaguely named columns, you expose a
`net_revenue` view that declares what it measures and which rules it applies.

The part most people underrate: the business logic lives in the view definition, not in
the model's head. If the net-revenue view already carries
`WHERE refund_flag = 0 AND test_account = 0`, every query that flows through it inherits
that rule automatically. The agent doesn't have to know it, remember it, or infer it.
The SQL engine enforces it —not the model's goodwill.

Dremio puts it bluntly: the semantic layer solves the most common, highest-impact class
of errors —wrong table, wrong column, missing business rule— which affect 80% of business
queries and are the ones most likely to produce numbers that end up in real decisions. It
doesn't solve everything. It solves the 80% that hurts most.

## Why the industry stopped talking about models and started talking about context

It's no accident that Databricks' most-discussed announcement this season isn't a model
but Genie Ontology: a live context layer that encodes how the business defines its own
metrics and terms, not just the data it connects. Genie stopped being a chat assistant and
started leaning on a business ontology —and moved into where people already work: Teams,
Microsoft 365 Copilot, Excel.

The asset Databricks is putting at the center isn't the ability to generate SQL. It's the
governed context that makes that SQL trustworthy. A data product without that context is a
GPS with no destination: it gets you somewhere fast, wherever that is. The model is a
commodity; the semantic layer is the moat.

## What this means if your world is SAP

Here the conversation gets personal for those of us who've spent years working with SAP and
are now looking to bring that data into a lakehouse.

When we integrated SAP with Databricks, the part that generated the most value wasn't the
pipeline. Moving data is a solved problem. The value was in the slow, unglamorous work of
defining what each metric means —what exactly counts as a "new customer," what does and
doesn't belong in "net sales"— and keeping that definition governed in one place.

At the time it felt like debt we paid so reports would stay consistent. Seen from 2026 it
was something else: without knowing it, we were building the semantic layer that now makes
any agent we query on top of it trustworthy.

## How to start without boiling the ocean

The temptation, once you realize the semantic layer is the asset, is to model everything.
That's the surest way to never finish.

The path Dremio recommends —and the one that works in practice— is to start narrow. Take the
five metrics your business asks about most often. Build documented, tested views for each.
Run the agent against those five and validate the outputs against historical values you
already know. Once they're reliable, add five more. The semantic layer grows in increments,
and so does the territory where you can trust an agent to do the work.

It isn't glamorous. It's exactly the kind of work the AI hype tempted us to skip —and exactly
the work that decides whether your data assistant is a trustworthy tool or a very articulate
generator of wrong numbers.

## The close

If you're investing in generative BI this year, the question isn't which model you pick. The
good ones are here, they resemble each other, and they keep getting cheaper. The question is
how much of your business is encoded in a governed semantic layer —because that share, not the
model, is the ceiling on what your agents can answer without lying to you.

Start with five metrics. Model them well. Validate against history. The rest is patience.

## Sources

- dbt Labs — _Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update_. https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026
- Dremio (Alex Merced) — _Semantic Layer for AI Agents: Stop Getting the Numbers Wrong_. https://www.dremio.com/blog/semantic-layer-for-ai-agents-stop-getting-the-numbers-wrong/
- Databricks — _Introducing Genie One, Genie Ontology, and Genie Agents_. https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents
- Analysis of Snowflake Cortex Sense (baseline text-to-SQL without context, ~21-25%). https://dev.to/albertomontagnese/text-to-sql-is-still-brittle-snowflakes-cortex-sense-is-a-new-take-2ahj
