---
name: reset-workflow
description: >
  Resets the profile files and/or documents folder to a blank template/fresh state.
  Triggers on: reset, /reset, reset setup, wipe profile, clear candidate data
---

# Reset Candidate Profile Data

You are resetting parts of the job search framework back to a blank state so the user can start fresh with the setup workflow.

**This command is destructive.** Nothing is deleted until the user explicitly confirms. Follow these steps exactly in order.

---

## Step 0: Parse Scope from Arguments

Check for a scope keyword in the user input:
- `profile` — clears candidate profile data from skill files only
- `documents` — deletes user-provided files from the `documents/` folder only
- `all` — both of the above

If no recognized scope keyword is specified, ask:

> **What would you like to reset?**
>
> - **`profile`** — Clears candidate data from the skill files (profile, behavioral, STAR examples, profile statements). The framework structure and writing rules are preserved. Use this to re-run the setup workflow from scratch.
>
> - **`documents`** — Deletes all files you've placed in the `documents/` folder (CV PDFs, LinkedIn export, diplomas, references, past applications). The folder structure and `README.md` are preserved.
>
> - **`all`** — Both of the above.
>
> Reply with `profile`, `documents`, or `all`.

Wait for the user's response before continuing.

---

## Step 1: Show Exactly What Will Be Cleared

Before doing anything, show the user precisely what will be wiped.

### If scope includes `profile`:

Read the current state of these files and report whether each has content or is already empty:
- `.agents/skills/job-application-assistant/01-candidate-profile.md`
- `.agents/skills/job-application-assistant/02-behavioral-profile.md`
- `.agents/skills/job-application-assistant/05-cv-templates.md` *(profile statements section only)*
- `.agents/skills/job-application-assistant/07-interview-prep.md` *(STAR examples and STAR candidates sections only)*

Present as:

```
## Profile reset will clear:

- 01-candidate-profile.md — [has content / already empty]
  Full file will be replaced with a blank template.

- 02-behavioral-profile.md — [has content / already empty]
  Full file will be replaced with a blank template.

- 05-cv-templates.md — [has profile statements / already blank]
  Profile statement templates will be cleared. LaTeX structure and tailoring guidelines are preserved.

- 07-interview-prep.md — [has STAR examples / already blank]
  STAR examples and any STAR candidate stubs will be cleared. Framework, tough questions, and roleplay guidelines are preserved.

The following files are NOT touched (they contain framework rules, not candidate data):
  - 03-writing-style.md
  - 04-job-evaluation.md
  - 06-cover-letter-templates.md
```

### If scope includes `documents`:

Use Glob to list all files present in `documents/cv/`, `documents/linkedin/`, `documents/diplomas/`, `documents/references/`, and `documents/applications/`. Present as:

```
## Documents reset will delete:

documents/cv/
  - [filename] or "(empty)"

documents/linkedin/
  - [filename] or "(empty)"

documents/diplomas/
  - [filename] or "(empty)"

documents/references/
  - [filename] or "(empty)"

documents/applications/
  - [subfolder/filename] or "(empty)"

documents/README.md — NOT deleted (instructions file)
```

If all document subfolders are already empty, state "All document subfolders are already empty — nothing to delete." and skip the confirmation step for this scope.

---

## Step 2: Require Explicit Confirmation

Present the confirmation prompt:

> **This cannot be undone.**
>
> Type **`RESET`** (all caps) to confirm, or anything else to cancel.

Wait for the response.
- If the response is exactly `RESET`: proceed to Step 3.
- If the response is anything else: abort and tell them "Reset cancelled. Nothing was changed."

---

## Step 3: Execute the Reset

### Profile reset

**For `01-candidate-profile.md`**, replace the file content with:

```markdown
# Candidate Profile

<!-- Run the setup workflow to populate this file -->

## Identity

## Education

## Professional Experience

## Independent Projects

## Technical Skills

## Publications

## Awards

## References
```

**For `02-behavioral-profile.md`**, replace the file content with:

```markdown
# Behavioral Profile

<!-- Run the setup workflow to populate this file -->

## Overview

## Strongest Behavioral Traits

## How I Work Best

## Growth Areas

## Mapping to Job Posting Language

## Management Style Preferences

## Using This in Applications
```

**For `05-cv-templates.md`**, locate the section that begins with `**Profile statement templates` and extends through the role-specific template blocks. Replace only that section with:

```markdown
**Profile statement templates:**

<!-- Run the setup workflow to populate role-specific profile statements -->
```

Leave all other content in `05-cv-templates.md` intact.

**For `07-interview-prep.md`**, locate and remove:
- The entire `## Ready-Made STAR Examples` section and all numbered STAR examples under it
- Any `## STAR Candidates (Complete Manually)` section

Replace with:

```markdown
## Ready-Made STAR Examples

<!-- Run the setup workflow to populate STAR examples from your actual experience -->
```

Leave all other content in `07-interview-prep.md` intact.

### Documents reset

For each non-empty document subfolder, delete all files within it. Do not delete the folder itself, and do not delete `documents/README.md`.

You can clean them via powershell or command line:
```powershell
Remove-Item -Path documents/cv/* -Force
Remove-Item -Path documents/linkedin/* -Force
Remove-Item -Path documents/diplomas/* -Force
Remove-Item -Path documents/references/* -Force
Remove-Item -Path documents/applications/* -Recurse -Force
```

---

## Step 4: Confirm What Was Done and Next Steps

After the reset is complete, report:

```
## Reset complete

### Cleared
[List each file/folder that was actually modified or cleared]

### Unchanged
[List anything that was already empty or was intentionally preserved]
```

Then tell the user what to do next based on what was reset:

**If profile was reset:**
> Your candidate profile is now blank. Run the setup workflow to repopulate it. The command auto-detects any files in your `documents/` folder and offers to read from there.

**If documents were reset:**
> The `documents/` folder is now empty. Add your career documents and run the setup workflow to populate your profile. See `documents/README.md` for instructions on what to put where.

**If both were reset:**
> Both your profile files and documents folder are now empty. Add documents to `documents/` (or skip and use the CV import / interview path), then run setup.
