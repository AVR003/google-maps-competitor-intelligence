# Examination Assignment Submission Document

---

## Project Title
**MapPulse AI – Google Maps Competitor Update Intelligence Platform**

- **Live Deployed Application URL:** `https://google-maps-competitor-intelligence.onrender.com` *(or your active live URL)*
- **GitHub Repository:** `https://github.com/AVR003/google-maps-competitor-intelligence`
- **Demo Subject:** ABC Salon, Kharghar (vs. 4 competitors: Enrich, Lakme, Toni & Guy, Jawed Habib)

---

## 1. Approach & Methodology

MapPulse AI is an end-to-end intelligence system designed for local businesses to monitor competitors' Google Maps Updates, identify promotional and topic trends, detect market gaps, and automatically draft high-converting, non-repetitive Google Maps update posts.

### Core Workflow & Architecture Steps:
1. **Multi-Project Management:** Supports project-level grouping of target business profiles, competitors, and localized search keywords. Pre-seeded with a realistic offline dataset for evaluation reliability.
2. **Automated Scraping & Anti-Automation Handling:**
   - Powered by a Python Selenium headless engine configured with stealth user-agents and dynamic DOM element extraction.
   - **CAPTCHA & Verification Protocol:** Gracefully detects verification challenges/rate limits, halts without crashing, triggers an interactive modal for manual confirmation, and records the intervention in audit logs.
3. **SHA-256 Duplicate Detection:** Every collected update is hashed (`SHA256(competitor + text + date)`). Re-scraping tests automatically identify and skip existing records, preserving repository uniqueness.
4. **AI-Driven Trend & Gap Analysis:** Analyzes competitor copy to generate the **Topic Trend Occurrence Matrix** (Topic, Competitors Using Topic, Count, Occurrence %), CTA breakdowns, and publishing patterns. Automated gap analysis highlights unexploited market opportunities.
5. **Content & Update Generation with Duplicate Prevention:** Users control idea volume (3, 10, 50 ideas). Prospective ideas are cross-referenced with persistent SQLite history to ensure fresh angles. One-click generation outputs complete copy, hashtags, Call-to-Action button, visual art direction, and AI image preview.

---

## 2. Technologies Used

- **Backend:** Python 3.14, FastAPI (Asynchronous REST API, OpenAPI/Swagger docs), Uvicorn.
- **Scraping & Automation:** Selenium WebDriver, BeautifulSoup4, WebDriver Manager.
- **Data Persistence:** SQLite (relational schema: projects, competitors, posts, logs, ideas, updates, settings).
- **Frontend & Visualizations:** HTML5, Tailwind CSS, Chart.js (trend visualizations), Lucide Icons.
- **AI & NLP Layer:** Multi-provider architecture supporting **Google Gemini 2.5 Flash**, **Groq LLaMA 3.3**, and an intelligent **Built-in Offline NLP Engine** for 100% evaluation reliability.
- **Deployment:** Render / Cloud container with Procfile configuration.

---

## 3. Key Screenshots of Working System

*(Paste your screenshots into these labeled sections in your final document)*

### Screenshot 1: Overview Dashboard & Analytics
> *Displays project details for ABC Salon Kharghar, tracked competitors, KPI metric cards, Chart.js topic distribution, and persistent scraping audit logs.*  
> **[INSERT SCREENSHOT 1 HERE]**

---

### Screenshot 2: Competitor Management, Scraper Console & Duplicate Detection
> *Shows monitored competitor profiles and the live terminal log demonstrating SHA-256 de-duplication ("9 found, 0 added, 9 duplicates skipped").*  
> **[INSERT SCREENSHOT 2 HERE]**

---

### Screenshot 3: AI Trend Occurrence Matrix & Strategic Gap Analysis
> *Displays the exact assignment Table 13 matrix (Hair Care Tips 50%, Festival Offers 36%, Before/After 24%) alongside actionable recommendations.*  
> **[INSERT SCREENSHOT 3 HERE]**

---

### Screenshot 4: Content Generator & Complete Ready-to-Publish Update
> *Shows user-selected idea batch generation and drafted complete Google Maps update post with full copy, location keywords, CTA, and visual mockups.*  
> **[INSERT SCREENSHOT 4 HERE]**

---

## 4. Bonus Features Implemented
- **Keyword-Based Competitor Discovery:** Discovers candidate businesses from local keywords (e.g. `'salon in Kharghar'`) and adds them directly to the queue with duplicate validation.
- **Competitive Gap Analysis:** Identifies content themes competitors are dominating versus untouched angles.
- **Offline Resilience:** Built-in heuristic NLP engine allows all scraping, analysis, and generation flows to operate seamlessly without requiring paid AI API credentials.
