# MapPulse AI - Google Maps Competitor Update Intelligence Tool
### Technical Development Examination Assignment Implementation

**MapPulse AI** is a complete, web-based competitor intelligence platform engineered specifically for **Google Maps Updates / Business Profile Posts**. 

The system collects, de-duplicates, and stores competitor update posts, runs AI content and trend analysis across local markets, detects strategic gaps, and generates complete, non-repetitive, ready-to-publish Google Maps updates.

---

## 🌟 Key Architecture & Capabilities

```
+-----------------------------------------------------------------------------------+
|                                  WEB FRONTEND                                     |
|  - Modern, responsive SPA (Tailwind CSS, Lucide icons, Chart.js)                  |
|  - Live Scraper Terminal Console & Real-time Status Banner                        |
|  - Interactive CAPTCHA Intervention & Manual Resolution Modal                     |
|  - Topic Trend Matrix (PDF Page 4), Gap Analysis & Strategic Recommendations     |
|  - Controllable Idea Generator (3, 10, 50) + Full Post Drafts + Copy Clipboard    |
|  - Embedded Step-by-Step Voiceover Demo Script Tab                                |
+-----------------------------------------------------------------------------------+
                                         │  HTTP / REST API (JSON)
                                         ▼
+-----------------------------------------------------------------------------------+
|                                FASTAPI BACKEND                                    |
|  - App Lifespan & Auto-Seeding: Realistic Pre-populated Demo Dataset              |
|  - REST Endpoints: Projects, Competitors, Scraping, Repository, AI, Settings      |
|  - Duplicate Detection Engine: SHA-256 content hashing                            |
|  - Anti-Automation & CAPTCHA Protocol Manager                                     |
+-----------------------------------------------------------------------------------+
             │                                                  │
             ▼                                                  ▼
+-------------------------+                       +---------------------------------+
|  PYTHON SCRAPING LAYER  |                       |       MULTI-AI PROVIDER         |
| - Selenium Chrome Head- |                       | - Built-in Intelligent NLP      |
|   less with Stealth DOM |                       |   (100% Offline Reliable)       |
| - Fallback Harvest Pool |                       | - Google Gemini 2.5 Flash       |
| - Persistent Run Logs   |                       | - Groq LLaMA 3.3 (High Speed)   |
+-------------------------+                       +---------------------------------+
             │                                                  │
             └───────────────────────┬──────────────────────────┘
                                     ▼
                      +-----------------------------+
                      |   PERSISTENT SQLITE REPO    |
                      | - projects                  |
                      | - competitors               |
                      | - scraped_posts             |
                      | - scraping_logs             |
                      | - generated_ideas           |
                      | - generated_updates         |
                      | - ai_analyses               |
                      | - settings                  |
                      +-----------------------------+
```

---

## 📋 Evaluation Checklist & Section Mapping

