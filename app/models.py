from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectCreate(BaseModel):
    name: str = Field(..., example="ABC Salon - Kharghar Intelligence")
    our_profile_name: str = Field(..., example="ABC Salon, Kharghar")
    our_profile_url: Optional[str] = Field(default="", example="https://maps.google.com/?cid=9988776655")
    keywords: List[str] = Field(default=[], example=["salon in Kharghar", "keratin treatment Kharghar"])

class ProjectUpdate(BaseModel):
    name: str
    our_profile_name: str
    our_profile_url: Optional[str] = ""
    keywords: List[str] = []

class CompetitorCreate(BaseModel):
    name: str = Field(..., example="Enrich Salon - Kharghar")
    profile_url: str = Field(..., example="https://maps.google.com/?cid=1234567890")

class CompetitorUpdate(BaseModel):
    name: str
    profile_url: str

class ScrapeRequest(BaseModel):
    competitor_ids: Optional[List[int]] = None
    simulate_captcha: bool = False

class IdeaGenerateRequest(BaseModel):
    count: int = Field(default=3, ge=1, le=100, example=3)

class FullUpdateGenerateRequest(BaseModel):
    topic: str = Field(..., example="Hair Care Tips")
    idea_summary: str = Field(..., example="Monsoon scalp detox and hard water rescue")

class SettingsUpdate(BaseModel):
    active_ai_provider: str = Field(default="builtin", example="builtin") # builtin, gemini, groq
    gemini_api_key: Optional[str] = ""
    groq_api_key: Optional[str] = ""
