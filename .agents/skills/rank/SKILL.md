---
name: rank-workflow
description: >
  Batch-scores the jobs collected by the scraper, triage them against the candidate profile and evaluation framework, and presents a ranked shortlist.
  Triggers on: rank, /rank, rank jobs, triage jobs, triage scraper results
---

# Triage Scraped Jobs into a Ranked Shortlist

You are batch-scoring the jobs that the scraper has collected, so the user can decide where to spend apply effort. Scraper finds and dedupes postings; rank is the bridge: it scores every new posting against the fit framework and returns a ranked shortlist.

Rank produces **triage scores**, not final evaluations. It scores from the posting text and the candidate profile only - no company research. The apply workflow's Step 1 evaluation (which adds company research) remains authoritative and always re-runs when the user applies.

Follow these steps **in order**.

---

## Step 0: Parse Input

Input arguments may contain:
- Nothing → rank all jobs with status `new` in `job_scraper/seen_jobs.json`
- A focus area (e.g., "data science") → rank only jobs whose title or stored fit-notes match the focus
- `--all` → re-rank every job that has not been applied to, including previously ranked ones (useful after the profile changes)
- `--top <N>` → shortlist size (default 5)

---

## Step 1: Load State

1. Read `job_scraper/seen_jobs.json`. If the file is missing or has no entries, tell the user to run the scraper first and stop.
2. Read `job_search_tracker.csv`. Build the exclusion set: any company+role already in the tracker is out of scope.
3. Select candidates: entries with status `new` (or all non-applied entries with `--all`), minus the exclusion set, filtered by the focus area if one was given.
4. If no candidates remain, say so ("Nothing new to rank - run the scraper to find fresh postings") and stop.
5. Read the scoring framework and profile **once**:
   - `.agents/skills/job-application-assistant/04-job-evaluation.md`
   - `.agents/skills/job-application-assistant/01-candidate-profile.md`

State how many jobs will be ranked before proceeding.

---

## Step 2: Batch-Fetch and Score

Triage and score the selected candidate jobs. For each job:

- Use the scoring rubric extracted from the files you read in Step 1: the strong/moderate/weak skill match areas, direct/adjacent experience domains, behavioral thrive/drain factors, career goals, deal-breakers, and the location constraints.
- Fetch each posting URL with WebFetch or `read_url_content` and score **only from actually fetched content**. If a URL is dead, redirects to a listing page, or the posting has expired, mark that job `expired` - never score from the title alone.
- Scope is triage: posting text vs. rubric. **No company research, no salary lookup, no web searches** - that depth belongs to apply.

Produce the following structured data for each job:
- **key**: the job's key in `seen_jobs.json`
- **status**: "scored" or "expired"
- **scores**: { "technical": 0-100, "experience": 0-100, "behavioral": 0-100, "career": 0-100 }
- **location**: "PASS" or "FAIL" or "FLAG"
- **deadline**: "YYYY-MM-DD" or null
- **strengths**: 1-3 bullets, grounded in the posting text
- **gaps**: 1-3 bullets, honest
- **language**: posting language

Scoring uses the dimension definitions from `04-job-evaluation.md` verbatim. The honesty rule applies to triage too: gaps are stated, never smoothed over.

---

## Step 3: Aggregate and Rank

For each scored job:

1. Compute the overall score with the weighting from `04-job-evaluation.md` (Technical 30%, Experience 25%, Behavioral 15%, Career Alignment 30%; location is unweighted).
2. Map to the framework's verdict bands (Strong Fit 75+, Good Fit 60-74, Moderate Fit 45-59, Weak Fit 30-44, Poor Fit <30).
3. **Location veto:** `FAIL` (e.g. requires relocation) excludes the job from the shortlist no matter the score - list it separately with the reason. `FLAG` (e.g. heavy travel) stays in the ranking but carries a visible ⚠ marker.
4. **Deadline urgency:** a deadline within 7 days gets a 🔥 marker and wins ties. A deadline that has already passed moves the job to `expired`.

Sort by overall score (descending), urgency as tiebreaker.

---

## Step 4: Update State

Update `job_scraper/seen_jobs.json` in place - these fields are additive to the scraper's schema:
- Ranked jobs: set `"status": "ranked"` and add `"rank_score": <overall>`, `"rank_verdict": "<band>"`, `"rank_date": "YYYY-MM-DD"`
- Dead or past-deadline jobs: set `"status": "expired"`

Do not modify `job_search_tracker.csv` - that file records applications, and rank never applies. Re-running rank is idempotent: already-`ranked` jobs are skipped unless `--all` re-scores them.

---

## Step 5: Present the Shortlist

Present the triage results:

```
## Job Ranking - YYYY-MM-DD

Ranked <N> new postings (<X> shortlisted, <Y> below threshold, <Z> expired/vetoed).

### Shortlist

| # | Score | Verdict | Title | Company | Location | Deadline | |
|---|-------|---------|-------|---------|----------|----------|---|
| 1 | 78 | Strong Fit | ... | ... | ... | ... | |

### Why these ranked highest
**1. <Title> at <Company> (78)** - [2-3 strength bullets and the honest gap]

### Below threshold
| Score | Verdict | Title | Company | One-line reason |

### Excluded
- <Title> at <Company> - location FAIL: requires relocation
- <Title> at <Company> - expired <date>
```

Rules for the presentation:
- Every claim traces to fetched posting text or the profile - no invented details.
- Say explicitly that these are **triage scores from the posting text only**, and that the apply workflow will re-evaluate with company research before anything is drafted.
- Then ask: "Want to apply to any of these? Give me the number(s) and I'll start with the full apply workflow."
- If the user picks one, run the apply workflow on that job's URL, passing the triage verdict as prior context but **re-running the full Step 1 evaluation**.
