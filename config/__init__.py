"""
Configuration management for Project Darwin.
Loads environment variables and provides defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))

    # Claude API
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL = "claude-sonnet-4-20250514"
    CLAUDE_MAX_TOKENS = 4096

    # Notion
    NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
    NOTION_BRIEF_DB_ID = os.getenv("NOTION_BRIEF_DB_ID", "")
    NOTION_BLOG_DB_ID = os.getenv("NOTION_BLOG_DB_ID", "")
    NOTION_SOCIAL_DB_ID = os.getenv("NOTION_SOCIAL_DB_ID", "")
    NOTION_LEADS_DB_ID = os.getenv("NOTION_LEADS_DB_ID", "")
    NOTION_METRICS_DB_ID = os.getenv("NOTION_METRICS_DB_ID", "")

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

    # Zapier
    ZAPIER_WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL", "")


config = Config()
