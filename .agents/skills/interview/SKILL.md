---
name: interview-prep-workflow
description: >
  Prepares the user for a real job interview by gathering company research, mapping STAR answers, creating a custom prep pack, and running a mock interview roleplay.
  Triggers on: interview prep, prepare for interview, /interview, mock interview, interview roleplay
---

# Prepare for an Interview on a Tracked Application

You are preparing the user for a real, scheduled interview on one of their applications. The frameworks for this already exist - `.agents/skills/job-application-assistant/07-interview-prep.md` (STAR examples, tough questions, questions to ask, roleplay protocol) and the Company Research Checklist in `.agents/skills/job-application-assistant/04-job-evaluation.md` - and the outcome archive records which stage the user is at. This command wires them together into a stage-specific prep pack and an optional mock interview.

Apply optimizes what the company reads; interview prep optimizes what the company hears. The bridge between them is consistency: the interviewer has read the submitted CV and cover letter, so everything prepared here must match what those documents claim.

Follow these steps **in order**.

---

## Step 0: Parse Input

Input arguments may contain a company name (optionally with a role), e.g., "acme".

- **With an argument:** match against `job_search_tracker.csv` rows. One match → proceed. Several → list and ask. None → the application isn't tracked; suggest registering it first via the outcome workflow, or accept posting details directly if the user wants to prep anyway.
- **Without an argument:** list tracker rows whose status suggests a live process (`interview`, `offer`, or recently `applied`) and ask which one.

---

## Step 1: Load the Application Context

1. **The archive** (maintained by the outcome workflow): `documents/applications/<company>_<role>/`
   - `job_posting.md` - the exact posting the user applied to
   - `cv_draft.tex` and `cover_letter.tex` - what was actually submitted. **These are what the interviewer read**; every talking point must be consistent with their claims.
   - `outcome.md` - the stage reached so far and any recorded feedback.
2. **Fallbacks:** posting via WebFetch on the tracker row's `source` URL, or ask the user to paste it; CV via `cv/main_<company>.tex` and cover letter via `cover_letters/cover_<company>_*.tex`. State plainly which context is missing.
3. **Ask the user what this interview is:** stage (phone screen / technical / case / final round), date, format, and who is interviewing (names and titles).
4. **Read the frameworks once**:
   - `.agents/skills/job-application-assistant/07-interview-prep.md`
   - `.agents/skills/job-application-assistant/01-candidate-profile.md`
   - `.agents/skills/job-application-assistant/02-behavioral-profile.md`
   - `.agents/skills/job-application-assistant/04-job-evaluation.md`

---

## Step 2: Research the Company (Interview-Focused)

Execute the Company Research Checklist: company website (mission, values, recent news), review sites, LinkedIn (team size, recent hires), and media coverage.

Additions for interview purposes:
- **Interviewer angle:** look up the interviewer's public professional profiles to anticipate their likely angle.
- **Conversation hooks:** 2-3 recent, verified company specifics the user can reference naturally in answers.

**Verify before using:** every company claim that will appear in the prep pack must be independently confirmed via WebSearch/WebFetch.

---

## Step 3: Build the Prep Pack

Assemble a stage-appropriate prep document:

### 1. Likely questions
1. **Recorded feedback from earlier stages** (`outcome.md`).
2. **The fit evaluation's gaps** - prepare honest bridge answers (acknowledge, connect adjacent experience, show the learning path). **Never prepare an answer that invents experience.**
3. **The posting's stated requirements**.
4. **The stage type** - phone screen, technical, or values round.

### 2. STAR answer mapping
Match the ready-made STAR examples in `07-interview-prep.md` to the likely questions using their "Use for" tags.
- For likely questions no existing STAR example covers, draft a new STAR answer grounded strictly in facts from `01-candidate-profile.md`. Include these in the prep pack.
- If setup left incomplete STAR stubs, surface them.

### 3. Consistency brief
Specific claims the submitted CV and cover letter make that the interviewer is most likely to probe. **No claim in the room that isn't on the paper.**

### 4. Tough questions, customized
Tough questions with per-application answers, includingverified company hooks.

### 5. Questions to ask
Pick 4-6 customized questions, omitting any the research already answers.

### 6. Logistics
Logistical notes, tips, and dates.

Save the pack to `documents/applications/<company>_<role>/interview_prep_<stage>.md`.

---

## Step 4: Offer a Mock Interview

Ask if the user wants to practice. If yes, run the roleplay **in this conversation** following the Roleplay Guidelines in `07-interview-prep.md` exactly: warm-up first, then role-specific technical questions, 1-2 behavioral questions, and one tough question or curveball. Give brief feedback after each answer.

Calibrate feedback against `02-behavioral-profile.md` to coach toward the user's natural register.

---

## Step 5: Close the Loop

End with:

> Good luck. After the interview, run the outcome workflow to log the stage and feedback.

Suggest appending user-approved draft STAR examples to `07-interview-prep.md`.
