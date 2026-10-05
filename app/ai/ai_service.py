import os
import uuid
from typing import List, Dict, Any, Optional
from app.database import (
    get_setting,
    get_posts,
    get_generated_ideas,
    save_generated_ideas,
    save_generated_update,
    save_ai_analysis,
    get_latest_ai_analysis
)
from app.ai.builtin_provider import (
    analyze_repository_builtin,
    generate_ideas_builtin,
    generate_update_builtin
)
from app.ai.gemini_provider import (
    analyze_repository_gemini,
    generate_ideas_gemini,
    generate_update_gemini
)
from app.ai.groq_provider import (
    analyze_repository_groq,
    generate_ideas_groq,
    generate_update_groq
)

class AIService:
    @staticmethod
    def get_active_provider() -> str:
        prov = get_setting("active_ai_provider", "builtin")
        return prov

    @staticmethod
    def get_api_key(provider: str) -> str:
        if provider == "gemini":
            return get_setting("gemini_api_key") or os.environ.get("GEMINI_API_KEY", "")
        elif provider == "groq":
            return get_setting("groq_api_key") or os.environ.get("GROQ_API_KEY", "")
        return ""

    @classmethod
    def analyze_repository(cls, project_id: int, client_name: str, force_refresh: bool = False) -> Dict[str, Any]:
        # If cache exists and not force_refresh, check latest
        if not force_refresh:
            cached = get_latest_ai_analysis(project_id)
            if cached:
                return {
                    "source": "cached",
                    "provider": cached.get("provider_used"),
                    "created_at": cached.get("created_at"),
                    "analysis": cached.get("analysis")
                }

        posts = get_posts(project_id)
        provider = cls.get_active_provider()
        api_key = cls.get_api_key(provider)

        analysis = None
        used_provider = provider

        if provider == "gemini" and api_key:
            analysis = analyze_repository_gemini(posts, client_name, api_key)
            used_provider = "Google Gemini"
        elif provider == "groq" and api_key:
            analysis = analyze_repository_groq(posts, client_name, api_key)
            used_provider = "Groq LLaMA"
        else:
            analysis = analyze_repository_builtin(posts, client_name)
            used_provider = "Built-in Intelligent Engine"

        # Save to database cache
        save_ai_analysis(project_id, analysis, used_provider)

        return {
            "source": "fresh",
            "provider": used_provider,
            "analysis": analysis
        }

    @classmethod
    def generate_ideas(
        cls,
        project_id: int,
        client_name: str,
        keywords: List[str],
        count: int = 3
    ) -> List[Dict[str, Any]]:
        # Fetch previous generated ideas to guarantee DUPLICATE PREVENTION (Requirement 16)
        past_records = get_generated_ideas(project_id)
        existing_ideas = [r["idea_summary"] for r in past_records]

        # Get latest trends from repository
        cached_analysis = get_latest_ai_analysis(project_id)
        trends = []
        if cached_analysis and "analysis" in cached_analysis:
            trends = cached_analysis["analysis"].get("topic_distribution", [])

        provider = cls.get_active_provider()
        api_key = cls.get_api_key(provider)

        ideas = []
        if provider == "gemini" and api_key:
            ideas = generate_ideas_gemini(client_name, keywords, trends, count, existing_ideas, api_key)
        elif provider == "groq" and api_key:
            ideas = generate_ideas_groq(client_name, keywords, trends, count, existing_ideas, api_key)
        else:
            ideas = generate_ideas_builtin(client_name, keywords, trends, count, existing_ideas)

        # Save new ideas with unique batch ID
        batch_id = str(uuid.uuid4())[:8]
        save_generated_ideas(project_id, ideas, batch_id)

        return ideas

    @classmethod
    def generate_full_update(
        cls,
        project_id: int,
        client_name: str,
        topic: str,
        idea_summary: str,
        keywords: List[str]
    ) -> Dict[str, Any]:
        provider = cls.get_active_provider()
        api_key = cls.get_api_key(provider)

        update_post = None
        if provider == "gemini" and api_key:
            update_post = generate_update_gemini(client_name, topic, idea_summary, keywords, api_key)
        elif provider == "groq" and api_key:
            update_post = generate_update_groq(client_name, topic, idea_summary, keywords, api_key)
        else:
            update_post = generate_update_builtin(client_name, topic, idea_summary, keywords)

        # Save generated update
        save_generated_update(project_id, update_post)
        return update_post
