# LinkedIn — EN

**Hook**
There are two ways a data assistant can fail. One is to return an error.
The other —far worse— is to return a number that looks flawless and is wrong.

**Body**
That second failure is exactly how text-to-SQL breaks when you let it run without
context over a real data warehouse. And it's the point that gets lost in most of the
generative BI conversation: the problem is rarely the language model. The model gets
better every quarter and cheaper on its own.

What decides whether you can trust the answer is the context —what each metric means,
which table is the right one, which business rule applies—. That lives in the semantic
layer, and the model doesn't supply it: you do.

The numbers back it up. In dbt Labs' 2026 benchmark, text-to-SQL scores 64.5% across
the full question set; within the scope of a well-modeled semantic layer, accuracy
approaches 100%. But the percentage isn't the point —how each one fails is. The semantic
layer, when it can't answer, tells you so. Text-to-SQL hands you a wrong number wearing
the face of truth.

After years integrating SAP with a lakehouse, this is the lesson I keep: the model is a
commodity; governed context is the defensible advantage. And you build it the same way as
always: start with your five most-queried metrics, model them well, validate against history.

**CTA**
I wrote the full analysis (with sources) in this week's papper. PDF link in the comments.
Is your organization investing in the model, or in the context?

_(Manual upload — remember to attach the PDF or the link to /publicaciones.)_
