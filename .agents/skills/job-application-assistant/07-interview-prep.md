# Interview Preparation Guide

<!-- SETUP: STAR examples are personalized by running /setup based on your actual experience -->

## STAR Format

Structure answers as: **Situation** (context), **Task** (your responsibility), **Action** (what you did), **Result** (outcome).

Keep answers to 1-2 minutes. Be specific. End with what you learned or would do differently.

## Ready-Made STAR Examples

<!-- These are populated by /setup from your actual experience. Below are templates showing the format. -->

### 1. Mobile Platform for Industrial Devices - Endava (IoT & BLE Connectivity)
**S:** Endava needed to build a specialized mobile platform to install, configure, and manage network-connected devices using wireless communication in field environments.
**T:** As React Native Developer, I was responsible for implementing device connectivity layers and resolving critical communication bugs under tight deadlines in a lean, 2-person team.
**A:** I optimized the hardware connectivity layers, developing robust Bluetooth Low Energy (BLE) and Wi-Fi communication protocols, and balanced rapid feature deployment with rigorous bug resolution.
**R:** Achieved stable, real-time device interaction under varying field conditions, reduced production defects, and maintained high system availability for technical operators.
**Use for:** "Tell me about a time you resolved a complex technical problem", "Describe working in a lean or fast-paced team"

### 2. Session Border Gateway Solution - DEK Technologies (High-Availability Backend)
**S:** DEK Technologies developed and enhanced high-availability Session Border Controller solutions for real-time telecom signaling.
**T:** As a Telecommunications Software Engineer, my task was to design, implement, and test core communication features aligned with strict signaling standards.
**A:** I wrote scalable backend features in Erlang, managed state via Mnesia databases, implemented SIP/Diameter/Megaco protocols, and defined comprehensive automated testing strategies to cover critical communication edge cases.
**R:** Delivered reliable, fault-tolerant signaling flows in production, significantly decreasing code defects and ensuring continuous uptime in real-time telecom environments.
**Use for:** "Describe a project requiring high reliability or performance", "How do you approach software quality and testing?"

### 3. Scrum Master Agile Leadership - DEK Technologies (Agile & Team Dynamics)
**S:** My engineering team faced communication overhead and uneven workload distribution during a high-stakes project phase.
**T:** I stepped into the Scrum Master role for a 5-person team to streamline work delivery and establish collaboration boundaries.
**A:** I facilitated daily standups, sprint planning, and retrospectives, introduced workload tracking dashboards in Jira, and mentored team members on Scrum principles to eliminate communication bottlenecks.
**R:** Successfully established a stable delivery cadence, eliminated double-work, and distributed the engineering workload evenly, boosting team morale and productivity.
**Use for:** "Tell me about a time you took the lead", "How do you handle team conflict or alignment issues?"

<!-- Add more STAR examples as needed. Aim for 4-6 covering different competencies. -->

## STAR Candidates (Complete Manually)

### Soi Trọ - AI-Orchestrated Go CLI Tool
**Source:** CV / GitHub project. A complete STAR already exists in `documents/applications/firegroup/interview_prep.md` (Q3) - copy and adapt from there rather than redrafting.
**What happened:** Built a Go CLI tool using the Google GenAI Go SDK and Gemini to extract and structure rental-listing details from screenshots/text, with Huh?/Bubble Tea TUI and OpenAPI 3.0 schema mapping, built through a structured AI agent orchestration loop.
**Why it matters:** Best answer for "describe a project you built using AI agents/tools" - demonstrates directing AI agents as an architect rather than just prompting.
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

### AI-Agent-Driven Engineering Velocity
**Source:** Interview prep pack. A complete STAR already exists in `documents/applications/firegroup/interview_prep.md` (Q1) - copy and adapt from there rather than redrafting.
**What happened:** Built a custom workspace workflow using Google Antigravity (Gemini) and Claude Code to draft Go struct definitions, scaffold unit tests for TDD, and write API documentation, reportedly cutting time spent on repetitive scaffolding by over 40%.
**Why it matters:** Directly answers "how do you use AI to boost engineering velocity" - a near-universal question given the candidate's AI-tooling positioning.
**S/T/A/R stub:**
- Situation:
- Task:
- Action:
- Result:

## Reusable Gap-Bridging Answers

These recur across almost every posting scored so far (MongoDB, Elasticsearch, Kubernetes/GCP, and AWS Lambda are all common gaps in `/rank` and `/upskill` output). Adapted from the Circa Pharmacy and FireGroup interview prep packs so they don't need to be redrafted per application.

