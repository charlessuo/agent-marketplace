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

## After a merge

- **Is the failing test new with this change, or was it passing before?** Before means this change
  broke it.
- **A flake or an environment fault is still a failure,** because the base is red. But say so
  plainly, so the fix is aimed at it and not at innocent code.

## Write for the reader

Your words are someone's whole next assignment. For each finding: the criterion, the test, what was
expected, and what happened. A verdict of "tests failed" costs a full round.