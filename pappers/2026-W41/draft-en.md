# From the bedsheet report to the agent

## In February 2027 Microsoft switches off Power BI Q&A, the feature it launched in 2013 with the promise that anyone could ask their data a question in plain language. Tableau has already retired Ask Data, and SAP has retired Search to Insight. This edition walks through eight generations of reporting, product by product: what each one made possible, what it didn't, and what kind of analysis we are actually buying today.

In February 2027, any Power BI report that still has a Q&A visual will show an error where it used
to show an answer. Microsoft announced the retirement in December 2025 for the end of 2026, and in
September it moved the date to February. The official replacement is Copilot.

Q&A arrived in September 2013 in the Power BI for Office 365 preview: you typed "sales by region in
2013" and a chart appeared. Tableau launched Ask Data in 2019 and retired it in 2024; SAP replaced
Search to Insight with Just Ask at the end of that same year. Between 2024 and 2027, all three
vendors are retiring their first attempt at letting people ask their data questions in natural
language.

[ FIGURE 1 — "The first NLQ, retired": timeline of Q&A, Ask Data and Search to Insight, and
Microsoft's migration table (Q&A Setup → Prep data for AI). ]

I have spent more than twenty years building reports in almost every generation that follows, and
the pattern repeats: each new product changes **what kind of question** the business can ask without
asking IT for anything. None of them has changed who decides what the number means.

## First generation: the bedsheet

In finance and operations teams in Mexico we call the long tabular report a **sábana**, a bedsheet:
hundreds or thousands of rows, printed or exported, with every column anyone ever asked for. It is
the COBOL or RPG listing on the mainframe, the ALV report in SAP and, since the nineties, Crystal
Reports.

**The analysis it enables:** operational. List, filter, sort, subtotal: "give me the open invoices
for branch 12 that are more than 60 days old." It is the oldest generation and the one that has died
the least: it is how a period close gets reconciled, because every row can be traced back to a
document.

**What it doesn't allow:** asking a new question; every variation is a request to IT. In the
mid-seventies IBM created *information centers* to handle the queue of requests (the *backlog*) that
IT could not keep up with. The reporting backlog is older than the PC.

## Second generation: the spreadsheet

VisiCalc (1979, Apple II) is often cited as the application that turned the personal computer into a
business tool. Lotus 1-2-3 and Excel followed. Excel 5, in 1993, brought the **PivotTable**, an idea
Lotus had tried in Improv (1991).

**The analysis it enables:** scenarios and cross-tab summaries without writing code: "what happens
to margin if price goes up 3%?" or "sales by product by month." For the first time, the business
user builds their own analysis.

**What it doesn't allow:** two people arriving at the same number. The spreadsheet works on an
extract, and every extract is a copy. Ever since, the most expensive question in a board meeting has
been "which of the two files is the right one?"

## Third generation: the cube

In 1993 Edgar F. Codd, the creator of the relational model, published with two co-authors the paper
that named **OLAP** (*Online Analytical Processing*): databases organized for analysis rather than
for recording transactions. Essbase (1992), Cognos PowerPlay, Microsoft Analysis Services and, from
1998, SAP BW with its BEx query tool all belong to that family.

**The analysis it enables:** multidimensional. Cut the data along any axis (*slice and dice*), drill
down a hierarchy (region → zone → customer) and compare against the same period last year. What was
a fragile formula in the spreadsheet is a function of the engine in the cube.

**What it doesn't allow:** asking what wasn't modeled. The cube answers fast, but only within the
dimensions and measures designed in advance; a question outside the design goes back to the request
queue.

## Fourth generation: the semantic layer

On November 27, 1991, Business Objects (now part of SAP) filed US patent application 5,555,403,
granted in 1996. Its goal, in the document's own words: to let users query relational databases
"without knowing the relational structure or the SQL language." The central piece was called the
**universe**: an easy-to-understand representation of the database, designed for a group of users.
Today we call it a *semantic layer*.

**The analysis it enables:** governed *ad hoc* querying (built on the spot). The user drags business
objects ("Customer", "Revenue", "Region") and the tool writes the SQL: "customers with more than
three returns this quarter," without waiting for anyone and using the definition of "revenue" that
finance approved.

**What it doesn't allow:** a universe that maintains itself. Someone in IT has to add every object,
every synonym and every rule. This idea comes back at the end.

## Fifth generation: visual discovery

In 2002 Chris Stolte, Diane Tang and Pat Hanrahan published Polaris at Stanford, a system for
querying and charting at the same time by dragging fields; Tableau was born from it. In parallel,
QlikView brought an associative engine that showed what matched a filter and also what was left out.

**The analysis it enables:** exploratory. See where a drop is concentrated, spot an outlier on a
map, find a relationship nobody had asked about. It is the first generation in which analysis starts
by looking, not by asking.

**What it doesn't allow:** a single truth. Every analyst builds their own workbook with their own
calculations. Visual discovery multiplied the analyses, and the definitions along with them.

## Sixth generation: cloud self-service

Power BI became generally available on July 24, 2015. Looker turned the semantic model into code
with LookML, its modeling language, and SAP Analytics Cloud combined BI, planning and prediction in a
single product.

**The analysis it enables:** self-built models and shared dashboards. The business analyst builds
their model, writes their measures (in Power BI, in the DAX language) and publishes for their team.
In SAC they can also plan on the same model they report from.

**What it doesn't allow:** controlling the sprawl. The ease that democratized reporting produced
hundreds of models with the same measure calculated in different ways. The "certified" badge I
looked at in the previous edition is an attempt to bring order here.

## Seventh generation: the first wave of artificial intelligence

This is where Q&A, Ask Data and Search to Insight come in, all trying to let the user type their
question. Alongside them came **augmented analytics**: features that looked for explanations on
their own, such as Key Influencers in Power BI, Explain Data in Tableau and Smart Insights in SAC.

**The analysis it enables:** automated diagnosis. "Which factors explain why this customer is
leaving?" or "why is this point off the trend?", without the analyst building the statistical model.

**What it doesn't allow:** a conversation. These engines recognized keywords and mapped them to
columns. For them to work, someone had to capture synonyms and relationships by hand; in Power BI,
with *Q&A Setup* and the option to "teach" Q&A. If the user typed "billing" and the synonym didn't
exist, there was no answer. The idea wasn't bad; the method didn't scale.

## Eighth generation: the agent

The current generation uses large language models (LLMs) to understand the intent of a question,
write the query, run it and explain the result. It is called *GenBI* (generative BI) or, when the
system chains several steps on its own, agentic analytics. These are the products competing today,
each with a sample question:

- **Copilot in Power BI.** Answers questions about the semantic model, creates report pages and
  writes DAX queries; since April 2025 it runs on the smallest Fabric capacity (F2). *"Summarize what
  changed in the sales report this week."*
- **Databricks Genie.** Generally available since June 2025. Answers with text, a table and a chart,
  and shows the SQL it used; Databricks has also announced a research mode that tests several
  hypotheses. *"Why did margin drop in the north in August?"*
- **Snowflake's agent.** Generally available since November 2025 as Snowflake Intelligence (the
  documentation now calls it Snowflake CoWork). It uses Cortex Analyst to turn questions into SQL
  over *semantic views*, views that carry the business metrics and relationships. *"Which ten
  customers grew the most versus last year?"*
