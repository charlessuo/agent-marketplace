# productivity

Focused communication and editing skills for Claude Code and Codex.

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

## Skills

### i-have-adhd

Shapes responses so the next action is easy to find and execute. It leads with
the action, numbers multi-step work, suppresses tangents, and keeps progress
visible across turns. Invoke it explicitly with `/i-have-adhd` in Claude Code
or `$i-have-adhd` in Codex. Vendored from
[ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) under the MIT
license.

### unslop

Removes AI tells from writing. It covers 31 patterns across content, language,
style, filler, and jargon, then asks for a self-audit pass. The description is
marked "must always apply", so Claude loads it for any writing or editing task
rather than waiting to be asked.
