# software-development

Engineering skills for specification, TDD, code review, architecture, and
domain modeling. The skills are vendored from
[mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering)
under the MIT license. Their upstream commit and content fingerprints are
recorded in [`skill-sources.json`](../../skill-sources.json).

## Install

### Claude Code

```
/plugin marketplace add charlessuo/agent-marketplace
/plugin install software-development@agent-marketplace
```

### Codex

```sh
codex plugin marketplace add charlessuo/agent-marketplace
codex plugin add software-development@agent-marketplace
```

### Hermes

```sh
hermes plugins install charlessuo/agent-marketplace/plugins/software-development --no-enable
hermes plugins enable software-development
```

## Skills

- `to-spec` — turn the current conversation into a project spec.
- `tdd` — a reference for behavior-focused test-driven development.
- `code-review` — review changes against repository standards and the originating spec.
- `codebase-design` — shared vocabulary and principles for deep module design.
- `improve-codebase-architecture` — identify architecture improvements and report them.
- `domain-modeling` — build and maintain the project domain model.

From the repository root, run `python3 scripts/check_skill_sources.py` to find
local edits, upstream updates, and upstream skills in these source trees that
are not imported here.
