# GovTruth — Verification Methodology

## Core Principle
We never publish a finding without at least 
TWO independent sources confirming it.

## Data Hierarchy

### Tier 1 — Primary Sources (Highest Trust)
- ECI official affidavits
- CAG audit reports  
- Parliamentary Q&A records
- PFMS fund flow data
- Court records and charge sheets

### Tier 2 — Secondary Sources (Supporting)
- Satellite imagery (ESA Sentinel-2)
- MCA21 corporate filings
- SEBI disclosures
- News archives (for timeline verification)

### Tier 3 — Citizen Reports (Flagging Only)
- Require Tier 1 or 2 confirmation
- Never published standalone
- Used to direct investigation

## Confidence Scoring

Every finding gets a confidence score:

| Score | Meaning |
|-------|---------|
| 90-100 | Multiple primary sources confirm |
| 70-89 | One primary + one secondary source |
| 50-69 | Single primary source |
| Below 50 | Under investigation — not published |

## What We Never Do
- Publish unverified claims
- Use anonymous sources as primary evidence
- Make accusations — we publish data and questions
- Accept information we cannot independently verify
- Cover parties selectively

## Legal Framework
- All published data from official public records
- Statistical analysis is not accusation
- Sources cited on every finding
- Methodology is open source and auditable
```

---

**Right Now — Your GitHub Should Look Like:**
```
github.com/govttruth
└── govtruth-core (PUBLIC REPO)
    ├── README.md        ← Mission statement
    ├── ROADMAP.md       ← Development plan
    ├── docs/
    │   └── methodology.md
    ├── scrapers/
    ├── analyzers/
    ├── api/
    ├── database/
    └── legal/
```

**That's a real project. Not an idea. A real project.**

---

**After GitHub — Next 2 Hours:**

**Register these right now:**
```
1. earthengine.google.com/signup
   Time: 15 minutes
   
2. data.gov.in/user/register  
   Time: 5 minutes — instant API key
   
3. Internet Freedom Foundation
   internetfreedom.in/contact
   Send email from ProtonMail:
   
   Subject: Legal support request — 
            civic transparency platform
   
   Body:
   "I am building an open source government 
   accountability platform using exclusively 
   public data sources. The platform tracks 
   MP asset declarations, CAG findings, and 
   government contract data. I would like to 
   understand the legal framework for this 
   work. Can we schedule a consultation?"
   
   Time: 10 minutes
```

---

**Tonight — First Code Commit:**

Copy the database schema from our conversation into:
`govtruth-core/database/schema.sql`

Copy the ECI collector script into:
`govtruth-core/scrapers/eci_collector.py`

Commit with message:
```
git commit -m "Initial commit — 
data collection infrastructure"
```

**GovTruth has its first code.**

---

**This Week's Milestones:**
```
TODAY (Day 1):
✓ GitHub created — govttruth
✓ ProtonMail secured
□ First repo with README
□ Google Earth Engine registered
□ data.gov.in API key
□ IFF contact email sent
□ First code committed

DAY 2-3:
□ ECI data downloading
□ Database schema live
□ First analysis running

DAY 4-5:
□ First real MP data in system
□ First statistical flags
□ Show to one trusted person for feedback

END OF WEEK 1:
□ Working data pipeline
□ First 3 findings identified
□ Journalist contact initiated
```

---

**One More Thing Akshay:**

Share the GitHub link publicly when first real data is in.

Tweet from a GovTruth Twitter account:
```
"We are building India's first satellite-verified, 
AI-powered government accountability platform.

All data from official public sources.
No political affiliation.
Open source.

We just started. Follow the build.

github.com/govttruth
#GovTruth #TransparentIndia"
