<p align="center">
  <img src="assets/mascot/pip_flight_loop.gif" alt="Pip, the courier bird" width="200">
</p>

# AI Job Search

*The job search that runs on your machine.*

<p align="center">
  <a href="https://trendshift.io/repositories/43622?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-43622" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/43622/daily" alt="MadsLorentzen%2Fai-job-search | Trendshift" width="250" height="55"/></a>
</p>

[![CI](https://github.com/MadsLorentzen/ai-job-search/actions/workflows/ci.yml/badge.svg)](https://github.com/MadsLorentzen/ai-job-search/actions/workflows/ci.yml)

An AI-powered job application framework that runs on both [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [Antigravity (Gemini)](https://gemini.google.com). Fork it, fill in your profile, and let your coding assistant evaluate job postings, tailor your CV, write cover letters, and prepare you for interviews.

> Note: This is an independent open-source project and is not affiliated with, endorsed by, sponsored by, or maintained by Anthropic. Anthropic and Claude Code are referenced only to describe the toolchain this workflow uses.
>
> This project has **no affiliated cryptocurrency, token, or paid sponsorship program**. Anything claiming otherwise is unauthorized and should be treated as a scam. The only ways to support the project are the Ko-fi link below and contributing on GitHub.

## Does it actually work?

I'm a geophysicist by training. When my position was cut in late 2025, I built this framework to run my own job search - the same `/scrape`, `/apply`, and `/interview` workflow in this repo, used weekly, on my own career. I was upfront about it with every employer I spoke to, and instead of counting against me, it usually sparked a genuine technical conversation.

Sixty-nine tailored applications, twenty first interviews, and one signed contract later, I started as an AI engineer in June 2026. People kept asking whether this actually works. It got me hired. Now it's yours.

*The longer version, including the full application funnel, is on [LinkedIn](https://www.linkedin.com/in/mads-lorentzen/).*

<p align="center">
  <i>Did this save you a Sunday of cover-letter writing? Consider a coffee.<br>
  Did it land you the job? Maybe two.</i> ☕
</p>

<p align="center">
  <a href="https://ko-fi.com/madslorentzen">
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=6" alt="Buy me a coffee at ko-fi.com" height="40">
  </a>
</p>

## What this is

A structured workflow that turns Claude Code or Antigravity (Gemini) into a full-stack job application assistant. The core workflow (self-profiling, fit evaluation, and the drafter-reviewer application pipeline) is **language- and country-agnostic**, and works identically regardless of which assistant you use. The job portal search skills are built for the Danish market (Jobindex, Jobnet, Akademikernes Jobbank, etc.), but the pattern is designed to be swapped for your local job boards.

```
Setup workflow  Scraper skill        Apply workflow
  |                |                     |
  v                v                     v
Fill in        Search job           Evaluate fit
your profile   portals              Score & recommend
  |                |                     |
  v                v                     v
Profile        Present matches      Draft CV + Cover Letter
files ready    with fit ratings     (LaTeX, tailored)
                   |                     |
                   v                     v
               Pick a match         Reviewer phase critiques
               -> Apply workflow    -> Revise -> Final output
```

The framework encodes career guidance best practices, including structured evaluation criteria, forward-looking cover letter framing, and optional salary benchmarking.

## Prerequisites

- [Claude Code](https://claude.com/claude-code) (CLI). Using a different agent tool (Codex, Antigravity, Gemini CLI)? Start at [`AGENTS.md`](AGENTS.md) - the portal search skills work there out of the box, and [community forks](https://github.com/MadsLorentzen/ai-job-search/discussions/78) adapt the full workflow.
- Python 3.10+
- [Bun](https://bun.sh) (for job search CLI tools)
- LaTeX distribution with `lualatex` and `xelatex`: [TeX Live](https://tug.org/texlive/), [MacTeX](https://tug.org/mactex/), [TinyTeX](https://yihui.org/tinytex/), or [MiKTeX](https://miktex.org/). The CV compiles with `lualatex` (pdflatex often fails on modern MiKTeX installs with `fontawesome5` font-expansion errors); the cover letter compiles with `xelatex` because `cover.cls` requires `fontspec`. If using a minimal TeX install such as TinyTeX or BasicTeX, install the extra packages listed in [SETUP.md](SETUP.md#minimal-tex-install-tinytexbasictex).
- Optional: `pdftotext` from [poppler](https://poppler.freedesktop.org/) (macOS: `brew install poppler`, Debian/Ubuntu: `apt install poppler-utils`, Windows: `choco install poppler`) — used by `/apply`'s ATS parseability check on the compiled CV. If missing, the check degrades gracefully to a visual keyword review.

## Quick start

### 1. Fork and clone

```bash
gh repo fork MadsLorentzen/ai-job-search --clone
cd ai-job-search
```

### 2. Install job search tools

PowerShell:

```powershell
$tools = @("jobbank-search", "jobdanmark-search", "jobindex-search", "jobnet-search", "linkedin-search", "freehire-search")
foreach ($tool in $tools) {
  Push-Location ".agents/skills/$tool/cli"
  bun install
  Pop-Location
}
```

Bash / zsh / Git Bash:

```bash
for tool in jobbank-search jobdanmark-search jobindex-search jobnet-search linkedin-search freehire-search; do
  (cd .agents/skills/$tool/cli && bun install)
done
```

For `linkedin-search` and `freehire-search` the install is optional: both have zero runtime dependencies and run with plain `bun`; `bun install` only pulls TypeScript dev types.

### 3. Set up your profile

Claude Code:
```bash
claude
# Then inside Claude Code:
/setup
```

Antigravity: in your Antigravity chat, run the setup workflow skill by typing:
> setup

The setup workflow offers three paths: read your `documents/` folder if you have one populated (CV PDF, LinkedIn export, diplomas, reference letters, past applications), import a single CV pasted in chat, or walk through an interview. It auto-detects what you have and asks. Documents-folder mode is idempotent and safe to re-run as you add more material; see `documents/README.md` for the layout.

### 4. Search for jobs

Claude Code: run `/scrape`. Antigravity: say `scrape`.

This searches multiple job portals for positions matching your profile, deduplicates results, and presents them sorted by fit. Pick a match to run the apply workflow on it directly — or, when a scrape returns more jobs than you want to eyeball, run the rank workflow (`/rank` or `rank`) to batch-score them all against the fit framework and get a ranked shortlist first.

### 5. Apply to a job

Claude Code: `/apply https://jobindex.dk/job/1234567`. Antigravity: `apply https://jobindex.dk/job/1234567`.

If the URL can't be fetched (some job portals block automated access), you can paste the job description directly instead.

This runs the full workflow: evaluate fit, draft CV + cover letter, run a reviewer critique (a dispatched subagent on Claude Code, a simulated reviewer context on Antigravity), revise, and compile/inspect the final output.

## Workflows and Skills

The setup, scrape, and apply actions form the core workflow. Seven additional workflow skills extend it once your profile is in place:

`/setup`, `/scrape`, and `/apply` form the core workflow. Eight more commands extend it once your profile is in place:

- **`/interview`** preps you for a scheduled interview on a tracked application. It builds a stage-specific prep pack from the application's archive (the exact posting, the CV and cover letter the interviewer actually read, feedback recorded from earlier rounds), researches the company and interviewers with a verify-before-use rule, maps likely questions to your STAR examples, and offers a mock interview following the roleplay protocol in `07-interview-prep.md`. Gaps get honest bridge answers, never invented experience.
- **`/outcome`** records what happened to an application - interview stages, offers, rejections, silence. It archives the submitted CV, cover letter, and posting text into `documents/applications/<company>_<role>/`, keeps `outcome.md` in the format `/setup` Path A parses, and updates the tracker. Once a few applications resolve, it points you back to `/setup` to calibrate the fit framework from what actually got interviews.
- **`/rank`** bridges `/scrape` and `/apply`: it batch-scores all newly scraped postings against the fit framework (parallel agents fetch each posting and score the five evaluation dimensions) and returns a ranked shortlist with honest per-job strengths and gaps. Deal-breakers veto, deadlines get urgency flags, dead postings get marked expired. Pick a number and it hands off to the full `/apply` workflow.
- **`/expand`** enriches your profile by scanning public sources you've already linked in it (GitHub repos, portfolio site, Kaggle, Google Scholar) and looking up syllabi for named courses and certifications. Discovered competencies are added to your profile with a source tag. Useful right after `/setup` to surface skills that documents alone don't make explicit.
- **`/upskill`** analyzes the gap between your profile and your tracked job postings (or a single posting via `/upskill <URL>`). Produces a prioritized heatmap of skill gaps and a learning plan with web-searched study resources and time estimates. Useful for career planning between applications.
- **`/html-report`** generates a self-contained HTML dashboard from `job_search_tracker.csv` and the application archives — stat cards, status/sector/channel/funnel charts (inline SVG, no external dependencies), and a filterable applications table. Opens directly in a browser, fully offline. Re-run it any time after `/outcome` adds new entries.
- **`/add-template`** registers your own LaTeX CV or cover letter template in place of the stock ones. It captures the template's instructions (compile engine, fonts, style rules, page limit), runs a mandatory test compile, and wires the template into `/apply`. See [LaTeX templates](#latex-templates) below.
- **`/add-portal`** generates a job-portal search skill for a job board in your market. It investigates the portal (search URL pattern, result structure, access rules), scaffolds the CLI skill from the same structure as the shipped ones, and test-runs a live query before registering. See [Job search tools](#job-search-tools) below.

`/reset` is also available, see [Starting over](#starting-over) below.

## File structure

```
ai-job-search/
├── CLAUDE.md                          # Main candidate profile + workflow rules
├── .claude/
│   ├── commands/
│   │   ├── apply.md                   # /apply workflow (drafter-reviewer)
│   │   ├── setup.md                   # /setup onboarding (documents folder, CV import, or interview)
│   │   ├── expand.md                  # /expand competency enrichment from documents and online presence
│   │   ├── add-template.md            # /add-template register custom LaTeX templates
│   │   ├── add-portal.md              # /add-portal generate a job-portal search skill for your market
│   │   ├── rank.md                    # /rank triage scraped jobs into a ranked shortlist
│   │   ├── outcome.md                 # /outcome record application results, archive materials
│   │   ├── interview.md               # /interview stage-specific prep pack + mock interview
│   │   ├── html-report.md             # /html-report generate application tracker dashboard
│   │   └── reset.md                   # /reset wipe profile data or documents folder
│   ├── skills/
│   │   ├── job-application-assistant/ # Core application skill (mirrors .agents/ below)
│   │   ├── job-scraper/               # Job search orchestration
│   │   └── upskill/                   # Gap analysis and learning plan
│   └── settings.json                  # Claude Code permissions (shared, scoped)
├── .agents/                            # Antigravity framework + cross-tool portal CLIs
│   ├── AGENTS.md                      # Main candidate profile + workflow rules (Antigravity)
│   ├── agents/
│   │   └── gemini-research-expert.md  # Research subagent
│   └── skills/
│       ├── job-application-assistant/  # Core application skill
│       │   ├── SKILL.md               # Skill definition
│       │   ├── 01-candidate-profile.md # Your education, experience, skills
│       │   ├── 02-behavioral-profile.md# PI/DISC/personality assessment
│       │   ├── 03-writing-style.md    # Tone, structure, do's and don't
│       │   ├── 04-job-evaluation.md   # Scoring framework for job fit
│       │   ├── 05-cv-templates.md     # LaTeX CV structure + tailoring rules
│       │   ├── 06-cover-letter-templates.md # LaTeX cover letter templates
│       │   └── 07-interview-prep.md   # STAR examples + interview framework
│       ├── job-scraper/               # Job search orchestration
│       │   ├── SKILL.md
│       │   └── search-queries.md      # Job search queries
│       ├── upskill/                   # Gap analysis and learning plan
│       │   └── SKILL.md
│       ├── setup/                     # Onboarding setup workflow
│       │   └── SKILL.md
│       ├── apply/                     # Drafter-reviewer application workflow
│       │   └── SKILL.md
│       ├── rank/                      # Triage scraped jobs
│       │   └── SKILL.md
│       ├── outcome/                   # Record application results
│       │   └── SKILL.md
│       ├── reset/                     # Clear profile data
│       │   └── SKILL.md
│       ├── expand/                    # Profile expansion
│       │   └── SKILL.md
│       ├── add-portal/                # Scaffold portal CLI skills
│       │   └── SKILL.md
│       ├── add-template/              # Register LaTeX templates
│       │   └── SKILL.md
│       ├── interview/                 # Interview prep workflow
│       │   └── SKILL.md
│       ├── jobbank-search/            # Akademikernes Jobbank (Denmark)
│       ├── jobdanmark-search/         # Jobdanmark.dk (Denmark)
│       ├── jobindex-search/           # Jobindex.dk (Denmark)
│       ├── jobnet-search/             # Jobnet.dk (Denmark, government portal)
│       ├── linkedin-search/           # LinkedIn public job listings (country-agnostic)
│       └── freehire-search/           # freehire.dev tech job aggregator (multi-market)
├── cv/
│   └── main_example.tex               # moderncv LaTeX template
├── cover_letters/
│   ├── cover.cls                      # Custom cover letter LaTeX class
│   ├── cover_example.tex              # Example cover letter
│   └── OpenFonts/                     # Lato + Raleway fonts
├── templates/                         # Custom templates
├── documents/                         # Career source materials
├── salary_lookup.py                   # Salary benchmarking tool
├── tools/
│   ├── convert_salary_excel.py        # Convert salary Excel to JSON
│   ├── lint_skills.py                 # CI lint for skills, commands, settings.json
│   ├── security_guards.py             # CI guards: permission allowlist, gitignore rules, manifests
│   └── README_SALARY_TOOL.md          # Salary tool setup instructions
├── job_scraper/                       # Scraper state (seen jobs, results)
├── upskill/                           # upskill reports output
├── job_search_tracker.csv             # Application tracking spreadsheet
└── SETUP.md                           # Detailed setup guide
```

## How the apply workflow works

The apply workflow runs a **drafter-reviewer workflow** with mandatory PDF compilation:

1. **Parse** the job posting (URL or text)
2. **Evaluate fit** against your profile (skills, experience, culture, location, career alignment)
3. **Draft** a tailored CV and cover letter in LaTeX
4. **Run a simulated reviewer phase** that researches the company and critiques the drafts
5. **Revise** based on the reviewer's feedback
6. **Compile and inspect** both PDFs: lualatex for the CV, xelatex for the cover letter. Gemini reads the rendered pages and iterates on the LaTeX until the CV is exactly 2 pages with no orphaned entry titles, and the cover letter is exactly 1 page with the signature visible and fonts consistent.
7. **ATS-check the CV**: extract the PDF's text layer (`pdftotext`, optional dependency) and verify it the way an ATS parser sees it. Keywords the profile genuinely supports get added; genuine gaps stay visible, never stuffed.
8. **Present** the final output with a verification checklist

All claims in the CV and cover letter are verified against your actual profile. The system never fabricates skills or experience.

### What makes this workflow different

- **PDF verification loop.** Most LaTeX-resume templates produce "looks fine in the .tex" output that breaks in the PDF. The apply workflow compiles and visually inspects every PDF and applies targeted fixes until the layout is clean.
- **ATS verification on the PDF text layer.** The apply workflow extracts the compiled CV's text layer with `pdftotext` and verifies contact details, reading order, and keyword coverage.
- **Relevance-weighted CV cutting.** When a CV overflows 2 pages, it scores each candidate line by (a) relevance to the target posting, (b) uniqueness, and (c) cover letter dependencies, cutting the lowest-total-score line first.
- **Drafter-reviewer separation.** The drafter writes; a reviewer researches the company and critiques the drafts, which are then revised. On Claude Code this is a dispatched subagent with a fresh context; on Antigravity it's a simulated reviewer perspective within the same context.

## Customization

### Which files to edit manually

If you prefer editing files directly, edit both the Claude Code and Antigravity copies so the two harnesses stay in sync:

| Antigravity file | Claude Code equivalent | What to change |
|-------------------|-------------------------|---------------|
| `.agents/AGENTS.md` | `CLAUDE.md` | Your full profile (name, education, experience, skills, goals) |
| `.agents/skills/job-application-assistant/01-candidate-profile.md` | `.claude/skills/job-application-assistant/01-candidate-profile.md` | Structured version of your CV data |
| `.agents/skills/job-application-assistant/02-behavioral-profile.md` | `.claude/skills/job-application-assistant/02-behavioral-profile.md` | Your behavioral assessment or self-assessment |
| `.agents/skills/job-application-assistant/04-job-evaluation.md` | `.claude/skills/job-application-assistant/04-job-evaluation.md` | Skill match areas, career goals, motivation filters |
| `.agents/skills/job-application-assistant/05-cv-templates.md` | `.claude/skills/job-application-assistant/05-cv-templates.md` | Profile statement templates for different role types |
| `.agents/skills/job-application-assistant/07-interview-prep.md` | `.claude/skills/job-application-assistant/07-interview-prep.md` | Your STAR examples from actual experience |
| `.agents/skills/job-scraper/search-queries.md` | `.claude/skills/job-scraper/search-queries.md` | Job search queries for your skills and location |

The job-portal CLI tools (`.agents/skills/*-search/`) and `/add-portal`-generated skills are shared — both harnesses read them from the same `.agents/skills/` location, no duplication needed.

### Updating your search queries

As your priorities evolve, you can reconfigure just the job search:
> setup --section search

This re-runs the search configuration interview.

### LaTeX templates

The CV uses [moderncv](https://ctan.org/pkg/moderncv) (banking style). The cover letter uses a custom `cover.cls` with Lato/Raleway fonts.

To use your own template instead, run:
> add template

Point it at your `.tex` file. The command interviews you for the template's instructions, stores everything under `templates/`, and activates the template.

- `add template --list` shows registered templates
- `add template --use <name>` switches between them
- `add template --use default` reverts to the stock templates

### Job search tools

The four Danish CLI tools in `.agents/skills/` (Jobbank, Jobdanmark, Jobindex, Jobnet) demonstrate the pattern for building a job-portal integration for a specific market. If you're in a different country, run `/add-portal` (Claude Code) or say `add portal` (Antigravity).

Give it your local job board's URL. The command investigates the portal (search-URL pattern, result-page structure, robots.txt/access rules), scaffolds a CLI skill with the same structure, commands, and output contract as the shipped ones, and test-runs a live query before registering anything. Auth-walled portals are declined, and portals with restrictive terms get a prominent personal-use-only warning in the generated skill. The generated skill is market-specific and lives in your fork; the generator itself is the universal part.

Maintaining a fork adapted to your market or language? Add it to the [Community forks & adaptations](https://github.com/MadsLorentzen/ai-job-search/discussions/78) thread so others can find it.

For **country-agnostic** starting points outside Denmark, the repo ships two portal skills alongside the Danish demos:

- **`linkedin-search`** — built on LinkedIn's public, unauthenticated `jobs-guest` endpoints. Field-agnostic, **zero runtime dependencies** (runs with just `bun`), and takes the search location as an explicit flag, so it works for any market out of the box (`-l "Berlin, Germany"`, `-l "Mumbai, Maharashtra, India"`, `-l "Remote"`, …). Intended for **personal use only** — automated access is against LinkedIn's Terms of Service, so keep volume low. See `.agents/skills/linkedin-search/SKILL.md`.
- **`freehire-search`** — queries the [freehire.dev](https://freehire.dev) aggregator's public REST API (JSON, no API key). Tech-focused (software, data, engineering, DevOps, remote), multi-market via facet flags (`--region`, `--country`, `--remote`), and **zero runtime dependencies**. Unlike the HTML-scraping Danish portals, results come back structured (skills, seniority, category). The backend is MIT-licensed and [self-hostable](https://github.com/strelov1/freehire) — point `FREEHIRE_API_URL` at your own instance if you prefer. See `.agents/skills/freehire-search/SKILL.md`.

### Salary benchmarking

The salary tool works with any salary data you provide. See `tools/README_SALARY_TOOL.md` for details.

### Starting over

To wipe your profile data and start fresh, run `/reset profile` (Claude Code) or say `reset profile` (Antigravity) to clear skill files while preserving framework rules. `reset documents` deletes files from the `documents/` folder; `reset all` clears both.

## Tips for better results

### Profile depth matters

The single biggest factor in output quality is how much detail you put into your profile.

- **Role descriptions:** Describe what you actually did in each position.
- **Skills in context:** Describe how and where you applied your skills.
- **All onboarding paths work:** Richer input produces sharper output.

### Career path discovery

The framework supports both explicit targeting and latent opportunity discovery. To get the most from this, invest time during setup in describing what energized you, what drained you, and what you'd want more of.

## Contributing

Thinking about a PR? Read [CONTRIBUTING.md](CONTRIBUTING.md) first - it explains what gets merged, what lives in forks, and why.

## Acknowledgements

- [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search) — the upstream repository this framework is forked from, originally built for Claude Code.
- [Mikkel Krogholm](https://github.com/mikkelkrogsholm) ([skills repo](https://github.com/mikkelkrogsholm/skills)) for the original job search CLI skills.
- Adapted to also run on [Antigravity (Gemini)](https://gemini.google.com): a parallel `.agents/` skill tree, AGENTS.md rules, verification checklists, and compilation toolchain were added for the Gemini coding assistant, alongside the original `.claude/`/CLAUDE.md Claude Code framework.

## License

MIT
