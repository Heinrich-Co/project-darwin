"""
Notion Integration for Project Darwin.
Syncs generated content (briefs, blogs, social posts, leads, metrics)
to Notion databases for team collaboration.

Setup:
1. Go to https://www.notion.so/my-integrations
2. Create integration → get NOTION_TOKEN
3. Share each database with the integration
4. Copy each database ID into .env
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional, List

import requests

from config import config

logger = logging.getLogger(__name__)

NOTION_API = "https://api.notion.so/v1"
NOTION_VERSION = "2022-06-28"


def _headers() -> Dict:
    """Return Notion API headers."""
    return {
        "Authorization": f"Bearer {config.NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def _is_configured() -> bool:
    """Check if Notion token is set."""
    return bool(config.NOTION_TOKEN and not config.NOTION_TOKEN.startswith("ntn_xxx"))


def _create_page(database_id: str, properties: Dict, children: List = None) -> Optional[Dict]:
    """Create a page in a Notion database."""
    if not _is_configured():
        logger.info("Notion not configured — skipping sync.")
        return None

    if not database_id:
        logger.warning("No database ID provided — skipping.")
        return None

    payload = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    if children:
        payload["children"] = children

    try:
        resp = requests.post(f"{NOTION_API}/pages", headers=_headers(), json=payload, timeout=30)
        if resp.status_code == 200:
            logger.info("Notion page created: %s", resp.json().get("id", ""))
            return resp.json()
        else:
            logger.error("Notion error %s: %s", resp.status_code, resp.text[:200])
            return None
    except Exception as e:
        logger.error("Notion request failed: %s", e)
        return None


# ------------------------------------------------------------------
# Sync functions for each content type
# ------------------------------------------------------------------

def sync_brief(brief: Dict) -> Optional[Dict]:
    """Sync a strategic brief to Notion."""
    db_id = config.NOTION_BRIEF_DB_ID
    if not db_id:
        return None

    keyword = brief.get("keyword", "Unknown")
    brief_id = brief.get("brief_id", "")
    status = brief.get("status", "draft")
    angles = brief.get("content_angles", [])
    angle_names = ", ".join(a.get("angle", "") for a in angles)

    properties = {
        "Name": {"title": [{"text": {"content": f"Brief: {keyword}"}}]},
        "Brief ID": {"rich_text": [{"text": {"content": brief_id}}]},
        "Keyword": {"rich_text": [{"text": {"content": keyword}}]},
        "Status": {"select": {"name": status}},
        "Angles": {"rich_text": [{"text": {"content": angle_names[:2000]}}]},
        "Created": {"date": {"start": brief.get("created_at", datetime.now().isoformat())}},
    }

    return _create_page(db_id, properties)


def sync_blog(blog: Dict) -> Optional[Dict]:
    """Sync a blog post to Notion."""
    db_id = config.NOTION_BLOG_DB_ID
    if not db_id:
        return None

    title = blog.get("title", "Untitled")
    word_count = blog.get("word_count", 0)
    status = blog.get("status", "draft")
    slug = blog.get("slug", "")

    properties = {
        "Name": {"title": [{"text": {"content": title}}]},
        "Slug": {"rich_text": [{"text": {"content": slug}}]},
        "Word Count": {"number": word_count},
        "Status": {"select": {"name": status}},
        "Reading Time": {"rich_text": [{"text": {"content": blog.get("reading_time", "")}}]},
        "Created": {"date": {"start": blog.get("created_at", datetime.now().isoformat())}},
    }

    # Add blog content as page body
    intro = blog.get("introduction", "")
    children = []
    if intro:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": intro[:2000]}}]},
        })
    for section in blog.get("sections", []):
        children.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": section.get("heading", "")}}]},
        })
        content = section.get("content", "")
        # Notion blocks have 2000 char limit
        for i in range(0, len(content), 2000):
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": content[i:i+2000]}}]},
            })

    return _create_page(db_id, properties, children[:100])  # Notion limit: 100 blocks


def sync_social_posts(social: Dict) -> Optional[Dict]:
    """Sync social posts to Notion."""
    db_id = config.NOTION_SOCIAL_DB_ID
    if not db_id:
        return None

    platform = social.get("platform", "unknown")
    keyword = social.get("keyword", "")
    posts = social.get("posts", [])

    results = []
    for i, post in enumerate(posts):
        post_type = post.get("type", "static")
        copy_text = post.get("copy", "")[:2000]

        properties = {
            "Name": {"title": [{"text": {"content": f"{platform.title()} - {post_type} - {keyword}"}}]},
            "Platform": {"select": {"name": platform}},
            "Type": {"select": {"name": post_type}},
            "Keyword": {"rich_text": [{"text": {"content": keyword}}]},
            "Copy": {"rich_text": [{"text": {"content": copy_text}}]},
            "Status": {"select": {"name": "Draft"}},
            "Created": {"date": {"start": datetime.now().isoformat()}},
        }

        result = _create_page(db_id, properties)
        if result:
            results.append(result.get("id"))

    return {"synced_posts": len(results), "ids": results}


def sync_leads(qualification: Dict) -> Optional[Dict]:
    """Sync qualified leads to Notion."""
    db_id = config.NOTION_LEADS_DB_ID
    if not db_id:
        return None

    results = []
    for lead in qualification.get("top_10", []):
        name = lead.get("name", "Unknown")
        company = lead.get("company", "")
        score = lead.get("combined_score", 0)
        stage = lead.get("stage", "Awareness")

        properties = {
            "Name": {"title": [{"text": {"content": f"{name} - {company}"}}]},
            "Company": {"rich_text": [{"text": {"content": company}}]},
            "Score": {"number": score},
            "Stage": {"select": {"name": stage}},
            "Source": {"rich_text": [{"text": {"content": lead.get("source", "")}}]},
            "Actions": {"rich_text": [{"text": {"content": ", ".join(lead.get("recommended_actions", []))[:2000]}}]},
            "Qualified": {"date": {"start": lead.get("qualified_at", datetime.now().isoformat())}},
        }

        result = _create_page(db_id, properties)
        if result:
            results.append(result.get("id"))

    return {"synced_leads": len(results), "ids": results}


def sync_analytics(report: Dict) -> Optional[Dict]:
    """Sync analytics report to Notion."""
    db_id = config.NOTION_METRICS_DB_ID
    if not db_id:
        return None

    period = report.get("report_type", "daily")
    content = report.get("content_performance", {})
    signals = report.get("buying_signals", {})
    leads = report.get("lead_intelligence", {})

    properties = {
        "Name": {"title": [{"text": {"content": f"Report - {period} - {datetime.now().strftime('%Y-%m-%d')}"}}]},
        "Period": {"select": {"name": period}},
        "Pages Monitored": {"number": content.get("pages_monitored", 0)},
        "Total Views": {"number": content.get("total_views_24h", 0)},
        "Total Signals": {"number": signals.get("total_signals", 0)},
        "Hot Leads": {"number": leads.get("hot_leads_8plus", 0)},
        "Date": {"date": {"start": datetime.now().isoformat()}},
    }

    # Add action items as page body
    children = []
    for action in report.get("action_items", []):
        children.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": f"[{action['priority']}] {action['action']} — {action.get('owner', '')}"}}],
                "checked": False,
            },
        })

    return _create_page(db_id, properties, children)


def check_connection() -> Dict:
    """Test Notion connection and return status."""
    if not _is_configured():
        return {"connected": False, "reason": "NOTION_TOKEN not set in .env"}

    try:
        resp = requests.get(f"{NOTION_API}/users/me", headers=_headers(), timeout=10)
        if resp.status_code == 200:
            user = resp.json()
            return {
                "connected": True,
                "bot_name": user.get("name", "Unknown"),
                "bot_id": user.get("id", ""),
                "databases": {
                    "briefs": bool(config.NOTION_BRIEF_DB_ID),
                    "blogs": bool(config.NOTION_BLOG_DB_ID),
                    "social": bool(config.NOTION_SOCIAL_DB_ID),
                    "leads": bool(config.NOTION_LEADS_DB_ID),
                    "metrics": bool(config.NOTION_METRICS_DB_ID),
                },
            }
        else:
            return {"connected": False, "reason": f"API error {resp.status_code}: {resp.text[:100]}"}
    except Exception as e:
        return {"connected": False, "reason": str(e)}
