# Google Maps Competitor Update Intelligence Tool
## Complete Video Recording Walkthrough & Voiceover Script

This document is your **word-for-word voiceover script** and **screen recording guide** to record your project evaluation video (Mandatory Demonstration, Sections 24 & 26).

---

### 🎬 Recording Checklist & Setup
- **Screen Recorder**: Use OBS Studio, Loom, or Windows Xbox Game Bar (`Win + Alt + R`).
- **Resolution**: 1080p full-screen browser view.
- **Application URL**: `http://localhost:8000` (or your deployed URL).
- **Duration**: ~3 to 4 minutes total.

---

### ⏱️ Minute-by-Minute Cue Sheet & Script

---

#### 📍 Scene 1: Introduction & Project Overview (0:00 - 0:35)
- **On Screen:** Start on the **Dashboard** tab (`http://localhost:8000`).
- **Visual Action:** Point your mouse at the project title `"ABC Salon - Kharghar Intelligence"`, the client profile `"ABC Salon, Sector 7, Kharghar"`, and the four key metric cards at the top.

🎙️ **Voiceover (Read this):**
> *"Hello everyone! Today, I am demonstrating my submission for the Google Maps Competitor Update Intelligence Tool assignment.*
>
> *The objective of this web application is to monitor Google Maps updates and posts from local competitor businesses, store them in a persistent repository, run AI-driven trend analysis to uncover what competitors are publishing, and generate fresh, high-converting Google Maps updates for our client business without repeating past ideas.*
>
> *For this evaluation, we are using the exact example from the assignment specification: ABC Salon in Kharghar, Navi Mumbai, monitoring four leading local competitors: Enrich Salon, Lakme Salon, Toni & Guy, and Jawed Habib."*

---

#### 📍 Scene 2: Competitor Management & Duplicate Detection (0:35 - 1:20)
- **On Screen:** Click on the **"Competitors & Scraper"** tab.
- **Visual Action:** 
  1. Show the competitor cards list (Enrich, Lakme, Toni & Guy, Jawed Habib).
  2. Point out the "Add Competitor Manually" button.
  3. Click the **"Scrape All Now"** button. The Live Console will show logs streaming in real-time.
  4. Point out how the console identifies newly discovered updates versus duplicates using SHA-256 fingerprinting.

🎙️ **Voiceover (Read this):**
> *"Under the Competitors and Scraper tab, users can manually add, edit, or remove competitor Google Maps profiles. In the live terminal below, our Python-based Selenium scraping engine communicates with Google Maps to parse recent updates, extracting text, timestamps, photos, and calls to action.*
>
> *Notice our duplicate detection mechanism in action: each post is assigned a unique SHA-256 fingerprint generated from the business name, normalized text, and timestamp. When we run another scrape, previously stored posts are automatically identified as duplicates and skipped rather than creating duplicate records, ensuring database integrity."*

---

#### 📍 Scene 3: CAPTCHA & Anti-Automation Handling (1:20 - 1:55)
- **On Screen:** Click the **"Test CAPTCHA"** (or **"Simulate CAPTCHA"**) button.
- **Visual Action:**
  1. The scraper console will flag `⚠️ Google Anti-Automation challenge detected! CAPTCHA screen presented.`
  2. The interactive **CAPTCHA modal** will pop up on the screen.
  3. Point to the modal, then click **"Verification Completed / Continue Scraping"**.
  4. Show how the scraper resumes immediately and finishes the job.

🎙️ **Voiceover (Read this):**
> *"As required in Section 8 of the assignment, the system must handle Google Maps CAPTCHA and anti-automation controls gracefully.*
>
> *When a verification challenge or rate limit is encountered, the scraper halts safely rather than silently failing. It immediately triggers a verification notification in the web interface and marks in persistent logs that manual intervention was required.*
>
> *Once the user completes verification and clicks 'Continue Scraping', the worker automatically resumes its pipeline and processes the remaining competitors."*

---

