# land

A personal, cross-project git-commit skill for AI coding assistants.

AI coding assistants often carry default commit instructions that conflict with a project's real guidelines. For example, a system prompt might instruct the assistant to add a generic `Co-authored-by` trailer or explain its internal thought process in the commit body, even when the project's `CONTRIBUTING.md` specifies something completely different.

`land` fixes that by establishing a predictable commit workflow:
- It reads the project's `CONTRIBUTING.md` and follows its attribution rules and pre-commit checks.
- If the project has no AI attribution policy, it falls back to a clean `Assisted-by: <tool>` trailer without cluttering git logs.
- It formats commit messages with Conventional Commits, drafts concise descriptions from staged changes, and prevents accidental blind staging.

---

## Commit Workflow

1. **Resolve Attribution Convention:** Target repository `CONTRIBUTING.md` takes precedence over all runtime defaults.
2. **Resolve Mode:**
   - `land` (no arguments): Default draft mode. Formats and displays the draft, waiting for explicit approval.
   - `land commit`: Auto-commit mode. Commits immediately without an extra confirmation prompt.
   - `land push`: Commit and push mode. Commits immediately and pushes to the current upstream branch.
3. **Staging and Pre-Commit Verification:**
   - Stages specific paths only, never using blind `git add -A`.
   - Scans staged diffs for credentials or secrets.
   - Discovers and runs documented pre-commit checks (such as linters, formatters, and test suites).
4. **Draft Commit Message:**
   - Formats the subject line using Conventional Commits (`<type>(<optional-scope>): <what changed>`).
   - Keeps the body limited to material context, omitting assistant process narration.
   - Appends conditional issue references and the resolved `Assisted-by:` trailer as the final line.
5. **Mode Branching:** Executes the appropriate action based on the selected mode.

---

## Repository Structure

```text
.
├── SKILL.md                 # Core skill specification and agent prompt instructions
├── README.md                # Project documentation and developer reference
├── CONTRIBUTING.md          # Repository attribution contract and pre-commit checks
├── .gitignore               # Git exclusions for OS, editor, and Python artifacts
└── scripts/
    └── verify_skill.py      # Automated validation engine for skill syntax and rules
```

---

## Installation and Runtime Integration

Agent runtimes discover skills in `~/.agents/skills/land` (macOS / Linux) or `%USERPROFILE%\.agents\skills\land` (Windows).

### Option A: Direct Clone
Clone the repository directly into your agent skills directory:

**macOS / Linux:**
```bash
git clone https://github.com/<owner>/land.git ~/.agents/skills/land
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/<owner>/land.git "$HOME\.agents\skills\land"
```

### Option B: Local Development Symlink
If you are developing `land` from a standalone workspace, link the repository into your global agents directory:

**macOS / Linux:**
```bash
ln -sfn "$(pwd)" ~/.agents/skills/land
```

**Windows (PowerShell with Developer Mode or Administrator):**
```powershell
New-Item -ItemType SymbolicLink -Path "$HOME\.agents\skills\land" -Target (Get-Location)
```

**Windows (Command Prompt):**
```cmd
mklink /D "%USERPROFILE%\.agents\skills\land" "%CD%"
```

---

## Verification

Run the verification engine to validate frontmatter, canonical types, required headers, and convention resolution logic:

**macOS / Linux:**
```bash
python3 scripts/verify_skill.py
```

**Windows:**
```powershell
python scripts/verify_skill.py
```
