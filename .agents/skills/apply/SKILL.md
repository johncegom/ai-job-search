---
name: apply-workflow
description: >
  Runs the drafter-reviewer job application workflow to evaluate fit, draft CV & cover letter in LaTeX, critique using a reviewer, compile and inspect PDFs, and verify output.
  Triggers on: apply, /apply, apply to job, write cover letter and CV, tailors cv and cover letter
---

# Drafter-Reviewer Job Application Workflow

You are orchestrating a two-phase job application workflow. The job posting is provided as input (either a URL or pasted text).

Follow these steps **exactly in order**. Do not skip steps.

**Token-efficiency rules for this workflow:**
- Never re-Read a file whose contents are already in your context from an earlier step. If you read it in Step 1, it is still available in Step 2.
- Perform the reviewer step internally by simulating a separate reviewer context (a hiring manager perspective) rather than attempting to spawn a separate text agent if the subagent tool is not available.
- Run the full verification checklist exactly once, at the end (Step 6). The reviewer focuses on content critique, not verification.
- Step 5 (compile and inspect PDFs) is mandatory and non-skippable — LaTeX page-break decisions are unpredictable, and `.tex` files that look fine often produce broken PDFs (orphaned entry titles, cover letters spilling to page 2, bullet fonts mismatching).

---

## Step 0: Parse Input

- If the input looks like a URL, use `WebFetch` or `read_url_content` to retrieve the job posting content.
- If it is pasted text, use it directly.
- Extract: **company name**, **role title**, **department** (if mentioned), **location**, and **language** of the posting (Danish or English).
- Store these for use throughout the workflow.

---

## Step 1: DRAFTER - Evaluate Fit

Read the evaluation framework:
- `.agents/skills/job-application-assistant/04-job-evaluation.md`
- `.agents/skills/job-application-assistant/01-candidate-profile.md`

Using the framework from `04-job-evaluation.md`, evaluate the job posting against the candidate's profile. If the salary lookup tool is configured, run:

```bash
python salary_lookup.py "<Company Name>" --json
```

If the posting specifies a city, add `--city "<City>"` to narrow results. Parse the JSON output and include the salary benchmark in the evaluation. If the tool is not configured or returns an error, skip the salary benchmark.

Present the evaluation to the user with:

1. **Skills match** - which required/preferred skills match vs. gaps
2. **Experience match** - how work history maps to the role
3. **Behavioral/culture match** - how behavioral profile fits the role/company culture
4. **Salary benchmark** - salary index for the company (if available)
5. **Overall fit score** and recommendation (strong fit / moderate fit / weak fit)

After presenting the evaluation, ask the user:
> "Should I proceed with drafting the CV and cover letter for this role?"

**If the user says no, stop here.** If yes, continue to Step 2.

---

## Step 2: DRAFTER - Draft CV + Cover Letter

You already have `01-candidate-profile.md` and `04-job-evaluation.md` in context from Step 1. **Do not re-read them.**

Read only the reference files you do not yet have:
- `.agents/skills/job-application-assistant/03-writing-style.md`
- `.agents/skills/job-application-assistant/05-cv-templates.md`
- `.agents/skills/job-application-assistant/06-cover-letter-templates.md`

Also read the most recent existing CV and cover letter files for concrete structural reference (one of each is enough):
- Read any existing `cv/main_*.tex` file as a LaTeX template reference
- Read any existing `cover_letters/cover_*.tex` or `cover_letters/Cover_*.tex` file as a template reference

### CV (`cv/main_<company>.tex`)
- Always in **English**
- Follow the moderncv/banking format from `05-cv-templates.md`
- Tailor the profile statement and experience bullets to the specific role
- Reframe skills and achievements to match job requirements
- Keep to 2 pages

### Cover Letter (`cover_letters/cover_<company>_<role>.tex`)
- **Match the language of the job posting** (Danish posting -> Danish cover letter, English posting -> English cover letter)
- Follow the structure from `06-cover-letter-templates.md`
- Use the `cover.cls` template
- Tailor the opening paragraph to the specific role and company
- Address to a named person if available in the posting, otherwise "Dear Hiring Manager" (or equivalent in posting language)
- Keep to approximately one page
- Any mention of agentic coding or AI tooling must reference **Antigravity (Gemini)** by name

Write both files to disk. Keep the exact text of both drafts in working memory.

---

## Step 3: REVIEWER - Research & Critique

Simulate a reviewer agent critique by switching perspective to an objective hiring manager. Conduct thorough company research and critique the drafts against the candidate's profile.

### 1. Research the Company
Use WebSearch and WebFetch to research:
- The company's website, mission, and recent news
- The specific department or team (if mentioned in the posting)
- Any recent projects, press releases, or strategic initiatives relevant to the role
- Company culture and values

### 2. Read Reference Materials (content-critique only)
Read these four files — and only these — to ground your critique:
- `.agents/skills/job-application-assistant/01-candidate-profile.md`
- `.agents/skills/job-application-assistant/02-behavioral-profile.md` — use this specifically to check whether the cover letter's voice matches the candidate's natural register. A "Collaborator" PI profile, for example, should not be given a combative, solo-hero tone; a "Persuader" profile should not be given over-hedged, apologetic phrasing.
- `.agents/skills/job-application-assistant/03-writing-style.md`
- `.agents/skills/job-application-assistant/04-job-evaluation.md`

Do NOT read `05-cv-templates.md` or `06-cover-letter-templates.md` — those govern LaTeX structure.

