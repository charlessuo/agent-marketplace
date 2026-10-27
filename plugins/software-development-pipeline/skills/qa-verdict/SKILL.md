---
name: qa-verdict
description: "Read a test run someone else measured and turn it into a verdict: check what actually ran, decide whether a failure is the product's or the test's, and write the finding for whoever acts on it. Use when judging test results you did not produce."
---

## Read the measurement first

- **Green or red is the exit code,** not the wording of the summary.
- **Find how many tests ran. Zero is not a pass;** it measures nothing.
- **Output may be elided in the middle;** look at both ends before concluding.
- **Copy the failing tests and assertions exactly.** You'll quote them.

## Product or test?

When a test fails, go back to the **criterion's own words**:
- **The product doesn't do what the criterion says:** the product is wrong.
- **The product meets the criterion, and the test demands more:** the test is wrong. That includes
  a test that asserts something never asked for, depends on timing or order, or drives the product
  wrongly.

Name which, and why.

- **A failure you can't explain is the test's first.** If the output doesn't show the actual value
  or the error, the test must expose it before anyone is blamed. Say what to print, not what to
  assume.
- **Weigh the account of whoever built it.** If they say the product is right and name a test
  defect, check that claim against the test itself before overruling it.
- **A test from an earlier change that now fails is a regression:** this change broke what that one
  shipped, unless this change's criteria deliberately change that behaviour. Then the test is
  wrong, and you name the criterion. Never "the test is stale" without one.
- **Both at fault?** The test findings go first, to whoever owns the tests: a product finding
  measured by a broken test isn't measured yet. Say in your summary what else you found, so it is
  checked once the tests are fixed.

## Enough coverage

Coverage is enough when **each criterion has a test that drives its observable behaviour**: what a
user does and sees.
- **Which test is tagged for which criterion may be measured for you.** When it is, take it as
  settled and judge what no count can: does each tagged test really drive the criterion it names?
  A tag on a test that never exercises its criterion leaves that criterion untested.
- **A criterion with no such test** is a send-back to the test author. Name the criterion, and the
  tagged test that fails to drive it.
- **Wanting a criterion tested more deeply, or with more cases, is a note** once the suite passes,
  never a send-back. A bar that rises after green has no end.

## After a merge

- **Is the failing test new with this change, or was it passing before?** Before means this change
  broke it.
- **A flake or an environment fault is still a failure,** because the base is red. But say so
  plainly, so the fix is aimed at it and not at innocent code.

## Write for the reader

Your words are someone's whole next assignment. For each finding: the criterion, the test, what was
expected, and what happened. A verdict of "tests failed" costs a full round.

**Quote the criterion's words before you send work back.** If you can't quote them, record the
finding as a note. Record these as notes too: an input outside a list the requirement calls
complete, and a request for anything the requirement puts out of scope.

## One pass, then converge

- **Your first verdict reports every finding at once,** blocking and not. A finding held back for a
  later round costs a whole round to deliver.
- **On a re-run, check your earlier findings first:** was each one addressed? That is most of
  the job.
- **A new finding sends the work back only if it blocks:** a criterion not met or not tested at
  all, data lost or corrupted, a crash on documented input, or a security problem. Everything else
  is a note.
- **Don't widen the scope on a re-review.** What the latest round didn't change was judged
  already.
- **Never reverse an earlier finding.** If one was wrong, say so and drop it; asking for the
  opposite of what you asked before sends the work in a circle.