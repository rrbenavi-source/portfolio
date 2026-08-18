# We took away the first rung

*The mechanical work AI absorbed wasn't only work. It was how a senior got made.*

**Brújula · Edition 07 · W34**
*Team Leadership · Data Engineering*

---

The last edition closed on something that sounded like good news: AI already handles the
mechanical work of a pipeline — connecting to the source, authenticating, landing the
data — and breaks down exactly where judgment lives, in the business rules.

I've spent two weeks turning over the part I didn't write. If the mechanical work is
solved, and the mechanical work is what we used to hand to someone starting out, **where
does someone starting out come in now?**

This week a number showed up that puts figures to that question.

## The number

On August 12, Stanford's Digital Economy Lab published the revision of a study it has
been running since 2025. It isn't a survey and it isn't a vendor report: it's
administrative payroll data from ADP, millions of workers in the United States, through
June 2026.

Here is what they compare. They rank every occupation by how exposed it is to generative
AI — how much of that job's work a model could plausibly do today — then contrast how
employment moved in the most exposed occupations against the least exposed, and split
the result by age.

The first finding deserves to come before all the others, because it's the one nobody
repeats: **there is no evidence of widespread displacement**.

The second one stings. Employment among workers aged **22 to 25** in the most exposed
occupations now sits **19% below** where it would be had it kept pace with their
same-age peers in less exposed occupations. Experienced workers show no comparable gap.
And the gap is widening: in the July 2025 reading it was 15%.

The third explains the second: the decline **is not coming from layoffs**. It's coming
from hiring that stopped. Separation rates fell for everyone; what closed was the front
door.

The authors themselves insist this is descriptive rather than causal, and that the gap
narrows once you control for education. Even so, two independent sources point the same
way: the Census Bureau measures a **12%** drop in employment among 22-to-24-year-olds in
the most exposed quintile of industries, and the Dallas Fed confirms the pattern with the
caveat nobody quotes — even if that entire decline became unemployment, it would be
roughly **0.1 percentage point** of the aggregate. This is a composition problem, not a
volume problem.

## The finding that actually changes how I run a team

None of that cost me sleep. What did was the new part of the study: the part that
explains **where** young employment falls.

It falls in occupations that rely on **codified knowledge** — the formal, standardized
kind that is written down and can be taught through a manual, a course, or a documented
procedure. And it rises, for experienced workers, in occupations that rely on **tacit
knowledge**: the kind acquired only through practice, mentorship, and repeated exposure
to real situations.

Put differently: AI is excellent at substituting for what someone already wrote down,
and turns out to complement what nobody ever wrote down at all.

That confirms what we've been arguing here. What we hadn't drawn out is the management
consequence, and it's this:

**Tacit knowledge isn't taught. It gets manufactured by passing through the codified
kind.**

Nobody develops the instinct to distrust a number without having reconciled two hundred
of them first. That instinct — the one that makes you look at a total and say "something
is wrong here" before you can explain why — doesn't come from a course. It comes from
chasing an eleven-peso discrepancy between two reports for three days and discovering at
the end that an exchange rate was applied on one side and not the other.

That work was boring, it was slow, and to the business it was worth very little. It was
also, without anyone designing it that way, **the only curriculum we had**. We pulled it
from the catalog because the machine does it faster, without noticing that besides
producing, it trained.

And here is the number that makes this a budget decision rather than a generational
lament. It comes from Indeed's Hiring Lab, which publishes its job postings index as a
public series — anyone can verify it in the St. Louis Fed's database — and which in July
reported something it wasn't expecting to find.

Between 2022 and 2026, the more exposed an occupation was to AI, the more its postings
fell. That much we knew. What's new is that over the past year **the relationship
flipped**: software development postings are up roughly **15%** since late February 2025,
while total postings across the country **fell 7%**. So the market didn't collapse. It's
coming back.

But look at where the rebound comes from. **71% of the increase is in senior roles**, and
it starts from a low floor — software postings remain 27.5% below their pre-pandemic
level, and data analysis roughly 30% below. Revelio Labs, a labor data provider,
measures the same thing by a different route and arrives at the same shape — senior
headcount +31%, junior +6%. That's vendor data, but it agrees with a public series built
on a different methodology. Two independent sources, the same split.

It isn't that the market fell. It's that the market is recovering **while skipping the
first rung**. Demand came back, and it came back asking for experience already made.