| Section | Feature Requirement | Implementation Details |
|---|---|---|
| **1 - 3** | Project-based Workflow | Supports multiple projects with client profile, competitors, and target search keywords. Seeded with default **ABC Salon, Kharghar**. |
| **4** | Scope of Data | Captures competitor name, profile URL, post URL, copy text, published dates, media/images, detected CTA, detected keywords, detected topic, timestamp, and content fingerprint. |
| **5** | Competitor Management | Add, edit, remove competitors manually. View competitor post count, last scraped date, and trigger single-competitor re-scrapes. |
| **6 & 25** | Keyword-Based Discovery | **Bonus Feature**: Enter keywords like `'salon in Kharghar'` to discover candidate competitors with ratings and addresses, and add them directly to project with duplicate protection. |
| **7** | Python Scraping Engine | Python-based Selenium WebDriver with stealth headers, dynamic DOM parser, and resilient fallback harvest pool. |
| **8 & 9** | CAPTCHA Handling | Detects verification challenges, triggers `"CAPTCHA_REQUIRED"` state, notifies the user via an interactive modal, logs `manual_intervention_required: 1`, and resumes upon confirmation. Includes a **"Simulate CAPTCHA"** button for the evaluation video demonstration. |
| **9** | Demo Dataset | Pre-populated realistic demo dataset featuring **ABC Salon Kharghar** and 4 competitors (**Enrich, Lakme, Toni & Guy, Jawed Habib**) with 18+ rich updates and authentic images. Evaluators can test without performing a live scrape. |
| **10** | Persistent Repository | Filter by competitor, topic, or keyword; search post copy; inspect photos in lightbox; view SHA-256 fingerprint; open source links. |
| **11** | Duplicate Detection | SHA-256 fingerprint hashing of `(competitor_name + text + date)`. Re-scraping ignores duplicates and records them in logs. |
| **12 & 13**| AI Content & Trend Matrix | Computes Topic Occurrence Table (exactly like PDF Page 4: *Topic \| Competitors Using Topic \| Occurrence %*). Identifies CTA patterns, top keywords, and publishing frequency. |
| **14 & 15**| Content & Update Generator | User-controlled batch count (3, 10, 50, etc.). One-click drafts full Google Maps updates (complete copy, emojis, location keywords, suggested photo concept, Call to Action, and AI visual graphic). |
| **16** | Duplicate Prevention | Compares prospective ideas against historical SQLite records (`generated_ideas`) to ensure previously generated ideas are never repeated. |
| **17** | Fresh Scraping | Supports re-scraping existing competitors; updates statistics; skips existing posts; captures newly published posts. |
| **18** | Multi-AI Providers | Built-in Intelligent NLP Engine (Offline / zero API key required), Google Gemini 2.5 Flash, and Groq LLaMA 3.3. Key entry safely managed via Settings modal. |
| **20 & 21**| Dashboard & Persistent Logs | Top-level KPI metrics cards, Chart.js topic distribution, CTA breakdown, and persistent SQLite scraping audit log with timestamps, new added, duplicates skipped, and CAPTCHA status. |
| **22** | Hosting Requirement | Easily deployable to Render, Railway, Hugging Face Spaces, or ngrok for open evaluator access without authentication. |

---

## 🚀 Quick Start Guide

### 1. Installation

Ensure Python 3.10+ is installed. In PowerShell or Terminal:

```bash
cd C:\Users\aakas\.gemini\antigravity\scratch\google-maps-competitor-intelligence
pip install -r requirements.txt
```

### 2. Launching the Platform

Run:
```bash
python run.py
```

Open your browser to:
👉 **`http://localhost:8000`**

Interactive OpenAPI Documentation:
👉 **`http://localhost:8000/docs`**

---

## 🌐 Online Deployment Guide (Hosting Requirement - Section 22)

The assignment requires the application to be hosted online and accessible without logging in. Here are the 2 fastest ways to deploy:

### Option A: Free Cloud Deployment via Render.com (Recommended)
1. Push this project folder to your GitHub repository.
2. Go to [Render.com](https://render.com) and click **New Web Service**.
3. Connect your repository.
4. Set:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Render generates a public URL (e.g., `https://map-pulse-ai.onrender.com`) that anyone can open without login!

### Option B: Instant Public Tunnel via ngrok or Cloudflare Tunnel
For an immediate live URL from your computer during evaluation:
```bash
# If using ngrok:
ngrok http 8000
```
This gives you a public HTTPS URL (e.g. `https://xxxx.ngrok-free.app`) instantly.

---

## 📽️ Video Recording & Voiceover Cue Sheet

The assignment mandates submitting a video demonstration. We have embedded the complete script into the web app itself under the **"Voiceover & Demo Script"** tab.

See [`VIDEO_VOICEOVER_SCRIPT.md`](./VIDEO_VOICEOVER_SCRIPT.md) for the complete minute-by-minute cues and word-for-word transcript.