#### 📍 Scene 4: Post Repository & Data Exploration (1:55 - 2:35)
- **On Screen:** Switch to the **"Post Repository"** tab.
- **Visual Action:**
  1. Scroll through the grid of scraped competitor updates showing photos, text, badges, and CTAs.
  2. Type `"keratin"` or `"monsoon"` into the Search bar to show real-time filtering.
  3. Filter by competitor using the dropdown (e.g. choose *"Enrich Salon"*).
  4. Click on any card to open the **Lightbox view** showing high-res photo, full copy, and detected tags.

🎙️ **Voiceover (Read this):**
> *"Moving to the Post Repository tab, non-technical users can easily search, filter, and inspect collected competitor updates. We can filter by competitor, content topic, or specific search keywords like 'keratin' or 'bridal'.*
>
> *Each record displays the competitor name, published date, call-to-action button, extracted SEO keywords, and content fingerprint, along with a direct link to the original Google Maps update source."*

---

#### 📍 Scene 5: AI Trend & Competitor Gap Analysis (2:35 - 3:15)
- **On Screen:** Switch to the **"AI Trend & Gap Analysis"** tab.
- **Visual Action:**
  1. Point to the **Topic Trend Occurrence Matrix** table (highlighting columns: Topic, Competitors Using Topic, Post Count, Occurrence %).
  2. Scroll down to show the **Competitor Gap Analysis** and **Actionable Strategy Recommendations** cards.
  3. Point out the badge showing the active AI provider (e.g., Built-in Intelligent Engine, Gemini, or Groq).

🎙️ **Voiceover (Read this):**
> *"Under the AI Trend Analysis tab, the platform runs deep content analysis using our integrated AI layer. It generates the exact Topic Occurrence Matrix required in Section 13 of the assignment specification—calculating how frequently each topic appears across competitors, such as Hair Care Tips at 50% and Festival Offers at 36%.*
>
> *Furthermore, as a bonus feature, the system conducts automated Gap Analysis, identifying which topics competitors are dominating and delivering concrete strategic recommendations to help ABC Salon increase its Google Maps search visibility."*

---

#### 📍 Scene 6: Content Generator, Duplicate Prevention & Final Updates (3:15 - 4:00)
- **On Screen:** Switch to the **"Content & Update Generator"** tab.
- **Visual Action:**
  1. In the "Number of Ideas" dropdown, select **3 Ideas** (or 5/10) and click **"Generate Ideas"**.
  2. Show the newly generated cards with Strategic Angle, Idea Summary, and Target Audience.
  3. Click **"Draft Full Google Maps Post"** on one of the ideas.
  4. Scroll down to show the completed update post: complete copy, relevant keywords, Call to Action button, suggested image concept, and AI graphic preview.
  5. Scroll down to the **"Historical Generated Ideas Repository"** table to show that past ideas are tracked in SQLite so they are never repeated.

🎙️ **Voiceover (Read this):**
> *"Now for the final stage: Content Planning and Generation. Users can control the exact number of ideas requested—such as 3, 10, or 50.*
>
> *To satisfy Section 16, duplicate prevention is strictly enforced: every generated concept is recorded in our SQLite database, and past ideas are passed into the AI prompt to prevent repetitive suggestions.*
>
> *With one click on 'Draft Full Google Maps Post', the system generates a complete, publish-ready Google Maps update with engaging emojis, local Kharghar location keywords, Call to Action button, photographic art direction, and AI visual mockup.*
>
> *In the settings, users can seamlessly switch between our 100% reliable built-in NLP engine, Google Gemini, and Groq LLaMA models.*
>
> *Thank you for reviewing the Google Maps Competitor Update Intelligence Tool!"*

---

### 💡 Extra Tips for Recording
1. Keep your voice confident, clear, and steady.
2. You do not need to show your face; a clean screen recording with microphone voiceover is standard and ideal.
3. If you make a small stumble while speaking, pause for 2 seconds and re-read the sentence; you can easily trim it or leave it natural!