### 3. Produce Feedback
Evaluate the draft CV and Cover Letter against the job posting and company research. Produce your feedback in **two parts**:

**Part A — Structured edits:**
A JSON array of concrete edits the drafter can apply directly. Each edit is an object:
```json
[
  {
    "file": "cv/main_<COMPANY>.tex" | "cover_letters/cover_<COMPANY>_<ROLE>.tex",
    "old_string": "<exact text currently in the draft>",
    "new_string": "<replacement text>",
    "reason": "<one-line rationale: keyword match / company angle / reframing / style>"
  }
]
```
Make `old_string` unique — include enough surrounding context so it matches exactly once per file.

**Part B — Narrative suggestions (for judgment calls that are not mechanical edits):**
Prose suggestions grouped by category:
- **Missed keywords/requirements** — what to add and roughly where
- **Company/department-specific angles** — connections between experience and the company's strategic priorities, based on your research
- **Action-oriented reframing** — identify passive, generic, or low-energy statements and suggest action-oriented rewrites
- **Tone and style issues** — check against `03-writing-style.md` AND `02-behavioral-profile.md`. Flag any issues with tone, formality, or voice (cliches, hedging, over-humility, inconsistent register)

**CRITICAL RULE:** All suggestions must be grounded in actual profile data. Do NOT suggest fabricating skills, experience, or achievements.

---

## Step 4: DRAFTER - Revise Based on Feedback

Switching back to the drafter perspective:

1. **Apply Part A (structured edits) directly.** For each edit in the JSON array, make the change in the files. Skip any whose rationale would require fabricating content.
2. **Apply Part B (narrative suggestions)** using judgment:
   - **Missed keywords/requirements:** add the keyword or capability where it fits naturally in the CV or cover letter.
   - **Company/department-specific angles:** weave the company's research into the cover letter opening or motivation paragraph.
   - **Action-oriented reframing:** rewrite passive or generic phrasing.
   - **Tone and style issues:** apply the writing-style-guide fixes.
3. Do NOT incorporate any suggestion that would fabricate skills or experience. If a posting requirement is a genuine gap, acknowledge it honestly and frame adjacent experience instead.

After all edits are applied, compile the updated drafts.

---

## Step 5: DRAFTER - Compile & Inspect PDFs (MANDATORY)

**Never skip this step.** Compile both documents and verify the PDFs before presenting.

### 5a. Compile

Run the compilation commands:
```bash
cd cv && lualatex -interaction=nonstopmode main_<company>.tex
cd ../cover_letters && xelatex -interaction=nonstopmode cover_<company>_<role>.tex
```

- CV uses **lualatex** — pdflatex fails on modern MiKTeX with fontawesome5 font-expansion errors.
- Cover letter uses **xelatex** — cover.cls requires fontspec.

If either compile fails, fix the error and re-compile until clean.

### 5b. Inspect layout

Inspect both compiled PDFs and verify:

**CV (`cv/main_<company>.pdf`):**
- [ ] Exactly 2 pages (not 1, not 3)
- [ ] No orphaned `\cventry` titles — a job/education title line must never sit alone at the bottom of page 1 with its bullets on page 2.
- [ ] Section headings are not isolated at the top of page 2 with only 1-2 lines below
- [ ] No awkward whitespace gaps

**Cover letter (`cover_letters/cover_<company>_<role>.pdf`):**
- [ ] Exactly 1 page
- [ ] Signature block visible, not cut off or pushed to a second page
- [ ] Bullet list font matches surrounding body text (both should be Raleway-Medium)

### 5c. Iterate until clean

If the layout has problems, edit the `.tex` files and recompile. Common fixes:
- **Orphaned CV entry title:** `\usepackage{needspace}` in preamble, then `\needspace{5\baselineskip}` immediately before the problematic `\cventry`
- **CV spills to page 3:** use relevance-weighted cutting. Cut the lowest-total-score line first, regardless of section.
- **Cover letter spills to 2 pages:** trim sentences that restate what a bullet already said or bullets that do not hit posting keywords.

### 5d. ATS & keyword verification (CV)

An ATS parser reads the PDF's embedded text layer.
If `pdftotext` (poppler) is missing, skip the parseability items with a warning and verify keyword coverage from a visual review.

**1. Extract the text layer:**
```bash
cd cv && pdftotext -layout main_<company>.pdf main_<company>.txt
```
Read the `.txt` file.

**2. Parseability checks:**
- [ ] Text extracted at all, with no garbage runs (no `(cid:NNN)` or ``)
- [ ] Email and phone survive as literal text
- [ ] Reading order matches the visual order
- [ ] Dates recognizable

**3. Keyword coverage:** Match the posting's keywords against the extracted text. Check which are covered, which are synonym-only, and which are missing. Note: **Never stuff keywords.**

**4. Clean up:** delete the extracted `.txt` file.

### 5e. Clean up build artifacts

Delete the `.aux`, `.log`, `.out` files (keep the `.tex` and `.pdf`).

---

## Step 6: Present Final Output

Run the full verification checklist from `.agents/AGENTS.md` now.

### Verification Checklist
Report pass/fail for each item in the verification checklist (factual accuracy, targeting, consistency, quality).

### Key Tailoring Decisions
Summarize 3-5 key decisions made to tailor the application.

### Files Created
List the files written:
- `cv/main_<company>.tex`
- `cover_letters/cover_<company>_<role>.tex`

Suggest the user review and finalize the files.
