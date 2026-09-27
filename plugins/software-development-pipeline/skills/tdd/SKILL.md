---
name: tdd
description: "Test-driven implementation: pick the seams, then red → green one vertical slice at a time, with tests that verify behaviour through public interfaces. Use whenever you implement a change or a fix with tests."
---

TDD is the red → green loop. This skill is what makes the loop produce tests worth keeping.

## Seams: where tests go

A **seam** is the public boundary you test at. Tests live at seams, never against internals.

- **Use the seams the project agreed** for this work; your brief says where they're recorded. Choose
  your own only where that record is silent: from the acceptance criteria and the interfaces that
  exist or that this work creates. Aim at critical paths and complex logic, not every edge case.
- **Write down the seams you tested,** so a reviewer can judge them. A new public interface you
  designed along the way is a design decision; record it the way your brief says.
- **Test your layer only.** If another role owns end-to-end tests (your brief says), don't write
  or duplicate them.

## A good test

- **Verifies behaviour through the public interface.** It survives refactors, and reads like a
  specification ("user can check out with a valid cart").
- **One logical assertion;** the name says WHAT, not HOW.
- **Its expected values come from an independent source of truth:** a literal, a worked example,
  or the criterion.

**Mock only at system boundaries:** external APIs, time and randomness, sometimes the file system.
Prefer a real database when the environment has one. Never mock your own modules. To keep
boundaries mockable, pass external clients in, and give each external operation its own function.

## Anti-patterns

- **Implementation-coupled:** mocks internals, tests private methods, asserts call counts, or
  verifies through a side channel. The tell: it breaks on a refactor that changed no behaviour.
- **Tautological:** the expected value is recomputed the way the code computes it, so it passes by
  construction.
- **Horizontal slicing:** all the tests, then all the code. Work in vertical slices instead: one
  test, one implementation, repeat.

## The loop

1. **A reported failure comes first.** If you're fixing one, your first red test reproduces it.
2. **Red:** one failing test at one seam. Run it, and see it fail for the reason you expect.
3. **Green:** only enough code to pass it. Run it again.
4. **Repeat** until the criteria are covered.
5. **Finish by running the project's whole unit suite, the way your brief says it is run.** It must
   be green.

**Refactoring isn't part of the loop.** Leave nothing behind that your test runs created:
caches, reports and build output.

## Report

The seams you tested; each test added, seen red and then green; and whether the whole suite was
green. If you couldn't run the tests, say so.