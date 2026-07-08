---
name: add-portal-workflow
description: >
  Generates a new job-portal search CLI skill for a job board in your local market, scaffolds its folder structure, and tests it.
  Triggers on: add portal, add job portal, /add-portal, register job portal
---

# Generate a Job-Portal Search Skill for Your Local Market

You are helping the user build a job-portal search skill for a job board in their market. This command is a guided workflow: investigate the portal, scaffold the skill from the canonical structure, and test-run a live query before registering anything.

The generator is **country-agnostic**: it works for any portal in any market and language. The skills it produces live in the user's workspace.

Input arguments may contain a subcommand, a portal URL, or nothing.

Follow these steps **in order**.

---

## Step 0: Parse Arguments

- If input contains `--list`: use Glob with `.agents/skills/*/SKILL.md`, print a table of installed portal skills (name, market from the description), and stop.
- If input contains a URL: treat it as the portal URL and carry it into Step 1.
- Otherwise: start the interview at Step 1.

---

## Step 1: Interview - Portal Basics

Ask the user:
1. **Portal URL** - the job board's public site (e.g. `https://www.seek.com.au`).
2. **Skill name** - kebab-case, suffixed `-search` (e.g. `seek-search`). Must not collide with an existing folder in `.agents/skills/`.
3. **Market and language** - which country/region the portal covers and what language its postings use. This drives the trigger phrases in `SKILL.md` (include local-language terms).
4. **A realistic test query** - a job title or skill the user would actually search for, used for the live test in Step 4.

---

## Step 2: Investigate the Portal

Do reconnaissance before writing any code. Use WebFetch (or `curl` via command line) on the portal:

1. **Find the search URL pattern.** Load the portal's search page, run a search in the URL bar, and identify: the search endpoint, the query parameter, and any parameters for location, posting age, and pagination. Prefer a JSON API if one backs the site; otherwise plan to parse the HTML results page.
2. **Fetch one search-results response** for the test query and identify the per-result fields: **id, title, company, location, posting date, and URL**.
3. **Find the detail-page pattern** - the URL that returns a single posting's full description, and where the description, deadline, employment type, and apply link live in it.
4. **Check access requirements and terms.**
   - Fetch `robots.txt` and check whether the search/detail paths are disallowed.
   - If the portal requires login/authentication to view listings, **stop**: this pattern only works on public pages.
   - If robots.txt disallows the paths, tell the user plainly and let them decide whether to proceed for personal use. If they proceed, the generated `SKILL.md` **must** carry a prominent personal-use-only warning.

Record everything you found - endpoints, parameters, field anchors, quirks.

---

## Step 3: Scaffold the Skill

**Canonical reference:** read `.agents/skills/linkedin-search/` before generating. Copy its architecture, not its LinkedIn-specific parsing.

Create `.agents/skills/<name>/` with:

```
<name>/
├── SKILL.md              # Skill definition with trigger phrases
├── url-reference.md      # Endpoint documentation from Step 2
└── cli/
    ├── package.json
    ├── tsconfig.json
    ├── README.md
    ├── src/
    │   ├── cli.ts        # Arg parsing, help text, command dispatch
    │   ├── helpers.ts    # Fetch, parsers, error writer
    │   └── commands/
    │       ├── search.ts
    │       └── detail.ts
    └── tests/
        └── helpers.ts    # Test utilities
```

### The portal-skill contract

These conventions make portal skills interchangeable for the scraper workflow:
- **Commands:** `search` and `detail <id|url>`.
- **Search flags:** `--query`/`-q`, `--jobage <days>` (posting age), `--page <n>`, `--limit <n>`, `--format json|table|plain` (default `json`).
- **JSON output shape:** `{ "meta": { "count": ..., "page": ... }, "results": [...] }` where each result has at least `id`, `title`, `company`, `location`, `date`, `url`.
- **Errors:** written to **stderr** as `{ "error": "...", "code": "..." }`, exit code `1`.
- **Fetching:** browser User-Agent, exponential backoff with jitter on 429/5xx (max ~6 retries).
- **HTML parsing:** parse each card independently so one malformed card does not break the rest.
- **Dependencies:** default to zero runtime dependencies (plain `bun` + `fetch` + regex parsing) like `linkedin-search`.

---

## Step 4: Test-Run a Live Query (MANDATORY)

Never register a portal skill that has not returned real results.

1. Install dev types and typecheck:
   ```bash
   cd .agents/skills/<name>/cli && bun install && bun run typecheck
   ```
2. Run the live search with the user's test query:
   ```bash
   bun run src/cli.ts search -q "<test query>" --limit 5 --format table
   ```
3. Verify the results are real and complete.
4. Take one `id` from the results and run `detail`:
   ```bash
   bun run src/cli.ts detail <id> --format plain
   ```
5. Run the test suite: `bun run test`.

Do not proceed to Step 5 until search, detail, and tests all pass.

---

## Step 5: Register

1. Ask whether the user wants the new portal added to their scraper search strategy. If yes, add the portal's site to the relevant query categories in `.agents/skills/job-scraper/search-queries.md` so the scraper workflow includes it.
2. Remind the user to run `bun install` under `.agents/skills/<name>/cli`.
3. Note that the skill auto-triggers from its `SKILL.md` description.

---

## Step 6: Confirm

Present a summary:

> **Portal skill `<name>` generated and verified.**
> - Files: `.agents/skills/<name>/`
> - Live test: search and detail verified
> - Data source: summary of endpoints
