# productivity

Focused communication, editing, and collaborative decision-making skills for Claude Code, Codex, and Hermes.

## Install

### Claude Code

```
/plugin marketplace add charlessuo/agent-marketplace
/plugin install productivity@agent-marketplace
```

### Codex

```sh
codex plugin marketplace add charlessuo/agent-marketplace
codex plugin add productivity@agent-marketplace
```

### Hermes

```sh
hermes plugins install charlessuo/agent-marketplace/plugins/productivity --no-enable
hermes plugins enable productivity
```

## Skills

### i-have-adhd

Shapes responses so the next action is easy to find and execute. It leads with
the action, numbers multi-step work, suppresses tangents, and keeps progress
visible across turns. Invoke it explicitly with `/i-have-adhd` in Claude Code
or `$i-have-adhd` in Codex. Vendored from
[the canonical skill directory](https://github.com/ayghri/i-have-adhd/tree/main/skills/i-have-adhd)
under the MIT license. Its original import commit is unknown; the tracker
records the confirmed source and flags the missing historical revision.

### unslop

Removes AI tells from writing. It covers 31 patterns across content, language,
style, filler, and jargon, then asks for a self-audit pass. The description is
marked "must always apply", so Claude loads it for any writing or editing task
rather than waiting to be asked.

### grilling

Runs a structured interview to stress-test a plan, decision, or idea. Vendored
from [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)
under the MIT license. See [`skill-sources.json`](../../skill-sources.json) for
the imported commit and content fingerprint, and run
`python3 scripts/check_skill_sources.py` from the repository root to compare it
with upstream.

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for source and license
notes for the bundled skills.
