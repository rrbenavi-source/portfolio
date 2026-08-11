---
title: Automating the pipeline is not automating the business rules
subtitle: The first agent benchmark on real pipelines says exactly where they break
format: opinion
date: 2026-08-11
---

In April 2025, three researchers at the University of Illinois published the first
serious exam for a question many of us had been asking under our breath: can an AI
agent — a model that doesn't just answer, but runs commands, writes files and fixes
its own mistakes — build a complete data pipeline, end to end?

The exam is called ELT-Bench, after the three stages of a pipeline — the chain that
moves data from the source system to the report: **extract** (pull it from the
source), **load** (land it in the warehouse) and **transform** (turn it into the
business tables someone actually decides with). These aren't toy exercises: 100
pipelines, 835 source tables and 203 data models, each with its calculation rule
inside. The agent connects to the sources, reads documentation, writes code and SQL,
and orchestrates every stage.

The best agent in that run — Spider-Agent with Claude 3.7 Sonnet and extended
thinking — scored **57% on extract and load**. And **3.9% on transform**.

That contrast is the whole argument. But here's something almost nobody says when
citing an AI study: that was sixteen months ago, and in this field sixteen months is
an era.

## A year later, half the problem is gone

In April 2026, a team from IBM Research and ETH Zurich re-ran the exam with current
models and published ELT-Bench-Verified. The new numbers:

| Stage | Apr 2025 (Claude 3.7 Sonnet) | Apr 2026 (Claude Sonnet 4.5) |
|---|---|---|
| Extract and load | 57% | **96 – 98%** |
| Transform | 3.9% | **32.5%** |

The range isn't uncertainty: it's two different agents on the same model, and the
simpler one scored 98%.

Connecting to the source, authenticating, landing the data in the warehouse: that
**got solved**. It went from failing four times out of ten to failing once in thirty.
It's a controlled exam, not your operation — real sources are dirtier — but the trend
is unambiguous. If your job, or your vendor's, consists of building and maintaining
those connections, better to find out from a study than from a contract renewal.

Transform improved too, and a lot: it multiplied by eight. But it still fails **two
times out of three**.

Watch the order, not just the numbers: the gap closes **from the bottom up**, the
mechanical first and the semantic last. And that's no accident.

AI is extraordinary with anything written down somewhere in the world, and useless
with anything that was never written. How to authenticate against the Salesforce API
is documented in a thousand tutorials. What a net sale means at your company — which
discounts count, which returns get subtracted, at what point in the fiscal calendar
it's recognized, why those three legal entities don't consolidate the same way — **is
written nowhere**. It lives in three people's heads and in a 2009 user exit: custom
code grafted onto the SAP standard.

## The number that changes the question

This is where the 2026 study stops talking about AI and starts talking about us.

Before publishing, the team audited **why** the agents failed at transform. They
reviewed the 81 failed tasks by hand, expecting model errors. They found something
else.

Of the column-level mismatches, **a third weren't agent errors: they were errors in
the exam.** Evaluation false positives, ambiguous descriptions, and ground truth —
the answer you're graded against — that was simply wrong. 82.7% of those failed tasks
had a problem of this kind.

The 32.5% in the table is, in fact, already the corrected number. Under the original
grading, that same agent scored 22.66%. Nearly ten points that didn't come from the
model: they came from the exam's own mistakes.

And the detail that stopped me cold: 30 columns — 1.2% of the total — had to be
**removed from the exam** because the team couldn't establish the correct answer. The
reason? Interpreting the same specification, the experts **agreed only 57.8% of the
time**.

Read that again. Experts. With the written definition in front of them. Agreeing on
what a column means barely more than half the time.

That number reframes the problem. Transform doesn't resist because the model is
limited. It resists because **the business rule was never written unambiguously** —
and when you force expert people to write it down, you discover they don't agree
among themselves either. The bottleneck isn't the machine that executes: it's the
definition nobody closed.

If that happens in an academic benchmark — a test built specifically to be evaluable
— with people paid to be precise: what odds do you give "get me net sales for the
month", said in a meeting, against a data model nobody documented?

## Where this lives in an SAP operation

If you work on SAP, you already know exactly where your 32.5% is.

It's in the extractor — the program that pulls the data out of the system — that
someone patched in 2011 to exclude three document types, without leaving a comment.
It's in the user exit that rewrites the profit center under a condition only its
author knows. It's in the Z report management uses every month that produces a
different number than the official dashboard, and in the answer we all accept:
*"that report just calculates differently."*

That's your transformation layer. It isn't in the pipeline: it's buried in twenty
years of correct decisions, made by competent people who solved a real problem on a
Tuesday and didn't have time to document it.

