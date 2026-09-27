# agent-marketplace

A Claude Code, Codex, and Hermes-compatible plugin marketplace. Each plugin is
a separate install, so you can take one and leave the rest.

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

Each plugin is a portable Agent Plugin package and can be installed from its
subdirectory:

```sh
hermes plugins install charlessuo/agent-marketplace/plugins/productivity --no-enable
hermes plugins enable productivity

hermes plugins install charlessuo/agent-marketplace/plugins/software-development --no-enable
hermes plugins enable software-development
```

Codex reads the existing Claude-compatible marketplace and loads the same
`skills/` files, so no duplicate skill tree or symlink is needed.

## Plugins

| Plugin | Version | What it does |
| --- | --- | --- |
| `productivity` | 0.3.0 | Focused communication and editing, including `i-have-adhd`, `unslop`, and upstream `grilling`. |
| `software-development` | 0.1.0 | Upstream engineering skills for specs, TDD, code review, architecture, and domain modeling. |

## Layout

```
.claude-plugin/marketplace.json   the catalog Claude Code and Codex read
plugins/<plugin>/
  .claude-plugin/plugin.json      the shared plugin manifest
  plugin.json                    Agent Plugins v1 manifest for Hermes
  skills/<skill>/SKILL.md         shared by Claude Code and Codex
scripts/                          validation and version helpers used by CI
skill-sources.json                imported-skill source commits and fingerprints
```

Two rules the CI enforces, both of which are easy to get wrong:

1. A skill's directory name must equal the `name` in its SKILL.md frontmatter.
2. A plugin's `name`, `description`, and `version` must be identical in
   `plugin.json` and in its `marketplace.json` entry.

## Adding a skill

Create `plugins/<plugin>/skills/<skill>/SKILL.md` with frontmatter:

```markdown
---
name: my-skill
description: One line telling the agent when to reach for this.
---
```

Then bump the plugin `version` in both the plugin manifest and marketplace
entry, and open a PR.

## Adding a plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json` with `name`,
   `description`, `version`, and `author`.
2. Add a matching entry to the `plugins` array in
   `.claude-plugin/marketplace.json` with `"source": "./plugins/<name>"`.
3. Add skills under `plugins/<name>/skills/`.

Run `python3 scripts/validate_marketplace.py` before pushing.

## Imported skill sources

Vendored skills keep their upstream repository, source directory, import commit,
and content hash in [`skill-sources.json`](skill-sources.json). This makes
upstream changes and local customizations visible without changing the imported
files. Run the crawler from the repository root:

```sh
python3 scripts/check_skill_sources.py
```

It checks each configured source tree and reports upstream updates, local edits,
missing source metadata, and upstream skills not imported into this repo. Use
`--strict` to return a nonzero status when any finding exists. To check existing
clones without network access, pass `--checkout https://github.com/mattpocock/skills.git=/path/to/skills-clone`
for each repository.

## Releases

Release automation is **off by default** while the repo is being set up. Linting
still runs on every pull request; only tagging and publishing are gated.

To turn it on later, add a repository variable under
Settings -> Secrets and variables -> Actions -> Variables:

| Variable | Value |
| --- | --- |
| `ENABLE_AUTO_RELEASE` | `true` |

With it set, merging a `version` bump to `main` creates the tag
`<plugin>--v<version>` and publishes a GitHub Release holding a zip of the
plugin plus a zip of each skill. Nothing is tagged until the manifests validate.

Manual runs from the Actions tab work whether or not the variable is set, and
both workflows default to a dry run when started by hand.

Tag format matches what `claude plugin tag` produces, so you can also cut a
release yourself:

```
claude plugin tag ./plugins/productivity --push
```

## Trying it before enabling

1. Run **auto-tag** from the Actions tab with `dry_run` checked. It validates
   the manifests and prints the tags it would create, without creating them.
2. Run **release-skills** with `tag: productivity--v0.2.0` and `dry_run`
   checked. It builds the archives and release notes and attaches them to the
   run as a downloadable artifact, without publishing a release. The tag does
   not need to exist yet; a dry run falls back to the current branch and says so.
3. Download the run artifact and confirm the zips look right.
4. Set `ENABLE_AUTO_RELEASE` to `true`.

## Workflows

`skill-lint` runs on every pull request and is not gated. It validates the
manifests, checks that every SKILL.md has a name and description, and rejects
directory or version mismatches. A second advisory job runs the upstream
`claude plugin validate` and reports without blocking merges.

`auto-tag` runs on pushes to `main` once `ENABLE_AUTO_RELEASE` is set, and on
manual dispatch at any time. It reads each plugin's version, creates any tag
that does not exist yet, and calls the release workflow directly. Calling it
in-process sidesteps the GitHub rule that a tag pushed with `GITHUB_TOKEN`
cannot trigger another workflow, so no personal access token is needed.

`release-skills` runs on a call from `auto-tag`, on manual dispatch, or on a
tag push once `ENABLE_AUTO_RELEASE` is set. Gating the tag push means a stray
tag cannot publish by accident. The job rechecks the tagged tree, confirms the
tag matches the manifest version, builds the archives with a SHA256SUMS file,
and publishes the release unless it is a dry run.

## Repository settings

Both release workflows need write access to create tags and releases. Under
Settings -> Actions -> General -> Workflow permissions, select
"Read and write permissions". Without it they fail with a 403.
