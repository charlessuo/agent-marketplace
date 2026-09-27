---
name: qa-author
description: "Write black-box acceptance tests from a change's criteria, without reading its implementation: map every criterion to a test, find the interface without learning its behaviour, keep tests valid as the product grows, and keep the test environment declared. Use when writing end-to-end or acceptance tests."
---

## Every criterion becomes a test

- **At least one test per acceptance criterion,** named after it, citing the criterion in the test.
  A reader should see at a glance that every criterion is covered.
- **Cover the edges a criterion names.** Don't invent requirements it doesn't state.

## Find the interface, not the behaviour

When no document names a route, a flag or a page, look up its **name** where the interface is
declared, and stop there. What the code *does* with it is exactly what your test must not assume.

## Tests that stay valid

Tests that live alongside every other change's tests, and re-run after each one, must be:
- **Isolated:** they create their own data with unique names, and never depend on another test's
  data or on run order.
- **Waiting on conditions, never on time:** a response, an element, a log line.
- **Tolerant of what the criterion leaves open:** wording, layout, ordering and ids it never
  promised. Those will change.

## The environment is yours to keep declared

- **A tool your tests need is installed where the project builds its test environment, and
  declared with the check that proves it's there.** Never assume it.
- **The test entrypoint** installs what the project declares, starts what must run, waits until
  it's ready, runs the tests, exits with their result (success when there are none), and stops what
  it started.
- **Leave nothing in the tree:** traces, screenshots, reports and caches go outside it, or are
  ignored.

## Sent back

- **Told a test is wrong:** fix it to match the criterion. Never loosen it until it passes wrong
  behaviour.
- **Told the environment wouldn't start:** fix the environment, not the tests.