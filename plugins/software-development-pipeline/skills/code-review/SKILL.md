---
name: code-review
description: "Review a change on two separate axes — Standards (the project's documented conventions and recorded decisions, plus a code-smell baseline) and Spec (what the originating requirement asked for) — and turn the findings into a verdict. Use when your task is to review a change set."
---

Review on two axes, and keep them apart:

- **Standards:** does the code follow the project's documented conventions and recorded decisions?
- **Spec:** does it do what the requirement asked, no less and no more?

A change can pass one axis and fail the other, and judging them together lets one hide the other.

## Inputs

Your brief says where each one is:
- **The change,** as a whole and as its latest round. Review the whole; on a re-review, use the
  latest round to check that earlier findings were actually addressed. If a diff was truncated,
  read the files themselves.
- **The spec:** the requirement's acceptance criteria, and the project's spec.
- **The standards:** the documented conventions and the decision records. If none exist, review
  against what does exist and say so. Never invent a standard.

## Standards pass

Report each break of a documented standard, citing the rule, and each baseline smell, naming it.

- **A documented standard can be a hard violation.** A smell is always a judgement call.
- **The project overrides the baseline:** where the standards or a decision endorse what a smell
  would flag, drop the smell.
- **Skip what tooling or the tests already enforce.**

**Smell baseline**, each *what it is* → *fix*:
- **Mysterious Name** → rename.
- **Duplicated Code** → extract.
- **Feature Envy** → move the method to the data it envies.
- **Data Clumps** → bundle into a type.
- **Primitive Obsession** → give the concept its own type.
- **Repeated Switches** → polymorphism, or one shared map.
- **Shotgun Surgery** → gather what changes together.
- **Divergent Change** → split the module.
- **Speculative Generality** → delete it.
- **Message Chains** → hide the walk behind one method.
- **Middle Man** → call the real target.
- **Refused Bequest** → composition.

## Spec pass

Do this separately; don't carry the Standards judgement into it. Report:
- criteria that are **missing or partial**;
- behaviour **nobody asked for**. Supporting changes the work needed, and the records your brief
  requires, are not scope creep;
- criteria that look implemented but **look wrong**.

Quote the criterion for each.

## Verdict

- **Request changes only for** a hard standards violation or a spec finding. **Smells never
  block;** list them as optional notes. Sending work back for a judgement call spends someone's
  retries on opinion.
- Every finding starts with `[Standards]` or `[Spec]`.
- Report the count per axis and the worst finding **within** each axis, never one winner across
  axes.