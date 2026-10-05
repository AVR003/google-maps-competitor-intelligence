import sqlite3
import os
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "intelligence.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        our_profile_name TEXT NOT NULL,
        our_profile_url TEXT,
        keywords TEXT DEFAULT '[]',
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS competitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        profile_url TEXT NOT NULL,
        last_scraped_at TEXT,
        last_status TEXT DEFAULT 'idle',
        post_count INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS scraped_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        competitor_id INTEGER NOT NULL,
        competitor_name TEXT NOT NULL,
        post_url TEXT,
        post_text TEXT NOT NULL,
        published_date TEXT,
        media_urls TEXT DEFAULT '[]',
        call_to_action TEXT,
        detected_keywords TEXT DEFAULT '[]',
        detected_topic TEXT,
        scrape_date TEXT NOT NULL,
        content_hash TEXT UNIQUE NOT NULL,
        source_reference TEXT,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
        FOREIGN KEY(competitor_id) REFERENCES competitors(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS scraping_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        competitor_name TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        posts_found INTEGER DEFAULT 0,
        new_posts_added INTEGER DEFAULT 0,
        duplicates_skipped INTEGER DEFAULT 0,
        images_downloaded INTEGER DEFAULT 0,
        failures INTEGER DEFAULT 0,
        captcha_status TEXT DEFAULT 'None',
        manual_intervention_required INTEGER DEFAULT 0,
        error_info TEXT,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS generated_ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        angle TEXT,
        idea_summary TEXT NOT NULL,
        target_audience TEXT,
        created_at TEXT NOT NULL,
        batch_id TEXT,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS generated_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        full_copy TEXT NOT NULL,
        relevant_keywords TEXT,
        call_to_action TEXT,
        suggested_image_concept TEXT,
        ai_image_url TEXT,
        created_at TEXT NOT NULL,
        provider_used TEXT,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS ai_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        analysis_json TEXT NOT NULL,
        provider_used TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)

    conn.commit()
    conn.close()

def compute_post_hash(competitor_name: str, post_text: str, published_date: Optional[str] = "") -> str:
    """Computes a SHA256 unique fingerprint for duplicate detection."""
    clean_text = " ".join((post_text or "").lower().split())
    clean_name = (competitor_name or "").strip().lower()
    clean_date = (published_date or "").strip().lower()
    raw = f"{clean_name}|{clean_text}|{clean_date}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

# Project Helpers
def get_all_projects() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["keywords"] = json.loads(d["keywords"]) if d["keywords"] else []
        result.append(d)
    return result

def get_project_by_id(project_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["keywords"] = json.loads(d["keywords"]) if d["keywords"] else []
    return d

def create_project(name: str, our_profile_name: str, our_profile_url: str = "", keywords: List[str] = None) -> int:
    conn = get_db_connection()
    now = datetime.now().isoformat()
    kw_json = json.dumps(keywords or [])
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (name, our_profile_name, our_profile_url, keywords, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, our_profile_name, our_profile_url, kw_json, now)
    )
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()
    return project_id

def update_project(project_id: int, name: str, our_profile_name: str, our_profile_url: str = "", keywords: List[str] = None):
    conn = get_db_connection()
    kw_json = json.dumps(keywords or [])
    conn.execute(
        "UPDATE projects SET name = ?, our_profile_name = ?, our_profile_url = ?, keywords = ? WHERE id = ?",
        (name, our_profile_name, our_profile_url, kw_json, project_id)
    )
    conn.commit()
    conn.close()

