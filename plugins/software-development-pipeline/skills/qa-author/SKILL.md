---
name: qa-author
description: "Write black-box acceptance tests from a change's criteria, without reading its implementation: map every criterion to a test and tag each test with the criteria it covers, find the interface without learning its behaviour, keep tests valid as the product grows, and keep the test environment declared. Use when writing end-to-end or acceptance tests."
---

## Every criterion becomes a test

- **At least one test per acceptance criterion.**
- **Tag each test with the numbers of the criteria it drives,** in the marker your brief gives, on
  the test itself: in its title or a comment beside it. A tag is what lets anyone, or anything,
  read the coverage without reading the tests. Every criterion carries at least one tag, and no tag
  names a criterion the change does not have.
- **Tag only what the test drives.** A test that sets up criterion 2 to check criterion 3 covers 3.
- **Cover the edges a criterion names.** Don't invent requirements it doesn't state.
- **Never skip a criterion the outside can't reach,** such as a crash mid-request. Drive it
  through the test hooks the project provides for that.

## Find the interface, not the behaviour

When no document names a route, a flag or a page, look up its **name** where the interface is
declared, and stop there. What the code *does* with it is exactly what your test must not assume.

What your setup must match is interface too: the tables and columns your test seeds or reads, the
columns an import file needs, the config keys, the input formats. Read them where they are declared
(the schema or migrations, the documented formats, another test's working fixture) before writing
the setup, never guess them. A test that fails on its own setup has measured nothing.

**Build every stand-in for another system from a real sample of it.** Start each page, API response
or file your test serves in place of a third party from a real capture, then trim or vary it for the
case. Never write one from what the format probably looks like: invented markup tests only that the
product agrees with whoever invented it. If you have no capture to start from, say so in your
summary.

## Tests that stay valid

Tests that live alongside every other change's tests, and re-run after each one, must be:
- **Isolated:** they create their own data with unique names, and never depend on another test's
  data or on run order.
- **Waiting on conditions, never on time:** a response, an element, a log line.
- **Tolerant of what the criterion leaves open:** wording, layout, ordering and ids it never
  promised. Those will change.

## Other changes' tests aren't yours

Tests that came with another change hold the behaviour it shipped. **Change one only when one of
your criteria changes that behaviour,** and name the criterion. A test of another change that now
fails is a finding about the product, not a test to bring in line.

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