The question that leaves on the table is uncomfortable because it has no market answer:
**where will the seniors of 2031 come from?** Not yours. Everyone's. It isn't that
nobody is training juniors — that 6% says otherwise. It's that they're being trained at
a fifth of the rate at which finished experience is hired, and that experience can't be
bought if the base stops being produced. No vendor sells it.

And if you run a large organization, the consequence reaches past your own payroll. The
experience you rent today — the senior consultant, the integrator, the shared services
center — comes out of the same funnel. When your supplier stops training juniors because
AI already covers the billable entry-level work, it isn't saving money: it's drawing down
an inventory of people with judgment who in three years will quote you higher and take
longer to arrive. That's a contract conversation, not an HR one.

## The honest objection

That's the case for it. Now the other side, because this newsletter is worth nothing if
I only tell you the half that suits me.

In June, two researchers at the London School of Economics' Centre for Economic
Performance published *The Broken Ladder*, using 243 million hires and 407 million job
postings across four countries.

Their argument cuts against the easy reading: exposure to generative AI is strongly
correlated with another simultaneous shock, **remote work**. Estimated separately, both
predict the falling share of juniors among new hires. Estimated **jointly**, the
remote-work effect holds and the AI coefficient attenuates so sharply it is often
statistically indistinguishable from zero.

Translated: maybe AI didn't break the ladder. Maybe we broke it when we stopped seating
the person starting out three meters from the person who knows.

Stanford's August revision addresses that objection: among its robustness checks it
controls for a remote-work measure — taken from Hansen and coauthors and from Lambert
and Schindler themselves — and holds that the divergence persists. Two serious teams,
different data, different conclusions. Anyone who tells you it's settled is selling you
something.

What's notable is that, for a leader, **the practical conclusion is identical either
way**. If AI is the culprit, you lost the work that trained people; if distance is the
culprit, you lost the exposure that trained them. In both cases what broke is learning
by observation, and in both cases it has to be rebuilt deliberately, because it no
longer arrives on its own.

## The half missing from the conversation

The debate is about what the junior loses. The other half is missing: **the senior has
to relearn too**, and mid-career, which is when the appetite for it is lowest. The ways
this craft used to be handed down — programming alongside someone, arguing a design at a
whiteboard, documenting for whoever comes next — now have AI sitting in the middle.

A qualitative study presented in April at the CHI conference observed the following: on
**familiar** tasks juniors and seniors hold on to control over what the tool proposes
equally well; the divergence shows up on **unfamiliar** ones, where the boundaries of
what's expected are poorly defined and move as you go. That's where the one steering
separates from the one along for the ride. And unfamiliar tasks are, precisely, where
learning happens. Small sample — five seniors and ten juniors — and qualitative, so I
don't take it as measurement but as a precise description of something I've watched
happen.

## What to do on Monday

I'm not proposing you hire juniors out of nostalgia, or slow down adoption of these
tools. That would be bad for the business and, on top of it, futile.

I'm proposing you accept that **training stopped being a byproduct and became a line
item** — and, if you sign the budget, a budget line. It used to come free; now you have
to design it. Five concrete things:

**One: change the deliverable, not the difficulty.** If AI produces the pipeline, don't
have the junior produce it — have them **audit it against the source**, with the evidence
in front of them. Reviewing teaches more than producing.

**Two: hand over the unfamiliar task on purpose.** Today that has to be arranged: take
them into the meeting where the user can't explain what they want, put them on gathering
the ambiguous requirement, let them raise the open question in front of everyone. That
isn't exposure to code: it's exposure to the business.

**Three: change what you evaluate.** If you measure someone by what they deliver, you're
measuring their tool. Measure the questions they ask. A junior who in their third month
asks "does this net sales figure include the returns from the entity that doesn't
consolidate the same way?" is worth more than one who shipped three dashboards without
asking anything — and the second will look more productive on any report.

**Four: redesign the interview.** If a candidate delivers something flawless and you
don't know how much of it they wrote, the portfolio has stopped helping you decide. What
still does: hand them someone else's code and ask what's wrong with it, or hand them a
deliberately ambiguous business rule and see whether they **catch the ambiguity** instead
of picking a reading and moving on. It makes no difference which tool they use.

**Five, if you sign contracts: ask your supplier who they are training.** Not how many
senior profiles they'll assign you, but what bench sits behind them. An integrator that
only offers finished talent is selling you its inventory, not its capacity to carry you
for three years. The question fits into a negotiation and almost nobody asks it.

---

One note on honesty before closing, and I'm writing this from Monterrey. All the
evidence I cited comes from English-speaking markets. **I don't know of an equivalent
series for Mexico**, and I'm not going to invent one.