def delete_project(project_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()

# Competitor Helpers
def get_competitors_by_project(project_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM competitors WHERE project_id = ? ORDER BY id ASC", (project_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_competitor(project_id: int, name: str, profile_url: str) -> int:
    conn = get_db_connection()
    now = datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO competitors (project_id, name, profile_url, created_at) VALUES (?, ?, ?, ?)",
        (project_id, name.strip(), profile_url.strip(), now)
    )
    conn.commit()
    comp_id = cursor.lastrowid
    conn.close()
    return comp_id

def update_competitor(comp_id: int, name: str, profile_url: str):
    conn = get_db_connection()
    conn.execute(
        "UPDATE competitors SET name = ?, profile_url = ? WHERE id = ?",
        (name.strip(), profile_url.strip(), comp_id)
    )
    conn.commit()
    conn.close()

def delete_competitor(comp_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM competitors WHERE id = ?", (comp_id,))
    conn.commit()
    conn.close()

# Scraped Post Helpers
def get_posts(project_id: int, competitor_id: Optional[int] = None, topic: Optional[str] = None, keyword: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = "SELECT * FROM scraped_posts WHERE project_id = ?"
    params: List[Any] = [project_id]

    if competitor_id:
        query += " AND competitor_id = ?"
        params.append(competitor_id)
    if topic:
        query += " AND detected_topic = ?"
        params.append(topic)
    if search:
        query += " AND (post_text LIKE ? OR competitor_name LIKE ? OR detected_keywords LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        d["media_urls"] = json.loads(d["media_urls"]) if d["media_urls"] else []
        d["detected_keywords"] = json.loads(d["detected_keywords"]) if d["detected_keywords"] else []
        if keyword:
            if not any(keyword.lower() in kw.lower() for kw in d["detected_keywords"]):
                continue
        result.append(d)
    return result

def insert_scraped_post(
    project_id: int,
    competitor_id: int,
    competitor_name: str,
    post_text: str,
    post_url: str = "",
    published_date: str = "",
    media_urls: List[str] = None,
    call_to_action: str = "",
    detected_keywords: List[str] = None,
    detected_topic: str = "",
    source_reference: str = ""
) -> bool:
    """Inserts post if not duplicate. Returns True if inserted, False if duplicate."""
    content_hash = compute_post_hash(competitor_name, post_text, published_date)
    conn = get_db_connection()
    now = datetime.now().isoformat()
    try:
        conn.execute(
            """INSERT INTO scraped_posts 
            (project_id, competitor_id, competitor_name, post_url, post_text, published_date, media_urls, 
             call_to_action, detected_keywords, detected_topic, scrape_date, content_hash, source_reference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                project_id, competitor_id, competitor_name, post_url, post_text, published_date,
                json.dumps(media_urls or []), call_to_action, json.dumps(detected_keywords or []),
                detected_topic, now, content_hash, source_reference
            )
        )
        # Update competitor post_count
        conn.execute(
            "UPDATE competitors SET post_count = (SELECT COUNT(*) FROM scraped_posts WHERE competitor_id = ?), last_scraped_at = ? WHERE id = ?",
            (competitor_id, now, competitor_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Duplicate detected
        conn.close()
        return False

# Logs Helpers
def add_scraping_log(
    project_id: int,
    competitor_name: str,
    start_time: str,
    end_time: str,
    posts_found: int,
    new_posts_added: int,
    duplicates_skipped: int,
    images_downloaded: int = 0,
    failures: int = 0,
    captcha_status: str = "None",
    manual_intervention_required: bool = False,
    error_info: str = ""
) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO scraping_logs 
        (project_id, competitor_name, start_time, end_time, posts_found, new_posts_added, duplicates_skipped, 
         images_downloaded, failures, captcha_status, manual_intervention_required, error_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            project_id, competitor_name, start_time, end_time, posts_found, new_posts_added,
            duplicates_skipped, images_downloaded, failures, captcha_status,
            1 if manual_intervention_required else 0, error_info
        )
    )
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return log_id

def get_scraping_logs(project_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM scraping_logs WHERE project_id = ? ORDER BY id DESC LIMIT ?",
        (project_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Ideas Helpers
def get_generated_ideas(project_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM generated_ideas WHERE project_id = ? ORDER BY id DESC", (project_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_generated_ideas(project_id: int, ideas: List[Dict[str, Any]], batch_id: str):
    conn = get_db_connection()
    now = datetime.now().isoformat()
    for idea in ideas:
        conn.execute(
            """INSERT INTO generated_ideas (project_id, topic, angle, idea_summary, target_audience, created_at, batch_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                project_id,
                idea.get("topic", "General"),
                idea.get("angle", ""),
                idea.get("idea_summary", idea.get("title", "")),
                idea.get("target_audience", "Local Customers"),
                now,
                batch_id
            )
        )
    conn.commit()
    conn.close()

# Updates Helpers
def save_generated_update(project_id: int, update_data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    now = datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO generated_updates 
        (project_id, topic, full_copy, relevant_keywords, call_to_action, suggested_image_concept, ai_image_url, created_at, provider_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            project_id,
            update_data.get("topic", "Update"),
            update_data.get("full_copy", ""),
            update_data.get("relevant_keywords", ""),
            update_data.get("call_to_action", "Call Now"),
            update_data.get("suggested_image_concept", ""),
            update_data.get("ai_image_url", ""),
            now,
            update_data.get("provider_used", "AI Engine")
        )
    )
    conn.commit()
    uid = cursor.lastrowid
    conn.close()
    return uid

def get_generated_updates(project_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM generated_updates WHERE project_id = ? ORDER BY id DESC", (project_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# AI Analysis Cache
def save_ai_analysis(project_id: int, analysis: Dict[str, Any], provider: str):
    conn = get_db_connection()
    now = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO ai_analyses (project_id, analysis_json, provider_used, created_at) VALUES (?, ?, ?, ?)",
        (project_id, json.dumps(analysis), provider, now)
    )
    conn.commit()
    conn.close()

def get_latest_ai_analysis(project_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute(
        "SELECT * FROM ai_analyses WHERE project_id = ? ORDER BY id DESC LIMIT 1",
        (project_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["analysis"] = json.loads(d["analysis_json"])
    return d

# Settings
def get_setting(key: str, default: str = "") -> str:
    conn = get_db_connection()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default

def set_setting(key: str, value: str):
    conn = get_db_connection()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
