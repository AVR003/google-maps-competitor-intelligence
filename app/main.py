import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    init_db,
    get_all_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project,
    get_competitors_by_project,
    add_competitor,
    update_competitor,
    delete_competitor,
    get_posts,
    get_scraping_logs,
    get_generated_ideas,
    get_generated_updates,
    get_setting,
    set_setting,
    get_latest_ai_analysis
)
from app.seed_data import seed_demo_data_if_empty
from app.models import (
    ProjectCreate,
    ProjectUpdate,
    CompetitorCreate,
    CompetitorUpdate,
    ScrapeRequest,
    IdeaGenerateRequest,
    FullUpdateGenerateRequest,
    SettingsUpdate
)
from app.scraper.scraper_engine import (
    scraper_state,
    start_scraping_job,
    resume_from_captcha,
    discover_competitors_by_keyword
)
from app.ai.ai_service import AIService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize SQLite DB and seed demo data if empty
    logger.info("Initializing SQLite database...")
    init_db()
    seed_demo_data_if_empty(force=False)
    logger.info("Ready to accept requests.")
    yield
    # Shutdown logic if any

app = FastAPI(
    title="Google Maps Competitor Update Intelligence Tool",
    description="Full-stack intelligence tool for tracking, analyzing, and generating Google Maps business posts.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for open accessibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=FileResponse)
async def serve_index():
    index_file = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_file):
        raise HTTPException(status_code=404, detail="Index HTML not found")
    return FileResponse(index_file)

# ----------------- PROJECTS API -----------------

@app.get("/api/projects")
async def list_projects():
    projects = get_all_projects()
    return {"projects": projects}

@app.post("/api/projects")
async def create_new_project(req: ProjectCreate):
    pid = create_project(
        name=req.name,
        our_profile_name=req.our_profile_name,
        our_profile_url=req.our_profile_url or "",
        keywords=req.keywords
    )
    return {"id": pid, "message": "Project created successfully"}

