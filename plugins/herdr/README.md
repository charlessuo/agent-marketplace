# herdr

Runs a project's work through Herdr: Claude orchestrates,
Codex workers implement in their own branch and worktree, separate Codex
reviewers review, and each approved change goes through a PR and GitHub Actions
before it reaches you.

## Requirements

- Herdr 0.9.5 or later, with Claude running inside a Herdr pane (`HERDR_ENV=1`).
- Herdr's own `herdr` skill installed. `herdr --skill` prints it. This plugin
  relies on it for command details and doesn't copy them.
- The Codex CLI, and `gh` signed in to the repository's GitHub account.

## Install

Install it only where the orchestrator runs. Codex workers shouldn't see the
orchestration rules, so don't add it to the Codex installation the workers use.

```
/plugin marketplace add charlessuo/agent-marketplace
/plugin install herdr@agent-marketplace
```

## Usage

Open the project in Herdr, start Claude in a pane there, and ask:

```
/herdr:herdr-orchestrate Add rate limiting to the public API and a
`--dry-run` flag to the import CLI. Two tasks, independent.
```

Claude then:

1. names itself `orch-<project>` and plans the two tasks;
2. creates a branch and worktree for each, opens a worker tab, and starts a
   Codex worker per task in visible panes without taking your focus;
3. starts a fresh Codex reviewer for each revision and sends findings back
   until the reviewer approves;
4. has the worker push and open a PR, sends GitHub Actions failures back
   through the same loop, and sends you a Herdr notification when CI passes.

Merge on GitHub and tell Claude, or ask it to have the worker merge. Claude
asks before merging, deploying, or removing a worktree, unless you already
authorized it.

Task records live in `<git-common-dir>/herdr-orchestrate/`, so after a restart
Claude checks them against live agents, worktrees, and PRs before continuing.

## Skills

- `herdr-orchestrate`: the orchestrator's workflow. It covers layout, task
  records, worker and reviewer briefs, the review and PR loop, coordination
  with other projects' orchestrators, and resuming.
