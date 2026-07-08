---
name: expand-workflow
description: >
  Scans user documents, GitHub, and online presence to discover hidden competencies, enriches them with web research, and appends them to candidate profile.
  Triggers on: expand, /expand, expand profile, enrich profile, discover skills, scan github
---

# Competency Expansion from Documents and Online Presence

You are enriching the candidate profile by discovering competencies hidden in documents and public online presence. This command is additive only — it never modifies existing profile content, only extends it.

Follow these steps **exactly in order**. Do not skip steps.

---

## Step 0: Read Existing Profile Files

Read these two files in parallel before doing anything else. You must know what is already there so you do not propose duplicates.

- `.agents/skills/job-application-assistant/01-candidate-profile.md`
- `.agents/skills/job-application-assistant/02-behavioral-profile.md`

Hold this content in context throughout the command. Do not re-read these files later.

---

## Step 1: Discovery — Scan All Sources

Scan every available source for "experience items" — anything that implies skill, knowledge, or competency. Process sources in this order.

### 1a. documents/cv/
Read all files in `documents/cv/`. Extract:
- Every course or module listed (including university coursework and online courses)
- Every certification mentioned, with issuer and date
- Every job responsibility bullet point (tools, methods, outcomes)
- Every independent project or side project
- Every volunteer or extracurricular role

### 1b. documents/linkedin/
Read all files in `documents/linkedin/`. Extract:
- Courses and certifications in the "Licenses & Certifications" section
- Skills and endorsements list
- Volunteer experiences
- Projects section
- Any platform-specific items not already found in the CV

### 1c. documents/diplomas/
Read all files in `documents/diplomas/`. Extract:
- All course/module names listed on transcripts
- Thesis title and subject area
- Any specialisation or track name

### 1d. documents/references/
Read all files in `documents/references/`. Extract:
- Competency language used by the referee
- Any specific projects, tools, or methods named

### 1e. GitHub Profile
Look up the GitHub username from `01-candidate-profile.md`. If a GitHub URL or username is present:

1. Use WebFetch or WebSearch to retrieve the public profile and pinned repositories
2. For each repository found:
   - Fetch the repository README
   - Note: name, description, primary language(s), topics/tags, any technologies mentioned in the README
3. Also retrieve the full repository list if available.

If no GitHub username or URL is found in the profile, skip this source.

### 1f. Other URLs in Profile
Check `01-candidate-profile.md` for any other URLs (portfolio site, personal website, Kaggle, Google Scholar, ResearchGate, publication links). For each:
- Fetch the page
- Extract any tools, methods, datasets, awards, or skills mentioned

---

## Step 2: Web Enrichment

For each experience item discovered in Step 1, search the web to extract the competencies it implies. Apply both approaches below:

### Approach A: Direct lookup (explicit tools and frameworks)
If the item names a specific tool, framework, library, method, or platform, search for it directly:
- `"[Course name] [Provider] syllabus learning outcomes"`
- `"[Certification name] skills covered exam guide"`
- `"[Tool/framework name] skills what you learn"`

Fetch the most relevant page and extract the competency list.

### Approach B: Inferred competencies (from description and context)
For each item, regardless of whether Approach A found anything, also reason from the description:
- What problem domain does this item address?
- What methods, skills, or knowledge does someone need to do this work?
- What is the standard toolchain for this kind of work?

Combine both approaches into a single competency list for each item.

### Prioritise web lookup for:
- Named online courses (Coursera, edX, Udemy, LinkedIn Learning, DataCamp, fast.ai, etc.)
- Named certifications (AWS, GCP, Azure, Databricks, Tableau, etc.)
- University courses with a standard syllabus
- GitHub repositories with a README that names specific technologies

### Infer (without web lookup) for:
- Generic job responsibility bullets with no named tool
- Vague project descriptions
- Reference letter language

---

## Step 3: Build Competency Map

After enriching all items, build a deduplicated competency map. Group findings into these categories:
- **Technical Skills — Primary**
- **Technical Skills — Secondary**
- **Domain Knowledge**
- **Methods and Practices**
- **Soft / Behavioral**

For each competency, record:
- The competency name
- The source item it came from (e.g. "Coursera — Deep Learning Specialisation")
- Whether it came from direct lookup (A), inference (B), or both

Remove anything already present in `01-candidate-profile.md` or `02-behavioral-profile.md`.

---

## Step 4: Present Grouped Summary

Present all new competencies for the user's review before writing anything. Format:

```
## Competency signals found across sources

**COURSES & CERTIFICATIONS**
Source: [Course/cert name — Provider]
  + [Competency 1]
  + [Competency 2]
  ...

**GITHUB — [repo-name]**
Source: README + inferred from tech stack
  + [Competency 1]
  + [Competency 2]
  ...

**JOB RESPONSIBILITIES — [Company, Role]**
Source: CV bullets + direct tool lookup
  + [Competency 1]
  ...

**BEHAVIORAL SIGNALS**
Source: [Reference letter — Name / LinkedIn About / Project leadership]
  + [Signal 1]
  ...
```

Then ask:

> **How would you like to proceed?**
> - **`all`** — Add everything above to your profile
> - **`review`** — Walk through each source group one at a time
> - **`skip`** — Cancel without writing anything
>
> Or specify groups to skip (e.g. "skip GitHub, add everything else").

Wait for the response before writing.

---

## Step 5: Write Confirmed Additions

Apply only the confirmed items. Use the Edit tool to add to the relevant sections of each file — do not rewrite entire files.

### Additions to `01-candidate-profile.md`
- Technical skills (primary and secondary) → append to the Technical Skills section
- Domain knowledge → append to the Domain Knowledge or Technical Skills section
- Methods and practices → append appropriately

For each addition, add a brief source annotation in a comment or parenthetical: *(Coursera — Deep Learning Specialisation)*, *(GitHub — project-name)*, etc.

### Additions to `02-behavioral-profile.md`
- Soft/behavioral signals → append to the "Strongest Behavioral Traits" or "How I Work Best" section
- Always label inferred behavioral additions: *[Inferred from reference letter — Name / review before relying on this]*

---

## Step 6: Summary Report

After writing, present:

```
## Expand Complete

### Added to 01-candidate-profile.md
[List each competency added, with source]

### Added to 02-behavioral-profile.md
[List each behavioral signal added, with source]

### Sources processed
[List each source scanned and how many competencies it yielded]

### Sources skipped
[List any sources that were missing, empty, or yielded nothing new]

### Needs manual review
[Any items that were ambiguous or where web lookup returned no clear syllabus]
```