What I can tell you is what it looks like from here. A large share of this region's
entry-level work never lived inside the business areas at all: it lived in the shared
services centers that multinationals set up in northeastern Mexico precisely because
that work was codified, repeatable, and could be written into a procedure. Which is to
say the region specialized in the exact layer AI absorbs first. If your organization
runs one of those centers, this discussion isn't theoretical and it isn't five years
out.

What travels isn't the percentages. It's the mechanism.

Headcounts aren't shrinking. They're getting more senior. That sounds like an
improvement, and in the short run it is. But a pyramid without a base isn't a more
efficient pyramid: it's a pyramid that hasn't fallen over yet.

---

## Sources

- Brynjolfsson, E., Chandar, B., Chen, R. **Canaries in the Coal Mine? Six Facts about
  the Recent Employment Effects of Artificial Intelligence.** Stanford Digital Economy
  Lab, August 2026 revision (ADP payroll data through June 2026). No widespread
  displacement; a 19% gap in employment for ages 22–25 in the most exposed occupations
  (15% at the July 2025 vintage); adjustment operating through reduced hiring rather
  than increased separations; declines concentrated in codified-knowledge occupations
  and growth for experienced workers in tacit-knowledge ones. The authors present this
  as descriptive rather than causal evidence and note the gap narrows when controlling
  for education. The divergence persists when controlling for remote work, interest
  rates, and alternative exposure measures.
  https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf
- Lambert, P. J., Schindler, Y. **The Broken Ladder: AI, Remote Work, and Early-Career
  Hiring.** CEP Discussion Paper 2193, London School of Economics, June 2026. 243
  million hires and 407 million job postings across the US, UK, Canada, and Australia,
  2017–2025. Estimated separately, GenAI and remote-work exposure each predict the
  falling junior share of new hires; estimated jointly, the remote-work effect holds
  while the GenAI coefficient attenuates sharply and is often statistically
  indistinguishable from zero.
  https://ideas.repec.org/p/cep/cepdps/dp2193.html
- Tucker, L. C. **US Census Bureau, CES Working Paper 26-27**, April 2026. A 12% decline
  in employment among workers aged 22–24 in the most AI-exposed quintile of industries
  over the ten quarters following ChatGPT's release, using matched employer-employee
  administrative data.
  https://www.census.gov/library/working-papers/2026/adrm/CES-WP-26-27.html
- **Federal Reserve Bank of Dallas**, January 2026. Confirms the pattern using the
  Current Population Survey and estimates that even if the entire decline in young
  employment in exposed occupations became unemployment, it would account for about 0.1
  percentage point of aggregate unemployment since November 2022.
  https://www.dallasfed.org/research/economics/2026/0106
- **Indeed Hiring Lab.** *AI and Job Postings: From Destruction to Creation?* (July 8,
  2026) and *US Labor Market Snapshot — June 2026* (July 23, 2026). Between May 2022 and
  May 2026, the most AI-exposed occupations lost the most postings; over the past year
  the relationship inverts and they rebound the most. Software development postings rose
  roughly 15% since late February 2025 while total postings fell 7%, but 71% of that
  increase is in senior roles and 37% in jobs mentioning AI in the title. Software
  remains 27.5% below its pre-pandemic level and data analysis roughly 30% below. The
  index is published as a public series and is available on FRED, from the Federal
  Reserve Bank of St. Louis (series IHLIDXUSTPSOFTDEVE).
  https://www.hiringlab.org/2026/07/08/ai-and-job-postings-from-destruction-to-creation/
- **Revelio Labs, AI Labor Market Tracker**, July 2026. Market data from a labor data
  provider, not academic evidence; used here only as corroboration of Indeed's public
  series, built on a different methodology. Among firms that adopted AI, senior headcount
  grew 31% against 6% for junior roles. The tracker itself notes that adopting firms were
  already growing faster before adoption.
  https://www.reveliolabs.com/ai-labor-market-tracker/us/july-2026
- Feng, D., Yun, B., Wang, A. Y. **From Junior to Senior: Allocating Agency and
  Navigating Professional Growth in Agentic AI-Mediated Software Engineering.** CHI 2026
  (arXiv:2602.00496). Qualitative study of software engineering: on familiar tasks
  juniors and seniors retain control equally; the divergence appears on unfamiliar
  tasks, where the boundaries of what's expected are poorly defined. Small sample (five
  seniors and ten juniors in the main phases).
  https://arxiv.org/abs/2602.00496