- **SAP Analytics Cloud: Just Ask and Joule.** Just Ask answers questions over SAC models that have
  been indexed beforehand; Joule remembers the context of the previous question. *"Now show me only
  the modern trade channel."*
- **Tableau Pulse.** It doesn't wait for the question: it watches metrics defined once in its
  metrics layer and alerts you when something changes, and why. *"Your returns metric is up 12%; the
  main driver is the western region."*
- **Looker Conversational Analytics.** Uses Gemini, Google's model, and relies on LookML so the
  answer uses the same calculation as the rest of the company.

**The analysis it enables:** conversational and multi-step. A single question can combine the
descriptive (what happened), the diagnostic (why) and a projection (what happens if it continues),
in the business's words rather than the model's.

**What it doesn't allow, yet:** guaranteeing the same answer. Microsoft says so in its own
documentation: preparing data for AI "can't guarantee a specific outcome every time," because AI
behavior is non-deterministic.

One data point for readers in Mexico: according to that same documentation, updated in September,
the standalone Copilot experience in Power BI is not yet available in the Mexico Azure region. It is
worth confirming where your capacity lives before designing the strategy.

## How well does an agent answer?

The best public reference is Spider 2.0, an academic *benchmark* for *text-to-SQL* (translating a
question into SQL) presented at ICLR 2025: 632 problems over real enterprise databases, many with
more than a thousand columns. When it was published, the best agent (built on OpenAI's o1-preview)
solved **21.3%**; the same approach solved 91.2% of the much simpler Spider 1.0. As of October 1,
2026, on the variants the public *leaderboard* now maintains (not identical to the original test),
first place reports **96.7%** on Snowflake and **76.2%** on the variant that mixes several database
engines. The progress is real and fast: less than two years.

In January 2026, at the CIDR conference, a team from the University of Illinois reviewed the
reference answers of Spider 2.0 on Snowflake and of BIRD, another widely used benchmark: it found
annotation errors in **66.1%** and **52.8%** of the problems, respectively. Once corrected, the
relative performance of the systems shifted by up to 31% and the ranking moved by up to three
places. Some of those errors were about domain knowledge: the "correct" answer didn't understand what
the business question was asking.

The hard part is not getting the agent to write good SQL. It is having someone who knows what the
right answer is.

[ FIGURE 2 — "Same question, four languages": SQL, MDX, DAX and a verified query with its
verified_by. ]

## What hasn't changed in eight generations

The documentation of the eighth-generation products asks for the same thing before promising
anything:

- **Power BI**, in "Prep data for AI," asks you to prepare the semantic model with an AI data schema,
  **verified answers** (a visual returned when a given question is asked) and **AI instructions**
  carrying the business logic and vocabulary, and then to mark the model as "Approved for Copilot."
- **Databricks** says whoever builds a Genie agent "needs to understand the data," and that analysts
  fluent in SQL "typically have the knowledge" to curate it.
- **Snowflake** acknowledges that generic solutions "struggle" to turn text into SQL "when they only
  have the database schema," because the schema lacks the definitions of the business process and
  its metrics.
- **SAP** offers a *readiness* check of the model before Just Ask and Joule use it.

Gartner summed it up in May: schema-only data models are "no longer sufficient" for agentic AI,
because they lack business context and meaning. In March it had predicted that by 2030 universal
semantic layers will be treated as critical infrastructure, on a par with the data platform and
cybersecurity.

The 1991 universe solved the same problem: translating the language of the business into the
structure of the database. What Q&A Setup asked for (synonyms, relationships, teaching the tool) is
almost exactly what Prep data for AI asks for today; in Microsoft's migration table, one is the
official replacement for the other. **The product changed eight times. The job of deciding what each
business word means never went away.**

[ FIGURE 3 — "Eight generations, one job": the full ladder with the analysis each generation enables
and what it doesn't allow. ]

## What to buy, depending on the question

No generation eliminated the one before it: the bedsheet still reconciles closes, Excel is still in
every finance team and the cube is still the fastest way to compare periods. For whoever decides the
investment, the useful question is not "what's the newest tool?" but "what kind of question does the
business need answered?"

| If the question is… | The analysis is… | The generation that answers it best |
|---|---|---|
| "Give me the detail to reconcile" | Operational, traceable | Bedsheet / tabular report |
| "What if…?" with my own assumptions | Scenarios | Spreadsheet or planning (SAC) |
| "Compare against last year by hierarchy" | Multidimensional | Cube / semantic model |
| "I want to see where the problem is" | Exploratory | Visual discovery |
| "Every morning, the same indicators" | Monitoring | Dashboard or metrics with alerts (Pulse) |
| "Why did it happen and what's next?", without knowing in advance what to cross | Conversational, multi-step | Agent (Copilot, Genie, Snowflake, Joule) |

Three recommendations for whoever signs the budget:

1. **Before buying the agent, take an inventory of your vocabulary.** If "net sales" is calculated
   three ways in three models, the agent will pick one, and do so with great confidence. The semantic
   layer is not optional: it is what you are really buying.
2. **Budget for the curator, not just the license.** Every eighth-generation product assumes someone
   who writes instructions, validates answers and maintains examples. That role has existed since the
   1991 universe; what's new is that its work can now be measured.
3. **Demand a test, and review it.** Genie has *benchmarks*, Power BI has verified answers and
   Snowflake has *verified queries*. Use them, but remember the Illinois study: the reference answer
   can be wrong too, and whoever writes it has to know the business, not just the SQL.

If your organization still has Q&A visuals, you have until February 2027 to migrate them. It's a good
moment to ask yourself something more fundamental: not which tool replaces them, but who is going to
decide what each question the business asks the agent actually means.

---

## Sources

- Microsoft Fabric Community, Power BI Updates Blog — *Power BI Q&A retirement reminder: February 2027
  timeline update* (Mohammad Ali, Power BI Team, Sep 2026): retirement extended from Dec 2026 to Feb
  2027; replacement table (Q&A Setup → Prep Data for AI); Copilot from F2 capacity.
  https://community.fabric.microsoft.com/blog/fbc_pbiupdatesblog/power-bi-qa-retirement-reminder-february-2027-timeline-update/5365841
- Microsoft Power BI Blog — *Deprecating Power BI Q&A* (announcement, Dec 2025; retirement planned
  for Dec 2026).
  https://powerbi.microsoft.com/blog/deprecating-power-bi-qa
- Microsoft Fabric Updates Blog — *Copilot and AI capabilities now accessible to all paid SKUs in
  Microsoft Fabric* (Apr 2025): Copilot from F2 starting April 30, 2025.
  https://blog.fabric.microsoft.com/en-us/blog/copilot-and-ai-capabilities-now-accessible-to-all-paid-skus-in-microsoft-fabric
- Microsoft 365 Message Center — MC1218421, *Retirement of Power BI Q&A* (Jan 16, 2026).
  https://mc.merill.net/message/MC1218421
- Microsoft SQL Server Blog — *Microsoft Updates Power BI for Office 365 Preview with New Natural
  Language Search…* (Sep 25, 2013).
  https://www.microsoft.com/en-us/sql-server/blog/2013/09/25/microsoft-updates-power-bi-for-office-365-preview-with-new-natural-language-search-mapping-capabilities/
- Microsoft Learn — *Prepare your data for AI to improve Copilot results* (updated Sep 16, 2026): AI
  data schema, verified answers, AI instructions, "Approved for Copilot," non-determinism, regional
  availability.
  https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai
- Microsoft — *Power BI is Generally Available today* (Jul 24, 2015) and Official Microsoft Blog
  (Jul 10, 2015), announcement of the GA date.
  https://blogs.microsoft.com/blog/2015/07/10/over-500000-unique-users-from-45000-companies-across-185-countries-helped-shape-the-new-power-bi/
- Tableau Help — *Automatically Build Views with Ask Data*: retirement in Tableau Cloud (Feb 2024) and
  Tableau Server 2024.2.
  https://help.tableau.com/current/pro/desktop/en-us/ask_data.htm
- SAP Knowledge Base Article 3532315 — *Deprecation of Search to Insight feature in SAP Analytics
  Cloud* (deprecated from QRC Q4 2024; successor Just Ask).
  https://userapps.support.sap.com/sap/support/knowledge/en/3532315
- SAP Help Portal — *Check Your Model's Readiness for Just Ask and Joule Analytical Insights*.
  https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/18850a0e13944f53aa8a8b7c094ea29e/121c342e23124efb8295f1bb785b2cc0.html
- SAP Learning — *Managing Conversations with Joule* (Joule keeps the context of the conversation).
  https://learning.sap.com/courses/getting-started-with-joule-for-business-users/managing-conversations-with-joule
- Databricks — *AI/BI Genie is now Generally Available* (Jun 12, 2025).
  https://www.databricks.com/blog/aibi-genie-now-generally-available
- Databricks — *Curate an effective Genie space* (best practices, updated Sep 11, 2026).
  https://docs.databricks.com/aws/en/genie/best-practices
- Snowflake — Release note *Nov 04, 2025: Snowflake CoWork (General availability)* and *Cortex
  Analyst* documentation (semantic views, verified queries).
  https://docs.snowflake.com/en/release-notes/2025/other/2025-11-04-snowflake-intelligence
  https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst
- Google Cloud — *Conversational Analytics in Looker overview*.
  https://docs.cloud.google.com/looker/docs/conversational-analytics-overview
- Tableau — *Now Available in 2024.1 Release: Tableau Pulse, Metrics Layer…*
  https://www.tableau.com/blog/release-tableau-pulse-metrics-layer-viz-navigation
- Cambot, J.-M. and Liautaud, B. — US Patent 5,555,403, *Relational database access system using
  semantically dynamic objects* (filed Nov 27, 1991, granted Sep 10, 1996).
  https://patents.google.com/patent/US5555403A/en
- Stolte, C., Tang, D. and Hanrahan, P. — *Polaris: A System for Query, Analysis, and Visualization of
  Multidimensional Relational Databases*. IEEE TVCG 8(1):52-65, 2002.
- Codd, E. F., Codd, S. B. and Salley, C. T. — *Providing OLAP to User-Analysts: An IT Mandate* (1993).
- Carr, H. H. — *Information Centers: The IBM Model vs. Practice*. MIS Quarterly 11(3):325-338, 1987.
  https://aisel.aisnet.org/misq/vol11/iss3/5/
- Lei, F. et al. — *Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL
  Workflows*. ICLR 2025. Leaderboard accessed Oct 1, 2026.
  https://spider2-sql.github.io/
- Jin, T., Choi, Y., Zhu, Y. and Kang, D. — *Text-to-SQL Benchmarks are Broken: An In-Depth Analysis of
  Annotation Errors*. CIDR 2026 (Jan 18-21, 2026), University of Illinois Urbana-Champaign.
  https://www.vldb.org/cidrdb/papers/2026/p5-jin.pdf
- Gartner — *Gartner Announces Top Predictions for Data and Analytics in 2026* (Mar 11, 2026) and
  *Gartner Says Lack of Semantics Causes Inaccurate AI Agents and Wasted Spending* (May 11, 2026).
  https://www.gartner.com/en/newsroom/press-releases/2026-03-11-gartner-announces-top-predictions-for-data-and-analytics-in-2026
  https://www.gartner.com/en/newsroom/press-releases/2026-05-11-gartner-says-lack-of-semantics-causes-inaccurate-artificial-intelligence-agents-and-wasted-spending
