# Search Queries for Job Scraper

## Search Sites

Primary:
- **linkedin.com/jobs** - LinkedIn job listings (filter: Ho Chi Minh City, Vietnam)
- **vietnamworks.com** - Leading Vietnamese job portal
- **itviec.com** - Top developer-focused portal in Vietnam
- **topdev.vn** - IT recruiter and job board in Vietnam
- **bebee.com** - Global job aggregator with active Vietnamese listings

## Query Categories

Queries are grouped by priority.

### Priority 1: Backend Developer (Go)

These match your strongest and most desired career direction.

```
site:itviec.com "Golang" "Ho Chi Minh"
site:topdev.vn "Golang" "Ho Chi Minh"
site:linkedin.com/jobs "Golang Developer" "Ho Chi Minh City"
site:linkedin.com/jobs "Go Backend Engineer" "Ho Chi Minh City"
site:linkedin.com/jobs "Software Engineer Go" "Ho Chi Minh City"
site:linkedin.com/jobs "Backend Developer HCMC" "Ho Chi Minh City"
site:itviec.com "Go Backend Engineer" "Ho Chi Minh"
site:topdev.vn "Backend Developer" "Go" "Ho Chi Minh"
site:bebee.com "Golang" "Ho Chi Minh"
```

### Priority 2: React Native / Mobile Developer

These leverage your recent project experience at Endava.

```
site:itviec.com "React Native" "Ho Chi Minh"
site:topdev.vn "React Native" "Ho Chi Minh"
site:linkedin.com/jobs "React Native Developer" "Ho Chi Minh City"
site:bebee.com "React Native" "Ho Chi Minh"
```

### Priority 3: Software Engineer

General software engineering roles targeting your languages.

```
site:itviec.com "Go" "Ho Chi Minh"
site:linkedin.com/jobs "Software Engineer" "Go" "Ho Chi Minh City"
```

### Priority 4: Scrum Master / Agile Leader

Roles focusing on agile team leadership.

```
site:vietnamworks.com "Scrum Master" "Ho Chi Minh"
site:linkedin.com/jobs "Scrum Master" "Ho Chi Minh City"
```

## Location Filter

Acceptable areas:
- Ho Chi Minh City (particularly District 1, District 3, District 7, Tan Binh, Binh Thanh)
- Remote (within Vietnam)

## Date Filter

Only include jobs posted within the last 14 days, or with an application deadline that has not yet passed. If a posting date cannot be determined, include it but flag as "date unknown".

## Adapting Queries

If the user specifies a focus area, select queries from the matching category and also generate 2-3 custom queries for that focus. For example:
- "scrape [focus_area]" -> relevant category queries + custom focus-specific queries
