# software-development-pipeline

Software development workflows for turning requirements into work, implementing
changes with TDD, reviewing code, authoring acceptance tests, evaluating QA
results, and distributing work. The adapted `to-spec`, `tdd`, and `code-review`
skills retain upstream provenance from
[mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering).
Source commits and content fingerprints are recorded in
[`skill-sources.json`](../../skill-sources.json).

## Install

### Claude Code

```
/plugin marketplace add charlessuo/agent-marketplace
/plugin install software-development-pipeline@agent-marketplace
```

### Codex

```sh
codex plugin marketplace add charlessuo/agent-marketplace
codex plugin add software-development-pipeline@agent-marketplace
```

### Hermes

```sh
hermes plugins install charlessuo/agent-marketplace/plugins/software-development-pipeline --no-enable
hermes plugins enable software-development-pipeline
```

## Skills

- `to-spec` — turn requirements into a spec, decision records, and work items.
- `tdd` — implement one behavior-focused vertical slice at a time.
- `code-review` — review changes against project standards and the spec.
- `qa-author` — write black-box acceptance tests from criteria.
- `qa-verdict` — assess a test run and report its QA verdict.
- `distribute-work` — select and assign the next ready item of work.
- `system-design` — coach system-design thinking like an interviewer while scoping a real system: a checklist framework, blind-spot questions, and a senior-level grading rubric.

From the repository root, run `python3 scripts/check_skill_sources.py` to find
local edits, upstream updates, and upstream skills in these source trees that
are not imported here.
