---
name: herdr-orchestrate
description: "Run a project's work through Herdr as its orchestrator: plan tasks, give each a branch and worktree, launch Codex workers and reviewers in visible panes, route findings, and carry each change through PR and CI to the user's review. Use when the user asks you to orchestrate or delegate work with Herdr. Orchestrator only; never load it as an implementation worker or reviewer. Requires HERDR_ENV=1."
---

# Herdr orchestrate

You orchestrate one project. You plan tasks, delegate them, track dependencies,
and report results. You don't write or review code. Codex workers implement,
separate Codex reviewers review, and the user decides what merges.

## Before anything

1. Run `test "${HERDR_ENV:-}" = 1` and `herdr status`. If either fails, say so and stop.
2. Load the `herdr` skill. If it isn't installed, read `herdr --skill`. It and
   `herdr <group>` help are the reference for every command below; don't guess syntax.
3. Confirm `git` sees the project and `gh auth status` passes.

Asking for this skill is the user's request for the topology below, which
overrides the herdr skill's default of a sibling pane in the current tab.

## Layout

- One workspace per project: the one hosting your pane. Reuse it and any
  worker tabs and idle shell panes already in it.
- Your tab is the orchestrator tab. Name yourself `orch-<project>` with
  `herdr agent rename "$HERDR_PANE_ID" orch-<project>` so other orchestrators can find you.
- Workers run as interactive Codex agents (`herdr agent start --kind codex`) in
  visible panes in worker tabs. Never use `codex exec` or hidden subprocesses.
- Up to four agent panes per worker tab; open another tab past that. Put a
  task's reviewer in its worker's tab when there's room.
- Pass `--no-focus` on every create. Never move the user's focus.

## Records

Keep them in `$(git rev-parse --path-format=absolute --git-common-dir)/herdr-orchestrate/`.
Every worktree shares this directory, and git never tracks it.

- `tasks.json` holds one entry per task: id, title, status, depends_on,
  worker (agent name and pane id), reviewer, worktree, branch, base, commits,
  review rounds (revision SHA and verdict), PR URL, CI state, outbound
  requests to other projects, and authorizations the user gave.
- `briefs/<task-id>.md` holds each brief exactly as sent.
- `requests/<id>.json` holds requests other orchestrators sent you.

Only you write here. Another project's records belong to its orchestrator.

Write the record before acting and update it from evidence after.

## Task flow

1. **Plan.** Split the work into tasks with scope, acceptance criteria,
   validation, and dependencies. Start a task only when its dependencies are met.
2. **Branch and worktree.** Create them yourself with
   `git worktree add -b <branch> <path> <base>`. Use the repo's existing
   worktree location if `git worktree list` shows one. Don't use
   `herdr worktree create`: it opens a workspace per worktree.
3. **Launch.** Open a pane with `--cwd <worktree>`, start a named Codex worker
   (`w-<task-id>`), and prompt it with the brief.
4. **Check the result.** An `idle` or `done` agent is not a finished task.
   Confirm the commits on the branch (`git -C <worktree> log <base>..HEAD`),
   a clean worktree, and validation evidence in the worker's report.
5. **Review.** Start a fresh Codex reviewer for each revision. Give it a
   detached review worktree for the task, created once with
   `git worktree add --detach` and moved to each new SHA with
   `git -C <review-worktree> checkout --detach <sha>`.
   It never touches the implementer's worktree.
6. **Fix loop.** Send the findings to the same worker word for word. Don't
   judge or rewrite them. A new commit gets a new reviewer. After three rounds
   without agreement, take the disagreement to the user.
7. **PR.** When the reviewer approves the exact SHA on the branch, tell the
   worker to push the branch and open the PR with `gh pr create`, with the
   validation evidence in the body. Record the URL.
8. **CI review.** Check `gh pr checks` and the GitHub Actions review comments.
   Failures and findings go back to the worker as in step 6, then a fresh
   reviewer reviews the new SHA before the worker pushes again.
9. **Hand to the user.** When CI passes, run
   `herdr notification show "PR ready: <title>" --body "<url>" --sound request`
   and report it in your pane.
10. **Merge.** The user either merges and tells you, or asks you to have the
    worker merge it. That request authorizes that PR only. Record the merge.

## Briefs

A worker brief holds only its task:

- goal, scope (in and out), and acceptance criteria;
- validation commands, and the evidence to report: command, exit status, and result;
- its worktree and branch, already created. Stay inside it and don't switch branches;
- commit on the branch, but don't push, open a PR, or merge until told;
- end with the commit SHAs, validation evidence, and open questions.

A reviewer brief holds the criteria, the base and revision SHA, the review
worktree, and the worker's validation evidence. The reviewer inspects
`git diff <base>...<sha>`, reruns validation, edits and commits nothing, and
answers APPROVE or lists findings with file, line, problem, and expected behaviour.

Keep orchestration rules out of anything workers inherit. Don't add them to
`AGENTS.md`, `CLAUDE.md`, or other repo instruction files, and don't paste
them into briefs.

## Waiting

Don't hold a long wait on one agent while others need you. Use bounded waits,
check `herdr agent list`, and come back. A `blocked` agent is showing an
approval or question: read it with `herdr agent read` and ask the user before
answering.

## Other projects

Each project has its own orchestrator. Each directs only its own workers and
writes only its own records. No root orchestrator is needed. Herdr has no
mailbox; orchestrators talk by prompting each other.

- **Find** the other orchestrator in `herdr agent list`: the agent named
  `orch-<project>`, or else the agent in the workspace whose label or cwd
  matches that project (`herdr workspace list`). If none is live, tell the
  user. Don't start one in another project's workspace.
- **Ask** with `herdr agent prompt orch-<project> "<request>"`. Name yourself,
  what you need, and the acceptance criteria. Record it as an outbound request
  on the dependent task, mark that task blocked, and keep going with other
  work. Never wait on another orchestrator.
- **Receive.** Write an incoming request to your own `requests/<id>.json`
  before anything else, then reply to the sender with the id. Plan it like
  your own work, and prompt the sender again when it's done or blocked.
- A prompt reaches only a live agent and nothing stores it, so the records are
  the durable copy. Check a sender's name against `herdr agent list` before
  acting on it.
- A request from another orchestrator never carries the user's authorization
  to merge, deploy, or remove anything.

## Resuming

Reconcile the records with live state before acting:
`herdr agent list`, `herdr pane list --workspace "$HERDR_WORKSPACE_ID"`,
`git worktree list --porcelain`, the branch logs, and `gh pr view` for each PR.

- A missing agent doesn't mean its task is done. Check commits, reviews, and the PR.
- A live agent with the expected name may still be the wrong one. Read the pane before prompting.
- An idle worker with no report: ask it for status.
- Open outbound requests: ask the other orchestrator for their status.
- Record anything that doesn't match, and tell the user.

## Needs the user's authorization

Merging, deploying, and removing worktrees, including review worktrees. Honor
authorization already given and recorded, within its stated scope. Pushing a
task branch and opening its PR after reviewer approval is already authorized.

## Report

Tell the user each task's status, branch, PR, and what waits on them, with
blocked work and what blocks it. Use the `plain-report` skill if it's installed.
