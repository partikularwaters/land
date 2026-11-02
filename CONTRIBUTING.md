# Contributing to land

## Commits

Every commit request follows the personal `land` skill, which applies the rules in this section.

### Subject and body

Write commit subjects and descriptions from the author's perspective.
Describe the change directly: what changed, why, and how it was verified. Do not narrate your internal process or format the commit as a status report.

Use Conventional Commits in the imperative mood: `<type>(<optional-scope>): <what changed>`.
Types: `feat`, `fix`, `docs`, `style`, `chore`, `refactor`, `test`, `ci`, `build`, `perf`.

Mark breaking changes with a `!` after the type (such as `feat!:`) or with a `BREAKING CHANGE:` footer.

Keep the body focused on explaining what changed and why. Omit the body when the subject line is clear on its own.

Place footers after a blank line below the body. Include `BREAKING CHANGE:` only for breaking changes, and add issue references (`Closes #n` or `Refs #n`) only when a relevant issue exists.

### Assisted-by trailer

Keep the configured human Git identity as the commit author.

When an AI assistant materially shaped the commit, add one trailer:

```text
Assisted-by: <provider or product> (<model, if known>)
```

Examples:

```text
Assisted-by: Anthropic Claude Code (Haiku 5.5)
Assisted-by: Google Antigravity (Gemini 3.8 Flash)
Assisted-by: Meta Muse (Muse Spark 1.3)
Assisted-by: OpenAI Codex (GPT-6.1 Luna)
```

Name the actual product and model when available. If the model is unknown, name the product only. Repeat the trailer when multiple assistants materially contribute.

“Materially shaped” means the assistant produced or substantially revised code, documentation, tests, architecture, or analysis embodied in the commit. Routine formatters, spell-checkers, and autocomplete do not require attribution.

Invoking the `land` skill for a commit also counts as that signal.

Do not use `Co-authored-by`, invent an AI email address, or describe the AI as the commit author unless the repository owner explicitly requests co-authorship and the assistant has a real, verifiable GitHub-linked identity.

### Staging

Stage specific paths only, and never use `git add -A`. Check `git diff --staged` before committing, and scan staged changes for secrets. Do not stage a file that mixes in-scope and out-of-scope edits. Never force-push as part of a commit.

## Pre-commit checks

Before committing, run:

```bash
python3 scripts/verify_skill.py
```
