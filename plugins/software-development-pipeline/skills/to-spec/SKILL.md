---
name: to-spec
description: "Turn a requirements conversation into a spec and a plan of work: confirm test seams while the person is still there, then synthesize a standalone spec, decision records, and vertical-slice work items with outside-in acceptance criteria. Use as a conversation converges, and on the turn after the person approves."
---

## Two moments

- **Still conversing:** when the shape stops changing, confirm the seams (below) with the person,
  then say you think it's ready.
- **After approval:** **don't interview.** Synthesize what you already know. An unresolved point
  becomes an open question, never a guess.

Your brief defines the exact shape of what you hand over. This skill is how to fill it.

## Know the current state

Read the project's existing spec, its decision records, and its glossary before proposing
anything. Use the project's vocabulary. A recorded decision stands unless the
person deliberately changes it.

**Leave recorded decisions to the person.** Supersede a decision record only when they asked for
that change. If their request seems to conflict with one, keep the decision and ask them about it by
name. If the conflict is still open after approval, list it as an open question, never as a new
decision.

## Agree the seams, while you can still ask

Sketch where the work will be tested:
- prefer existing seams to new ones;
- use the highest one possible;
- fewer is better, and one is ideal.

**Ask the person whether they match their expectations.**

## The spec

Revise an existing spec rather than replacing it. Sections:
- **Problem Statement:** from the user's perspective.
- **Solution:** from the user's perspective.
- **User Stories:** a long, numbered list covering everything, each "As an <actor>, I want
  <feature>, so that <benefit>". Numbers stay stable across revisions.
- **Glossary:** every domain term, one line each. A term that names stored data maps to exactly
  the table and column(s), or the API field(s), that hold it. Two terms never share a definition:
  if they would, they are one term, or the definition is not precise enough yet. Add a term when
  the work introduces one, and keep the old ones.
- **Testing Decisions:** the agreed seams, what a good test is here (external behaviour only), and
  prior art.
- **Decisions:** a one-line index. Each decision also gets its own record: its context, the
  decision, its consequences, and what was rejected.
- **Out of Scope.**
- **Open Questions.**

**No file paths or code snippets;** they go stale. The one exception is a prototype snippet that
encodes a decision more precisely than prose; trim it and say where it came from.

## The plan

- **Vertical slices:** each item delivers something a user can observe, end to end. Not layer by
  layer.
- **Each item says how you'd know it works, from the outside,** and names the stories it covers.
- **Each item is independently implementable and testable.** Two changes that must land together
  are one item; small beats large.
- **An item's terms are the glossary's terms.** A new one goes into the glossary first, then the
  item uses it.
- **Every term a criterion depends on is defined,** in observable terms: what a word like
  "eligible", "complete" or "last successful state" means as something a user can see. An
  undefined term is read two ways by the implementer and the tester, and each round flips between
  them.
- **A criterion about failure or bad input lists its cases,** as a closed list: no "such as", no
  "etc.". An open list can be extended by every reviewer, every round.
- **Each item says what it leaves out:** nearby behaviour a reader might assume it covers, stated
  as out of scope, so nobody tests for it.
- **A dependency only where one item truly needs another first.**
- **Human review for anything irreversible or load-bearing.**

**On a revision,** hand over the whole revised result, never a diff of it.