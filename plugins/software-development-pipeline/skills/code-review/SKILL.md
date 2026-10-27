---
name: code-review
description: "Review a change on two separate axes — Standards (the project's documented conventions and recorded decisions, plus a code-smell baseline) and Spec (what the originating requirement asked for) — then check that each behaviour change has a test that would catch its regression, and each claim made about the change against the diff and the test output, and turn the findings into a verdict. Use when your task is to review a change set."
---

Review on two axes, and keep them apart:

- **Standards:** does the code follow the project's documented conventions and recorded decisions?
- **Spec:** does it do what the requirement asked, no less and no more?

A change can pass one axis and fail the other, and judging them together lets one hide the other.

Then two passes over the evidence: is each behaviour the change makes protected by a test, and does
each thing said about the change hold?

## Inputs

Your brief says where each one is:
- **The change,** as a whole and as its latest round. Review the whole; on a re-review, use the
  latest round to check that earlier findings were actually addressed. If a diff was truncated,
  read the files themselves.
- **The spec:** the requirement's acceptance criteria, and the project's spec.
- **The standards:** the documented conventions and the decision records. If none exist, review
  against what does exist and say so. Never invent a standard.
- **What was said about the change:** the builder's summary, any plan or description of it, and
  the test output. The summary and the plan are testimony. The diff and the output are evidence.

## Standards pass

Report each break of a documented standard, citing the rule, and each baseline smell, naming it.

- **A documented standard can be a hard violation.** A smell is always a judgement call.
- **The project overrides the baseline:** where the standards or a decision endorse what a smell
  would flag, drop the smell.
- **Skip what tooling or the tests already enforce,** but catch a change that switches the tooling
  off. Report a new lint suppression or a raised complexity threshold anywhere in the change as a
  hard violation. The linter measures complexity, so nobody turns it down.
- **Hold each glossary term to one name.** Report a variable, collection or structure that holds
  two terms the glossary keeps apart. Block on it when the merge causes behaviour the criteria
  forbid. Otherwise report it as a note.

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
- criteria that look implemented but **look wrong**;
- code that parses **another system's format**, such as a page, an API response or an exported
  file, tested only on samples someone wrote by hand. Ask for a trimmed real capture. A
  hand-written sample proves only that the code agrees with its author.

Quote the criterion for each.

## Verification-gap pass

For each behaviour the change adds or alters, name the regression it could introduce, then find the
test that would fail if it did. Read the tests in the diff; don't take their names on trust.

- **No such test is a finding.** Say what behaviour, what regression, and what test is missing.
- **A gap in behaviour a criterion asks for is a spec finding** under that criterion: nothing shows
  the criterion is met. Any other gap is a note.
- **A test that exists but could cover more cases is a note,** never a gap.
- **A test that would still pass with the behaviour broken is no test:** it asserts too little,
  mocks the thing under test, or never reaches the changed path.

## Claims-check pass

Check each claim in the testimony against the evidence, never the other way round.

- **"Added", "handled", "fixed", "covered":** find it in the diff.
- **"Tests pass":** find it in the output, with how many ran. A claim the output doesn't show is
  unchecked.
- **"Already exists", "unchanged", "not needed":** look at the code.
- **A claim the evidence contradicts is a finding.** When it is about a criterion, it is a spec
  finding under that criterion. When it is about anything else, it is a note.
- **A claim you can't check stays unchecked.** Say so; don't repeat it as fact.

## Verdict

- **Request changes only for** a hard standards violation or a spec finding. **Smells never
  block;** list them as optional notes. Sending work back for a judgement call spends someone's
  retries on opinion.
- **A spec finding is a criterion missing, partial or wrong,** in the criterion's own words. An
  edge case the criterion never names is a note, however plausible.
- **Quote what a blocking finding breaks.** Name the criterion, decision record or documented
  standard, and quote its words. If you can't quote any, report the finding as a note.
- **Keep closed lists closed.** Report an input outside a list the requirement calls complete as a
  note. Do the same for a request for anything the requirement puts out of scope.
- Every finding starts with `[Standards]` or `[Spec]`. A verification gap or a failed claim goes
  under the axis it bears on: a criterion is Spec, a documented testing convention is Standards.
- Report the count per axis and the worst finding **within** each axis, never one winner across
  axes.

## One pass, then converge

- **Your first review reports every finding at once,** blocking and not. A finding held back for a
  later round costs a whole round to deliver.
- **On a re-review, check your earlier findings first:** was each one addressed? That is most of
  the job.
- **A new finding sends the work back only if it blocks:** a criterion not met, data lost or
  corrupted, a crash on documented input, a security problem, or a hard standards violation.
  Everything else is a note.
- **Don't widen the scope on a re-review.** What the latest round didn't change was reviewed
  already.
- **Never reverse an earlier finding.** If one was wrong, say so and drop it; asking for the
  opposite of what you asked before sends the work in a circle.
