---
name: triage
description: "Verify each finding a reviewer raised before anyone acts on it: check the claim where it points, give it exactly one verdict and one route, and log every finding with its evidence. Use when your task is to triage someone else's review findings."
---

A finding is a claim that something goes wrong. Your job is to find out whether it does, before it
costs anyone a round. You don't review the change again and you don't fix it.

## Carried findings first

If earlier rounds have a triage log, check each finding against it before anything else. **Same
place, same claim, and the code there still reads as the logged row describes:** keep that row's
verdict and route, start its evidence with `carried:`, and don't verify it again. If the code has
changed since, it is a new finding: verify it.

## Verify each claim

- **Go to the place the finding cites.** Does the bad outcome it describes actually happen there?
  Read past the changed lines, into callers and the guards upstream, until you can answer yes or
  no.
- **Judge the problem, not the proposed fix.** A plausible fix doesn't make a problem real.
- **A different finding about nearby code doesn't settle this one.**
- **Code that fails loudly on a situation nobody showed the program can reach is correct,** not a
  defect.
- **Check a claim about stored data against the data.** When you have a copy, query it; the count
  is your evidence. A path for data that doesn't exist harms nobody.
- **Ignore the severity the reviewer gave.** It lacked the context to grade.

## One verdict per finding

- **`real`:** the bad outcome happens. Evidence: what you verified, and where.
- **`false`:** you checked, and it doesn't happen at the cited place. Evidence: what disproves
  *this* claim, such as the code that prevents it, a count, or the requirement's own words. A true
  fact about nearby code that doesn't disprove the claim doesn't count.
- **`unsure`:** you couldn't tell. Evidence: what would settle it. Use this only when the code and
  the data leave the question open. When they're enough to decide, decide.

## One route per finding

- **`fix`:** real, caused by this change, and the requirement says what right looks like. This is
  the only route that sends work back.
- **`ask`:** real and caused by this change, but the requirement doesn't settle the fix. It reads
  two ways, or the fix needs a decision nobody made. Don't guess the intent unless only one
  reading is possible. Evidence: the question, written for the person who owns the requirement,
  so they can answer it in a line.
- **`defer`:** real, but not this change's problem: it was there before the change. Also an
  `unsure` finding that would matter if true. Evidence: why it's real, or what would settle it.
- **`reject`:** every `false` finding, on its refutation. Also a real finding that is minor,
  unlikely in everyday use, and whose fix would add guards, branches or parameters. Also anything
  the requirement itself excludes: an input outside a list it calls complete, or something it puts
  out of scope. Reject for scope only when the requirement says so, never because the change
  happens not to touch that code.

**Never route a `false` finding anywhere but `reject`, and never route an `unsure` one to `fix`.**

## Log every finding

One row per finding, in the order they were raised: its id, verdict, route and evidence in a
sentence or two. Never drop a finding, fold two into one, or add one of your own. If you notice a
problem nobody raised, say so in your summary; it isn't a row.

## Routes cascade

- **Any `ask`:** the whole set waits for the person. Fixes built around an open question may have
  to be undone.
- **Otherwise, any `fix`:** the work goes back with only the `fix` findings.
- **Otherwise:** nothing goes back, and the work moves on. Deferred findings are kept as notes.
