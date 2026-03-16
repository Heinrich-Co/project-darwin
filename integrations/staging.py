"""
Staging System for Project Darwin.
Content lands here first for Camila's review.
Only after approval does it move to Notion.

Flow: Skills generate → Staging (Claude Project) → Camila approves → Notion (team)
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Staging directory — all generated content saved here as JSON files
STAGING_DIR = Path(__file__).resolve().parent.parent / "staging"
STAGING_DIR.mkdir(exist_ok=True)


def _save_to_staging(content_type: str, keyword: str, data: Dict) -> str:
    """Save content to staging directory. Returns the staging file path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_keyword = keyword.lower().replace(" ", "_")[:30]
    filename = f"{content_type}_{safe_keyword}_{timestamp}.json"
    filepath = STAGING_DIR / filename

    staging_entry = {
        "id": f"{content_type}_{safe_keyword}_{timestamp}",
        "type": content_type,
        "keyword": keyword,
        "status": "pending_review",  # pending_review → approved → pushed_to_notion → needs_revision
        "created_at": datetime.now().isoformat(),
        "reviewed_at": None,
        "approved_at": None,
        "pushed_to_notion_at": None,
        "revision_feedback": None,
        "data": data,
    }

    filepath.write_text(json.dumps(staging_entry, indent=2, default=str), encoding="utf-8")
    logger.info("Staged %s for '%s' → %s", content_type, keyword, filename)
    return str(filepath)


def stage_brief(brief: Dict) -> str:
    return _save_to_staging("brief", brief.get("keyword", "unknown"), brief)


def stage_blog(blog: Dict) -> str:
    keyword = blog.get("slug", blog.get("title", "unknown")).replace("-", " ")
    return _save_to_staging("blog", keyword, blog)


def stage_social(social: Dict) -> str:
    return _save_to_staging("social", social.get("keyword", "unknown"), social)


def stage_designs(designs: Dict) -> str:
    return _save_to_staging("designs", designs.get("keyword", "unknown"), designs)


def stage_linkedin(post: Dict) -> str:
    return _save_to_staging("linkedin", post.get("pillar", "unknown"), post)


# ------------------------------------------------------------------
# Review & Approval
# ------------------------------------------------------------------

def list_pending() -> List[Dict]:
    """List all content waiting for Camila's review."""
    pending = []
    for f in sorted(STAGING_DIR.glob("*.json"), key=os.path.getmtime, reverse=True):
        try:
            entry = json.loads(f.read_text(encoding="utf-8"))
            if entry.get("status") == "pending_review":
                pending.append({
                    "id": entry["id"],
                    "type": entry["type"],
                    "keyword": entry["keyword"],
                    "created_at": entry["created_at"],
                    "file": f.name,
                })
        except Exception:
            continue
    return pending


def list_all(status_filter: str = None) -> List[Dict]:
    """List all staged content, optionally filtered by status."""
    items = []
    for f in sorted(STAGING_DIR.glob("*.json"), key=os.path.getmtime, reverse=True):
        try:
            entry = json.loads(f.read_text(encoding="utf-8"))
            if status_filter and entry.get("status") != status_filter:
                continue
            items.append({
                "id": entry["id"],
                "type": entry["type"],
                "keyword": entry["keyword"],
                "status": entry["status"],
                "created_at": entry["created_at"],
                "file": f.name,
            })
        except Exception:
            continue
    return items


def get_staged_content(file_name: str) -> Optional[Dict]:
    """Get full content of a staged item for review."""
    filepath = STAGING_DIR / file_name
    if not filepath.exists():
        return None
    return json.loads(filepath.read_text(encoding="utf-8"))


def approve_content(file_name: str) -> Optional[Dict]:
    """Mark content as approved. Ready to push to Notion."""
    filepath = STAGING_DIR / file_name
    if not filepath.exists():
        return None

    entry = json.loads(filepath.read_text(encoding="utf-8"))
    entry["status"] = "approved"
    entry["approved_at"] = datetime.now().isoformat()
    filepath.write_text(json.dumps(entry, indent=2, default=str), encoding="utf-8")
    return entry


def request_revision(file_name: str, feedback: str) -> Optional[Dict]:
    """Mark content as needing revision with feedback."""
    filepath = STAGING_DIR / file_name
    if not filepath.exists():
        return None

    entry = json.loads(filepath.read_text(encoding="utf-8"))
    entry["status"] = "needs_revision"
    entry["revision_feedback"] = feedback
    entry["reviewed_at"] = datetime.now().isoformat()
    filepath.write_text(json.dumps(entry, indent=2, default=str), encoding="utf-8")
    return entry


def mark_pushed_to_notion(file_name: str) -> Optional[Dict]:
    """Mark content as pushed to Notion."""
    filepath = STAGING_DIR / file_name
    if not filepath.exists():
        return None

    entry = json.loads(filepath.read_text(encoding="utf-8"))
    entry["status"] = "pushed_to_notion"
    entry["pushed_to_notion_at"] = datetime.now().isoformat()
    filepath.write_text(json.dumps(entry, indent=2, default=str), encoding="utf-8")
    return entry


def get_weekly_summary() -> Dict:
    """Generate weekly summary for notification."""
    all_items = list_all()
    pending = [i for i in all_items if i["status"] == "pending_review"]
    approved = [i for i in all_items if i["status"] == "approved"]
    revised = [i for i in all_items if i["status"] == "needs_revision"]
    pushed = [i for i in all_items if i["status"] == "pushed_to_notion"]

    return {
        "total_items": len(all_items),
        "pending_review": len(pending),
        "approved": len(approved),
        "needs_revision": len(revised),
        "pushed_to_notion": len(pushed),
        "pending_items": pending,
        "generated_at": datetime.now().isoformat(),
        "message": f"You have {len(pending)} items waiting for review.",
    }