No automated migration tool is going to extract that, because it isn't code: it's
intent. The tool translates what the code *does*; the question that decides your
project is why it does it.

## The bill that's piling up

Meanwhile, data teams are using AI exactly backwards from what would serve them.

dbt Labs' *State of Analytics Engineering 2026* — 363 data professionals and leaders
— found that **72% prioritize AI for writing code**, and only **24% prioritize it for
managing the pipeline**: testing, observability, quality control. Creation is being
prioritized three times more than control.

In the same report, **71%** worry about incorrect or hallucinated outputs — numbers
the model invents and delivers with complete confidence — reaching the stakeholders
who will decide with them. And **77%** of leaders report pushing their teams to ship
faster with AI. Seven in ten fear the consequence that nearly eight in ten leaders
are accelerating.

Nobody is buying speed. They're buying volume with no checkpoint: with no one
reviewing before the number goes out.

## Where it does pay off

None of this is an argument against AI. I use it every day: this newsletter and the
portfolio it's published on are built with it. The argument is about **where** to put
it.

There are three jobs where AI genuinely pays off for a data architect:

**Completing specifications.** Taking a spec from 60% to 95%, because the model asks
about the edge cases you no longer see, precisely because they're so close to you.
It's the best use I've found, and it connects to edition 02: the design is the
migration. A specification that accounts for the rare case is worth more than a
pipeline written fast.

**The semantic autopsy of legacy systems.** Reading 300 Z reports written by other
people and extracting the business rule buried in each one. No tired human beats a
machine at that: it's volume, it's tedious, and the result can be verified against
real data. It is, at scale, edition 04: the autopsy of a single Z report.

**Lineage — where each number comes from and what it passed through — and the
documentation nobody wrote.**

All three share the same signature, and that's the practical rule: **the input is
written but scattered, and the result can be verified in minutes.** When a task meets
those two conditions, AI is an enormous multiplier. When it doesn't, you're moving
work around, not eliminating it.

## The rule and its corollary

Two rules come out of all this.

The first: **never ask AI for something you don't know how to verify.** If you can't
evaluate the result in less time than producing it would have taken you, you gained
nothing: you moved the work somewhere you're no longer measuring it. And it isn't a
theoretical cost: a full run of the 2026 exam cost around $343 and more than two
days. Verifying properly always costs something; the question is whether you pay for
it on purpose or by accident.

The second is the one that actually decides your year: **every hour AI saves you on
mechanical work has to be reinvested in the business rules, which are the one thing
it can't handle alone.**

If that saving turns into more pipelines instead of better definitions, you bought
debt on installments. And the first payment comes due the day an agent answers a
business question with an impeccable number nobody signed off on.

Extract and load are no longer your job. Start acting like that's true.

---

## Sources

- Jin, T., Zhu, Y., Kang, D. *ELT-Bench: An End-to-End Benchmark for Evaluating AI
  Agents on ELT Pipelines*. arXiv:2504.04808 (April 2025) · VLDB. 100 pipelines, 835
  source tables, 203 data models. Spider-Agent with Claude 3.7 Sonnet (extended
  thinking): 57% on extract and load, 3.9% on transform; $4.30 and 89.3 steps per
  pipeline. Agents on open-source LLMs scored 0%.
  https://arxiv.org/abs/2504.04808
- Zanoli, C., Giovannini, A., Jin, T., Klimovic, A., Perlitz, Y.
  *ELT-Bench-Verified: Benchmark Quality Issues Underestimate AI Agent Capabilities*.
  arXiv:2603.29399 (April 2026). SWE-Agent with Claude Sonnet 4.5: 96% on extract and
  load, 32.51% on transform (66/203 models); ReAct baseline: 98% and 32.51%. Audit:
  problems in 82.7% of the 81 failed transform tasks; 33% of column-level mismatches
  attributable to the benchmark (23.6% evaluation false positives, 4.8% ambiguous
  descriptions, 4.5% ground truth errors); 30 columns removed (1.2% of the total) on
  expert agreement of just 57.8%. Cost of a full run: ~$343 and 2 days 7 hours.
  https://arxiv.org/abs/2603.29399
- dbt Labs. *State of Analytics Engineering 2026* (April 14, 2026, n=363). 72%
  prioritize AI-assisted coding; 24% prioritize pipeline management (testing and
  observability); 71% concerned about incorrect or hallucinated outputs reaching
  stakeholders; 77% of leaders pushing AI productivity.
  https://www.getdbt.com/resources/state-of-analytics-engineering-2026
