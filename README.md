# Project Darwin — The Heinrich Co. Brain Model

An AI-powered content automation system that transforms how Heinrich Co. creates marketing content, qualifies leads, and measures performance.

**20x faster** content creation · **95% cost reduction** · **8 AI Skills** working together

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/naqi7272/project-darwin.git
cd project-darwin

# 2. Create virtual environment
python -m venv venv
source venv/Scripts/activate    # Windows Git Bash
# source venv/bin/activate      # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 5. Run
python app.py
# Server starts at http://127.0.0.1:5000
```

## Test Endpoints

```bash
# Health check
curl http://127.0.0.1:5000/

# Generate strategic brief (Skill #2)
curl -X POST http://127.0.0.1:5000/api/generate-brief \
  -H "Content-Type: application/json" \
  -d '{"keyword":"consulting services it"}'

# Write blog post (Skill #3)
curl -X POST http://127.0.0.1:5000/api/write-blog \
  -H "Content-Type: application/json" \
  -d '{"keyword":"consulting services it"}'

# Create social posts (Skill #4)
curl -X POST http://127.0.0.1:5000/api/create-social \
  -H "Content-Type: application/json" \
  -d '{"keyword":"consulting services it","platform":"linkedin"}'

# Generate design prompts (Skill #5)
curl -X POST http://127.0.0.1:5000/api/design-visuals \
  -H "Content-Type: application/json" \
  -d '{"keyword":"consulting services it","title":"IT Consulting Guide"}'

# Qualify leads (Skill #6)
curl -X POST http://127.0.0.1:5000/api/qualify-leads \
  -H "Content-Type: application/json" \
  -d '{"leads":[{"name":"Jenny Cohen","company":"Air Doctor","title":"CEO","source":"presto","buying_signal_score":8}]}'

# Analytics report (Skill #7)
curl -X POST http://127.0.0.1:5000/api/analytics-report \
  -H "Content-Type: application/json" \
  -d '{"period":"daily","content_pages":9,"total_views":14,"total_leads":179,"hot_leads":24}'

# LinkedIn post (Skill #8)
curl -X POST http://127.0.0.1:5000/api/linkedin-post \
  -H "Content-Type: application/json" \
  -d '{"pillar":"structural_intelligence"}'

# Full pipeline — end-to-end for one keyword
curl -X POST http://127.0.0.1:5000/api/full-pipeline \
  -H "Content-Type: application/json" \
  -d '{"keyword":"consulting services it"}'
```

## Project Structure

```
project-darwin/
├── app.py                        # Main Flask application (all endpoints)
├── requirements.txt              # Python dependencies (Python 3.12 compatible)
├── .env.example                  # Environment variable template
├── Dockerfile                    # Container config for Railway
├── railway.toml                  # Railway deployment settings
├── .gitignore
├── README.md
├── config/
│   └── __init__.py               # Centralized configuration
├── skills/
│   ├── __init__.py
│   ├── skill_1_brand_guardian.py  # Brand validation & guidelines
│   ├── skill_2_strategy.py       # Strategic brief generation
│   ├── skill_3_writer.py         # Blog post writing
│   ├── skill_4_social.py         # Platform-specific social content
│   ├── skill_5_designer.py       # Nano Banana design prompts
│   ├── skill_6_qualifier.py      # Lead scoring & qualification
│   ├── skill_7_analytics.py      # KPIs, reports, competitor tracking
│   └── skill_8_linkedin.py       # Camila's LinkedIn editorial posts
├── handlers/
│   └── __init__.py               # Plugin handler — routes commands to skills
└── integrations/
    └── __init__.py               # Claude API integration
```

## The 8 Skills

| # | Skill | Input | Output | Time |
|---|-------|-------|--------|------|
| 1 | Brand Guardian | Any content | Validation result | instant |
| 2 | Strategy Expert | Snoika keyword | Strategic brief (3 angles) | 2 min |
| 3 | Content Writer | Brief | 2400-word blog post | 15 min |
| 4 | Social Creator | Blog data | 5+ platform-specific posts | 10 min |
| 5 | Visual Designer | Blog data | 5 Nano Banana prompts | 5 min |
| 6 | Lead Qualifier | Lead list | Scored & staged leads | 2 min |
| 7 | Analytics Manager | Metrics data | KPI report + actions | 5 min |
| 8 | LinkedIn Optimizer | Pillar + topic | Camila's editorial post | 5 min |

## Tech Stack

- **Framework:** Flask 3.0 (Python 3.12)
- **AI Engine:** Claude API (Anthropic)
- **Hosting:** Railway
- **Database:** Supabase (optional)
- **Team Hub:** Notion (optional)

## Deploy to Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect your GitHub repo
4. Set environment variable: `ANTHROPIC_API_KEY`
5. Deploy — Railway auto-builds from Dockerfile

## Data Sources

- **Snoika** — 41 high-opportunity keywords
- **Google Search Console** — Current rankings (30 keywords)
- **Google Analytics 4** — Traffic & engagement
- **Presto** — Lead data (179+ leads)
- **Maverick** — Sales outreach
- **Sales Navigator** — LinkedIn lead intelligence
- **Google Sheets** — 6 operational sheets

---

Built for Heinrich Co. by Naqi · Project Darwin v2.0