### "Have you worked with MongoDB / Elasticsearch?"
> "My professional database experience is primarily with PostgreSQL, Mnesia, and Redis. I understand that MongoDB focuses on document validation rules and aggregation pipelines, while Elasticsearch uses inverted indexes for search relevance, and I'm comfortable with the Go driver integrations for both, though I don't have professional production experience with either yet."

### "How comfortable are you with Kubernetes / GCP?"
> "I'm comfortable with containerization principles and have worked alongside DevOps pipelines at DEK Technologies and Endava, including Docker workflows in my own projects. I haven't configured multi-region production clusters in GCP or Kubernetes myself - that's an area I'm actively upskilling in by building local clusters and writing Kubernetes manifests for Pods, Deployments, and Services, rather than something I'd claim as production experience."

### "Do you have AWS Lambda / serverless experience?"
> "My primary deployment experience is with containerized environments (Docker, Kubernetes), not serverless. I understand the FaaS model conceptually - stateless handlers, cold starts, API Gateway routing, event-source triggers - and Go's low cold-start overhead makes it a natural fit for Lambda, but I haven't shipped a production Lambda function yet."

## Common Tough Questions

### "Why did you leave / are you looking to leave?"
> "DEK Technologies merged into Endava, which shifted my recent focus to mobile client platforms. While I enjoyed building these wireless platforms, my passion is core backend engineering and high-availability systems. I am looking for a backend-focused role (using Go or Erlang) where I can build reliable platforms and contribute my agile team-coordination skills."

### "You don't have [specific skill/experience]."
> "While I don't have direct professional experience with [X] yet, I have a strong foundation in low-level communication protocols, databases, and general software architecture. For instance, when I transitioned from Erlang telecom backend work to React Native mobile development, I quickly mastered BLE and Wi-Fi connectivity APIs. I'm highly adaptable and eager to bring this same speed of learning to your tech stack."

### "Where do you see yourself in 5 years?"
> "I see myself as a Senior Backend / Systems Engineer who owns the design and implementation of highly available communication or cloud platforms. I also hope to continue mentoring junior engineers and helping teams scale their agile delivery processes."

### "What's your biggest weakness?"
> "My commitment to high-quality code can sometimes lead me to spend extra time writing highly exhaustive unit tests for minor features. To balance this, I've learned to categorize features by business risk and apply test coverage pragmatically to keep delivery timelines on track."

### "Why this company specifically?"
> Customize per company. Must reference: specific projects, company values, market position, or team structure. Never give a generic answer.

## Questions You Should Ask Interviewers

### About the Role
- "What does a typical week look like in this role?"
- "What would success look like in the first 6 months?"
- "What's the biggest challenge the team is facing right now?"

### About the Team
- "How big is the team, and how do you divide work?"
- "What does the development/project lifecycle look like, from idea to production?"
- "How do you onboard new team members?"

### About Tech & Growth
- "What's your current tech stack for [relevant area]?"
- "Is there room to grow into more architectural or strategic decisions?"
- "How does the team stay current with new tools and methods?"

### About Culture (use these to prevent disappointment)
- "How would you describe the team culture?"
- "What does professional development look like here?"
- "Is there flexibility for remote/hybrid work?"
- "What's the balance between development/new projects and maintenance work?"
- "How would you describe the leadership style in this team?"
- "What do people who thrive here have in common?"

## Phone/Video Interview Tips
- Have STAR examples written out (use this file)
- Keep a glass of water nearby
- Smile when speaking (it changes your tone)
- Ask for clarification if a question is vague
- It's OK to take 5 seconds to think before answering
- End with: "Is there anything else you'd like to know about my background?"

## After the Application (Best Practice)

### Follow-Up Etiquette
- **Don't call to "stand out"** or to learn more about the role post-submission - this risks a negative impression
- If the employer specified a timeline, respect it and wait
- If no timeline was given and significant time has passed (2+ weeks), a brief call to ask about status is acceptable
- If you have genuinely new, relevant information to share, a short follow-up is fine

### Thank-You Notes
- When you receive any update (interview invitation, rejection, or status update), send a brief thank-you message
- Express appreciation for their time and the process
- Keep it short (2-3 sentences)

## Roleplay Guidelines
When the user asks for interview practice:
1. Ask which role/company to simulate
2. Start with easy warm-up questions ("Tell me about yourself")
3. Progress to role-specific technical questions
4. Include 1-2 behavioral questions using the competencies from the job posting
5. End with a tough question or curveball
6. After each answer, give brief feedback: what worked, what to sharpen
7. Suggest which STAR example would work best for each question
