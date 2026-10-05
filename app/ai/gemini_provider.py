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

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def call_gemini(api_key: str, prompt: str, system_instruction: str = "") -> Optional[str]:
    if not api_key:
        return None
    url = f"{GEMINI_API_URL}?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    if system_instruction:
        payload["systemInstruction"] = {
            "parts": [{"text": system_instruction}]
        }

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        else:
            logger.warning(f"Gemini API returned status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return None

def analyze_repository_gemini(
    posts: List[Dict[str, Any]],
    client_name: str,
    api_key: str
) -> Dict[str, Any]:
    if not api_key:
        return analyze_repository_builtin(posts, client_name)

    # Prepare summarized competitor posts
    summaries = []
    for p in posts[:25]:
        summaries.append(f"- [{p.get('competitor_name')}] ({p.get('published_date')}): {p.get('post_text')[:180]}")

    posts_text = "\n".join(summaries)
    prompt = f"""You are an expert Google Business Profile strategist.
Analyze the following Google Maps competitor posts for a local business '{client_name}':

{posts_text}

Provide an in-depth analysis returned strictly in valid JSON format with this exact schema:
{{
  "summary": "Brief executive summary of competitor activities",
  "topic_distribution": [
    {{"topic": "Name", "count": 10, "competitors_using": "3 of 4", "occurrence_pct": 45.0, "competitors_count": 3}}
  ],
  "top_keywords": [
    {{"keyword": "Keyword", "count": 8}}
  ],
  "cta_distribution": {{"Book Online": 12, "Call Now": 8}},
  "competitor_activity": [
    {{"competitor": "Name", "total_posts": 5, "primary_focus": "Discounts", "offer_heavy": true}}
  ],
  "gap_analysis": [
    "Identified gap 1...",
    "Identified gap 2..."
  ],
  "recommendations": [
    "Strategic recommendation 1...",
    "Strategic recommendation 2..."
  ],
  "offer_patterns": "Summary of offers used by competitors",
  "publishing_patterns": "Analysis of posting frequency"
}}
Return ONLY raw JSON, with no markdown code blocks.
"""
    raw_response = call_gemini(api_key, prompt)
    if raw_response:
        try:
            clean = raw_response.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            return json.loads(clean.strip())
        except Exception as e:
            logger.warning(f"Failed to parse Gemini response as JSON: {e}. Falling back to built-in.")

    return analyze_repository_builtin(posts, client_name)

def generate_ideas_gemini(
    client_name: str,
    keywords: List[str],
    trends: List[Dict[str, Any]],
    count: int,
    existing_ideas: List[str],
    api_key: str
) -> List[Dict[str, Any]]:
    if not api_key:
        return generate_ideas_builtin(client_name, keywords, trends, count, existing_ideas)

    prompt = f"""You are a content strategist for Google Maps / Google Business Profile.
Business: '{client_name}'
Target Keywords: {', '.join(keywords)}
Competitor Topic Trends: {json.dumps(trends[:4])}
Previously Generated Ideas (DO NOT REPEAT OR DUPLICATE THESE):
{json.dumps(existing_ideas[-20:] if existing_ideas else [])}

Generate exactly {count} distinct, creative, high-converting Google Maps Update Post IDEAS that stand out against competitors and address local search intent.

Return strictly a JSON array with exactly {count} items:
[
  {{
    "topic": "Topic Name (e.g. Hair Care Tips, Festival Offer, Before/After)",
    "angle": "Strategic Angle",
    "idea_summary": "Catchy headline & update concept",
    "target_audience": "Specific audience target"
  }}
]
Return ONLY raw JSON, with no markdown wrapping.
"""
    raw_response = call_gemini(api_key, prompt)
    if raw_response:
        try:
            clean = raw_response.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            parsed = json.loads(clean.strip())
            if isinstance(parsed, list) and len(parsed) > 0:
                return parsed[:count]
        except Exception as e:
            logger.warning(f"Failed to parse Gemini ideas: {e}. Falling back to built-in.")

    return generate_ideas_builtin(client_name, keywords, trends, count, existing_ideas)

def generate_update_gemini(
    client_name: str,
    topic: str,
    idea_summary: str,
    keywords: List[str],
    api_key: str
) -> Dict[str, Any]:
    if not api_key:
        return generate_update_builtin(client_name, topic, idea_summary, keywords)

    prompt = f"""Generate a complete, ready-to-publish Google Maps Update Post for:
Business: '{client_name}'
Topic: '{topic}'
Idea / Angle: '{idea_summary}'
Relevant Keywords: {', '.join(keywords)}

Return strictly JSON with this exact structure:
{{
  "topic": "{topic}",
  "full_copy": "Engaging complete Google Maps update text with emojis, benefits, location info, and call to action",
  "relevant_keywords": "comma separated local keywords",
  "call_to_action": "Book Online | Call Now | Learn More | Get Offer",
  "suggested_image_concept": "Detailed description of the ideal photo to attach (lighting, subject, styling)",
  "ai_image_url": "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=900&auto=format&fit=crop&q=80",
  "provider_used": "Google Gemini 2.5 Flash"
}}
Return ONLY raw JSON.
"""
    raw_response = call_gemini(api_key, prompt)
    if raw_response:
        try:
            clean = raw_response.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            parsed = json.loads(clean.strip())
            parsed["provider_used"] = "Google Gemini 2.5 Flash"
            return parsed
        except Exception as e:
            logger.warning(f"Failed to parse Gemini update: {e}. Falling back to built-in.")

    res = generate_update_builtin(client_name, topic, idea_summary, keywords)
    res["provider_used"] = "Google Gemini (Fallback to Local)"
    return res
