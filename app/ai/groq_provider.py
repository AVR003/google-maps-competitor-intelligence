import requests
import json
import logging
from typing import List, Dict, Any, Optional
from app.ai.builtin_provider import (
    analyze_repository_builtin,
    generate_ideas_builtin,
    generate_update_builtin
)

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(api_key: str, messages: List[Dict[str, str]], model: str = "llama-3.3-70b-versatile") -> Optional[str]:
    if not api_key:
        return None
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=25)
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.warning(f"Groq API returned status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error calling Groq API: {e}")
        return None

def analyze_repository_groq(posts: List[Dict[str, Any]], client_name: str, api_key: str) -> Dict[str, Any]:
    if not api_key:
        return analyze_repository_builtin(posts, client_name)

    summaries = []
    for p in posts[:25]:
        summaries.append(f"- [{p.get('competitor_name')}] ({p.get('published_date')}): {p.get('post_text')[:180]}")
    posts_text = "\n".join(summaries)

    system_prompt = "You are a senior competitor intelligence analyst. Return your analysis strictly as JSON."
    user_prompt = f"""Analyze competitor posts for '{client_name}':
{posts_text}

JSON Output schema:
{{
  "summary": "...",
  "topic_distribution": [
    {{"topic": "Hair Care Tips", "count": 10, "competitors_using": "3 of 4", "occurrence_pct": 50.0, "competitors_count": 3}}
  ],
  "top_keywords": [{{"keyword": "Balayage", "count": 6}}],
  "cta_distribution": {{"Book Online": 10}},
  "competitor_activity": [{{"competitor": "Name", "total_posts": 4, "primary_focus": "Discounts", "offer_heavy": true}}],
  "gap_analysis": ["..."],
  "recommendations": ["..."],
  "offer_patterns": "...",
  "publishing_patterns": "..."
}}
"""
    raw = call_groq(api_key, [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])
    if raw:
        try:
            return json.loads(raw.strip())
        except Exception as e:
            logger.warning(f"Groq JSON parse error: {e}")

    return analyze_repository_builtin(posts, client_name)

def generate_ideas_groq(
    client_name: str,
    keywords: List[str],
    trends: List[Dict[str, Any]],
    count: int,
    existing_ideas: List[str],
    api_key: str
) -> List[Dict[str, Any]]:
    if not api_key:
        return generate_ideas_builtin(client_name, keywords, trends, count, existing_ideas)

    system_prompt = "You are a Google Maps Marketing Strategist. Return JSON containing a list of ideas."
    user_prompt = f"""Generate {count} unique Google Maps update ideas for '{client_name}'.
Keywords: {', '.join(keywords)}
Avoid previously generated: {json.dumps(existing_ideas[-20:] if existing_ideas else [])}

Return format:
{{
  "ideas": [
    {{
      "topic": "Topic Name",
      "angle": "Angle",
      "idea_summary": "Headline and concept",
      "target_audience": "Audience"
    }}
  ]
}}
"""
    raw = call_groq(api_key, [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])
    if raw:
        try:
            parsed = json.loads(raw.strip())
            ideas = parsed.get("ideas", [])
            if ideas:
                return ideas[:count]
        except Exception as e:
            logger.warning(f"Groq ideas parse error: {e}")

    return generate_ideas_builtin(client_name, keywords, trends, count, existing_ideas)

def generate_update_groq(
    client_name: str,
    topic: str,
    idea_summary: str,
    keywords: List[str],
    api_key: str
) -> Dict[str, Any]:
    if not api_key:
        return generate_update_builtin(client_name, topic, idea_summary, keywords)

    system_prompt = "You are a professional copywriter for Google Business Profiles. Output JSON only."
    user_prompt = f"""Write a full Google Maps post for:
Business: '{client_name}'
Topic: '{topic}'
Idea: '{idea_summary}'
Keywords: {', '.join(keywords)}

Return JSON:
{{
  "topic": "{topic}",
  "full_copy": "post text with emojis and details",
  "relevant_keywords": "keywords",
  "call_to_action": "Book Online",
  "suggested_image_concept": "image description",
  "ai_image_url": "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=900&auto=format&fit=crop&q=80",
  "provider_used": "Groq LLaMA 3.3"
}}
"""
    raw = call_groq(api_key, [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])
    if raw:
        try:
            parsed = json.loads(raw.strip())
            parsed["provider_used"] = "Groq LLaMA 3.3"
            return parsed
        except Exception as e:
            logger.warning(f"Groq update parse error: {e}")

    res = generate_update_builtin(client_name, topic, idea_summary, keywords)
    res["provider_used"] = "Groq (Fallback to Local)"
    return res
