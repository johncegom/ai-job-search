---
name: add-template-workflow
description: >
  Registers a custom LaTeX CV or cover letter template with the job search framework, validates that it compiles, and activates it.
  Triggers on: add template, register template, /add-template, use template
---

# Register a Custom CV or Cover Letter Template

You are helping the user register their own LaTeX template with the job search framework. The framework ships with moderncv (banking style) for CVs and a custom `cover.cls` for cover letters. This command lets the user swap in their own template: store the template files, capture usage instructions (compile engine, fonts, style rules, page limits), verify the template compiles, and wire it into the apply workflow.

Input arguments may contain a subcommand, a template name, a file path, or nothing.

Follow these steps **in order**.

---

## Step 0: Parse Arguments

- If input contains `--list`: run **List Mode** below and stop.
- If input contains `--use <name>`: skip to **Step 5: Activate** with that template name. `--use default` deactivates any custom template and restores the stock guidance (see Step 5).
- If input contains a file path: treat it as the template source and carry it into Step 1.
- Otherwise: start the registration flow at Step 1.

### List Mode

Use Glob with `templates/**/TEMPLATE.md` to find registered templates. For each, read the manifest and print a table:

```
## Registered Templates

| Name | Type | Engine | Fonts | Active |
|------|------|--------|-------|--------|
| <name> | CV / Cover letter | lualatex/xelatex/pdflatex | <main font> | yes/no |
```

A template is **active** if `.agents/skills/job-application-assistant/05-cv-templates.md` (CV) or `.agents/skills/job-application-assistant/06-cover-letter-templates.md` (cover letter) contains an `ACTIVE-TEMPLATE` managed block naming it. If no custom templates exist, say so. Stop here.

---

## Step 1: Template Type and Source

Ask the user:
1. **Type:** Is this a **CV** template or a **cover letter** template?
2. **Source:** Where is the template? Accept a path, pasted LaTeX content, or a directory.

Read every provided file. If the template references a document class or package that is not part of standard TeX distributions, confirm the user has the file and ask for it if missing.

---

## Step 2: Capture Template Instructions

Interview the user for the metadata that the apply workflow needs to use the template correctly. Infer as much as possible from the LaTeX source first and present your inferences for confirmation.

Collect:
1. **Name** - short kebab-case identifier (e.g. `awesome-cv`). Must not collide with an existing folder in `templates/`.
2. **Compile engine** - `lualatex`, `xelatex`, or `pdflatex`.
3. **Fonts** - which font(s) the template uses and where they come from (bundled in fonts/ or system font).
4. **Style rules** - color scheme, section order, heading style, spacing conventions, bullet formatting, date format.
5. **Page limit** - hard page count for the compiled PDF. Default: **2 pages** for a CV, **1 page** for a cover letter.
6. **Known pitfalls** (optional).

---

## Step 3: Store the Template

Create the template folder:
- CV: `templates/cv/<name>/`
- Cover letter: `templates/cover_letters/<name>/`

Write into it:
1. **`template.tex`** - the template skeleton. Replace all personal data in the source with `[PLACEHOLDER]` tokens (`[YOUR_NAME]`, `[YOUR_EMAIL]`, `[YOUR_PHONE]`, `[YOUR_LINKEDIN_URL]`, ...) so the template is shareable and profile-agnostic.
2. **Class/style files** - copy any `.cls`/`.sty` files alongside `template.tex`.
3. **`fonts/`** - copy bundled font files here.
4. **`TEMPLATE.md`** - the manifest. Use exactly this format:

```markdown
# Template: <name>

- **Type:** CV | Cover letter
- **Engine:** lualatex | xelatex | pdflatex
- **Page limit:** <N> page(s)
- **Fonts:** <main font> (<bundled in fonts/ | system font>)
- **Class/packages:** <documentclass and non-standard packages>

## Compile command
    cd <output dir> && <engine> -interaction=nonstopmode <file>.tex

## Style rules
- <rule 1>

## Known pitfalls
- <pitfall and its fix>
```

---

## Step 4: Verify the Template Compiles (MANDATORY)

Never register a template without a successful test compile.

1. Copy `template.tex` to a scratch file in the same folder (e.g. `_compile_test.tex`) and fill every `[PLACEHOLDER]` with realistic dummy data.
2. Compile with the declared engine:
   ```bash
   cd templates/<type>/<name> && <engine> -interaction=nonstopmode _compile_test.tex
   ```
3. If compile fails: show the user the error lines, diagnose, and fix what you can.
4. On success, inspect the PDF and confirm the layout renders sensibly.
5. Delete the scratch files: `_compile_test.tex`, `_compile_test.pdf`, and all `.aux`/`.log`/`.out` artifacts.

Do not proceed to Step 5 until the test compile passes.

---

## Step 5: Activate the Template

Activation wires the template into the apply workflow by adding a **managed block** to the top of the relevant guidance file — `.agents/skills/job-application-assistant/05-cv-templates.md` for CVs, `.agents/skills/job-application-assistant/06-cover-letter-templates.md` for cover letters.

Insert (or replace, if one exists) this block immediately after the file's H1 title:

```markdown
<!-- BEGIN ACTIVE-TEMPLATE (managed by template-registration - do not edit by hand) -->
> **Active template override: `<name>`**
>
> A custom template is active. Where this block conflicts with the stock guidance below, this block wins. Structural advice below (tailoring, page-budget, cutting rules) still applies.
>
> - **Template skeleton:** `templates/<type>/<name>/template.tex`
> - **Manifest:** `templates/<type>/<name>/TEMPLATE.md`
> - **Compile with:** `<engine>`
> - **Fonts:** <font summary>
> - **Page limit:** exactly <N> page(s)
> - **Output file:** unchanged (`cv/main_<company>.tex` / `cover_letters/cover_<company>_<role>.tex`)
<!-- END ACTIVE-TEMPLATE -->
```

When `--use default` is requested, remove the managed block entirely to revert to stock templates.

---

## Step 6: Confirm

Present a summary:

> **Template `<name>` registered and activated.**
> - Files: `templates/<type>/<name>/`
> - Test compile: passed with `<engine>` (<N> page(s))
> - The apply workflow will now draft from this template.