@app.get("/api/projects/{project_id}")
async def fetch_project(project_id: int):
    p = get_project_by_id(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@app.put("/api/projects/{project_id}")
async def modify_project(project_id: int, req: ProjectUpdate):
    p = get_project_by_id(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    update_project(project_id, req.name, req.our_profile_name, req.our_profile_url or "", req.keywords)
    return {"message": "Project updated successfully"}

@app.delete("/api/projects/{project_id}")
async def remove_project(project_id: int):
    delete_project(project_id)
    return {"message": "Project deleted successfully"}

# ----------------- COMPETITORS API -----------------

@app.get("/api/projects/{project_id}/competitors")
async def list_competitors(project_id: int):
    comps = get_competitors_by_project(project_id)
    return {"competitors": comps}

@app.post("/api/projects/{project_id}/competitors")
async def add_new_competitor(project_id: int, req: CompetitorCreate):
    cid = add_competitor(project_id, req.name, req.profile_url)
    return {"id": cid, "message": "Competitor added successfully"}

@app.put("/api/competitors/{competitor_id}")
async def edit_competitor(competitor_id: int, req: CompetitorUpdate):
    update_competitor(competitor_id, req.name, req.profile_url)
    return {"message": "Competitor updated successfully"}

@app.delete("/api/competitors/{competitor_id}")
async def delete_competitor_endpoint(competitor_id: int):
    delete_competitor(competitor_id)
    return {"message": "Competitor removed"}

# ----------------- SCRAPING & CAPTCHA API -----------------

@app.post("/api/projects/{project_id}/scrape")
async def trigger_scrape(project_id: int, req: ScrapeRequest):
    success, msg = start_scraping_job(
        project_id=project_id,
        competitor_ids=req.competitor_ids,
        simulate_captcha=req.simulate_captcha
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "simulate_captcha": req.simulate_captcha}

@app.get("/api/scraper/status")
async def get_scraper_status():
    return {
        "is_running": scraper_state.is_running,
        "status": scraper_state.status,
        "project_id": scraper_state.project_id,
        "current_competitor": scraper_state.current_competitor,
        "total_competitors": scraper_state.total_competitors,
        "processed_competitors": scraper_state.processed_competitors,
        "posts_found": scraper_state.posts_found,
        "new_posts_added": scraper_state.new_posts_added,
        "duplicates_skipped": scraper_state.duplicates_skipped,
        "images_downloaded": scraper_state.images_downloaded,
        "captcha_active": scraper_state.captcha_active,
        "manual_intervention_required": scraper_state.manual_intervention_required,
        "logs": scraper_state.logs[-40:],
        "error_message": scraper_state.error_message
    }

@app.post("/api/scraper/solve_captcha")
async def solve_captcha_endpoint():
    resume_from_captcha()
    return {"message": "Verification acknowledged. Scraper resuming."}

@app.get("/api/projects/{project_id}/logs")
async def get_project_scraping_logs(project_id: int):
    logs = get_scraping_logs(project_id)
    return {"logs": logs}

# ----------------- REPOSITORY POSTS API -----------------

@app.get("/api/projects/{project_id}/posts")
async def get_project_posts(
    project_id: int,
    competitor_id: int = Query(None),
    topic: str = Query(None),
    keyword: str = Query(None),
    search: str = Query(None)
):
    posts = get_posts(project_id, competitor_id=competitor_id, topic=topic, keyword=keyword, search=search)
    return {"posts": posts, "count": len(posts)}

# ----------------- AI ANALYSIS & TRENDS API -----------------

@app.post("/api/projects/{project_id}/analyze")
async def run_ai_analysis(project_id: int, force_refresh: bool = Query(False)):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    result = AIService.analyze_repository(project_id, project["our_profile_name"], force_refresh=force_refresh)
    return result

@app.get("/api/projects/{project_id}/analysis")
async def get_cached_analysis(project_id: int):
    cached = get_latest_ai_analysis(project_id)
    if not cached:
        # Generate automatically if empty
        project = get_project_by_id(project_id)
        if project:
            return AIService.analyze_repository(project_id, project["our_profile_name"], force_refresh=False)
        return {"analysis": None}
    return cached

# ----------------- CONTENT IDEA & UPDATE GENERATOR -----------------

@app.post("/api/projects/{project_id}/generate-ideas")
async def generate_content_ideas(project_id: int, req: IdeaGenerateRequest):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ideas = AIService.generate_ideas(
        project_id=project_id,
        client_name=project["our_profile_name"],
        keywords=project.get("keywords", []),
        count=req.count
    )
    return {"ideas": ideas, "count": len(ideas)}

@app.get("/api/projects/{project_id}/ideas")
async def list_generated_ideas(project_id: int):
    records = get_generated_ideas(project_id)
    return {"ideas": records}

@app.post("/api/projects/{project_id}/generate-update")
async def generate_complete_update(project_id: int, req: FullUpdateGenerateRequest):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_post = AIService.generate_full_update(
        project_id=project_id,
        client_name=project["our_profile_name"],
        topic=req.topic,
        idea_summary=req.idea_summary,
        keywords=project.get("keywords", [])
    )
    return update_post

@app.get("/api/projects/{project_id}/updates")
async def list_generated_updates(project_id: int):
    records = get_generated_updates(project_id)
    return {"updates": records}

# ----------------- KEYWORD DISCOVERY API (BONUS) -----------------

@app.get("/api/discover-competitors")
async def discover_competitors(keyword: str = Query(...)):
    results = discover_competitors_by_keyword(keyword)
    return {"keyword": keyword, "discovered_competitors": results}

# ----------------- SETTINGS & DEMO RESET API -----------------

@app.get("/api/settings")
async def get_settings():
    active_provider = get_setting("active_ai_provider", "builtin")
    gemini_key = get_setting("gemini_api_key", "")
    groq_key = get_setting("groq_api_key", "")
    return {
        "active_ai_provider": active_provider,
        "has_gemini_key": bool(gemini_key or os.environ.get("GEMINI_API_KEY")),
        "has_groq_key": bool(groq_key or os.environ.get("GROQ_API_KEY")),
        # Do not expose secret key strings to frontend
        "providers_available": [
            {"id": "builtin", "name": "Built-in Intelligent Engine (Offline NLP / 100% Reliable)", "requires_key": False},
            {"id": "gemini", "name": "Google Gemini 2.5 Flash", "requires_key": True},
            {"id": "groq", "name": "Groq LLaMA 3.3 (High Speed)", "requires_key": True}
        ]
    }

@app.post("/api/settings")
async def update_settings(req: SettingsUpdate):
    set_setting("active_ai_provider", req.active_ai_provider)
    if req.gemini_api_key is not None and req.gemini_api_key != "":
        set_setting("gemini_api_key", req.gemini_api_key.strip())
    if req.groq_api_key is not None and req.groq_api_key != "":
        set_setting("groq_api_key", req.groq_api_key.strip())
    return {"message": "Settings saved successfully", "active_provider": req.active_ai_provider}

@app.post("/api/reset-demo")
async def reset_demo_data():
    seed_demo_data_if_empty(force=True)
    return {"message": "Demo dataset re-seeded successfully with ABC Salon and 4 competitors."}
