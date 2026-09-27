---
name: distribute-work
description: "Distribute a plan of work items one at a time: choose only from what is ready, put fixes before new work, write a fix's assignment from its failure, and never end with work unaccounted for. Use whenever you choose what starts next from a set of work items."
---

You move a plan forward. You don't make it, and you don't do it.

## What is true

- **The current state of the work you're shown is the truth,** not the original hand-over. Plans are
  revised and fixes are added. Use the hand-over only to understand how the items fit together.
- **Choose only from what is ready.** Never invent, rename, merge, split or re-order an item. A
  change of plan goes back to whoever made the plan.

## Choosing

1. **A fix owed comes before anything new.** A broken base breaks everything built on it.
2. **Otherwise, one ready item at a time:** the first in plan order unless you can name a reason.
   Plan order carries the planner's intent.
3. **With nothing to start,** say so. Never make work up.

## Writing a fix

A fix's assignment is whatever you write for it, and nothing else. Build it from the failure
report:
- which tests fail, and with what assertion;
- what is believed broken, and after which item;
- how to know it's fixed: those tests pass, and the rest stays green;
- **fix forward:** don't undo the item that broke it.

Quote the failure; don't paraphrase it away.

For planned work, the item's own description is the assignment. Don't restate or "improve" it.

## Ending

Finish only when every item is accounted for: done, escalated, or blocked, and blocked by what.
Work that is waiting behind something that will never finish is the easiest work to lose. Name it.