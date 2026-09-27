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

Read the project's existing spec, its decision records, and its domain glossary if it has one,
before proposing anything. Use the project's vocabulary. A recorded decision stands unless the
person deliberately changes it.

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
- **A dependency only where one item truly needs another first.**
- **Human review for anything irreversible or load-bearing.**

**On a revision,** hand over the whole revised result, never a diff of it.