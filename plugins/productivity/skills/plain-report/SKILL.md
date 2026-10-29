---
name: plain-report
description: "Write anything another reader acts on (a hand-over, findings, a verdict, a summary, PR text, a notice) so it is short, factual and quick to act on: outcome first, facts over narrative, nothing the reader can't use. Use for every report, hand-over field or message you write for someone else."
---

# Plain report

The reader has to act on what you write, or check it. Every line costs them time. Give them the
result, the facts behind it, and nothing else.

## Outcome first

The first line is the result: the verdict, what changed, or what is blocked. Then only what the
reader needs to act on it or check it.

> Bad: "I started by reading the handler, then traced the call into the store, and after some
> digging it turned out the retry loop was the problem, so I fixed it."
>
> Good: "Fixed: the retry loop in `store.py:88` never reset its counter. Test
> `test_retry_resets` covers it."

## Facts over narrative

- **Point at the thing.** `file:line`, the number, the exact quote, the command, the id. A reader
  can check `api.py:142 returns 500 on an empty body`; they can't check "the API has some issues
  with edge cases".
- **No process story.** Leave out what you looked at first and how you got there. Give the result
  and the evidence.
- **No retelling.** Don't restate the task, the request or anything else the reader already has.

## Shape and length

- **One finding per line,** or a short list. Use a table when the items share fields (id, status,
  where).
- **A summary is a line or two.** If it needs more, the extra belongs in a list below it or in
  the file it came from.
- **Point to details, don't paste them.** Name the log, file or commit where the details live.
  Quote only the line that matters.
- **Structured fields follow the same rules.** A JSON `summary` is a sentence, not an essay. A
  `reason` names the cause. Each list item is one fact.

## Nothing the reader can't use

- **No rationale for routine choices.** Explain a choice only when the reader might disagree with
  it or need to undo it.
- **No recap, no closing line.** Stop when the facts are out. No "In summary", no "Let me know
  if…", no "Hope this helps".
- **No empty hedges.** Cut "may potentially", "it seems", "should probably" when nothing is in
  doubt. When something is uncertain, say it once and say it exactly: what is unknown and what
  would settle it.

> Bad: "This might possibly cause issues in some cases."
>
> Good: "Unverified: whether `sync()` runs before `close()` on shutdown. A test that kills the
> process mid-write would settle it."

## Plain sentences

- **Plain words.** "use", not "leverage" or "utilize". "is" and "has", not "serves as", "stands
  as", "boasts" or "features". Drop AI vocabulary: crucial, delve, enhance, robust, seamless,
  pivotal, landscape, showcase, underscore.
- **Active voice; name the actor.** "The loader rejects the file", not "the file is rejected".
- **One idea per sentence.** If the reader has to backtrack to parse a sentence, split it.
- **Say what it does, not how it feels.** "a column rename fails the build", not "keeps the
  schema safe". If a sentence can't be restated as a fact, an instruction or a number, cut it.
- **Cut filler and adverbs.** "In order to" becomes "to". "It is important to note that" goes.
  "Significantly faster" becomes the measured number.
- **No puffery or chatbot phrases.** No "robust solution", "great question", "Certainly!",
  "Found it!".
- **One name per thing.** Pick a term and repeat it. Don't cycle "item", "task" and "ticket" for
  the same object.
- **Plain formatting.** Sentence-case headings. No decorative emoji. Bold only what the reader
  must not miss.

## Before you send

Read it as the reader. Cut every line they would skip. Check the first line alone tells them
the outcome.
