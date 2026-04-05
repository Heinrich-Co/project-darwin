"""
Scale 3: Content Performance Intelligence
Connects with GA4 data from Google Sheets to track which content drives results.
Feeds back into content strategy for self-improvement.

This module reads from the Google Sheets data (synced by Apps Script at 6 AM)
and provides actionable insights for content optimization.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger("analytics.performance")

PERFORMANCE_FILE = Path(__file__).resolve().parent / "performance_data.json"

# KPI benchmarks from Heinrich Co. standards
BENCHMARKS = {
    "blog_views_30d": 1000,
    "engagement_rate": 8.0,
    "reading_time_min": 4.0,
    "social_reach_monthly": 50000,
    "social_engagement": 6.0,
    "leads_monthly": 50,
    "mqls_monthly": 30,
    "sql_conversion": 20.0,
    "cac_max": 5000,
    "pipeline_target": 500000,
}


def _load_data() -> Dict:
    if PERFORMANCE_FILE.exists():
        return json.loads(PERFORMANCE_FILE.read_text(encoding="utf-8"))
    return {"content": {}, "keywords": {}, "weekly_snapshots": []}


def _save_data(data: Dict):
    PERFORMANCE_FILE.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def ingest_ga4_data(pages: List[Dict]) -> Dict:
    """Ingest GA4 page data (from daily email or direct API).
    Each page: {title, path, views, engagement_rate, avg_duration, conversions}
    """
    data = _load_data()
    updated = 0

    for page in pages:
        key = page.get("path", page.get("title", "unknown"))
        existing = data["content"].get(key, {
            "first_seen": datetime.now().isoformat(),
            "history": [],
        })

        existing["title"] = page.get("title", "")
        existing["latest_views"] = page.get("views", 0)
        existing["latest_engagement"] = page.get("engagement_rate", 0)
        existing["latest_duration"] = page.get("avg_duration", 0)
        existing["last_updated"] = datetime.now().isoformat()

        # Keep 30-day history
        existing["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "views": page.get("views", 0),
            "engagement": page.get("engagement_rate", 0),
        })
        existing["history"] = existing["history"][-30:]

        # Calculate performance score (0-100)
        score = calculate_performance_score(page)
        existing["performance_score"] = score

        data["content"][key] = existing
        updated += 1

    _save_data(data)
    return {"status": "ingested", "pages_updated": updated}


def calculate_performance_score(page: Dict) -> int:
    """Calculate a 0-100 performance score for a content page."""
    views = page.get("views", 0)
    engagement = page.get("engagement_rate", 0)
    duration = page.get("avg_duration", 0)
    conversions = page.get("conversions", 0)

    view_score = min(30, (views / BENCHMARKS["blog_views_30d"]) * 30)
    engagement_score = min(30, (engagement / BENCHMARKS["engagement_rate"]) * 30)
    duration_score = min(20, (duration / (BENCHMARKS["reading_time_min"] * 60)) * 20)
    conversion_score = min(20, conversions * 10)

    return min(100, round(view_score + engagement_score + duration_score + conversion_score))


def get_content_recommendations() -> Dict:
    """AI-like recommendations based on performance data."""
    data = _load_data()
    recommendations = []

    for key, content in data["content"].items():
        score = content.get("performance_score", 0)
        views = content.get("latest_views", 0)
        engagement = content.get("latest_engagement", 0)
        title = content.get("title", key)

        if score < 20:
            recommendations.append({
                "content": title,
                "score": score,
                "action": "LOW PERFORMANCE — Consider rewriting with stronger hook and updated data.",
                "priority": "HIGH",
            })
        elif score < 50 and views > 0:
            recommendations.append({
                "content": title,
                "score": score,
                "action": "MODERATE — Has traffic but low engagement. Add FAQ section, update internal links.",
                "priority": "MEDIUM",
            })
        elif engagement > 50 and views < 100:
            recommendations.append({
                "content": title,
                "score": score,
                "action": "HIGH ENGAGEMENT but low visibility. Promote on social, add to newsletter.",
                "priority": "HIGH",
            })
        elif score > 70:
            recommendations.append({
                "content": title,
                "score": score,
                "action": "TOP PERFORMER — Create more content around this topic. Repurpose into social + carousel.",
                "priority": "OPPORTUNITY",
            })

    recommendations.sort(key=lambda x: x["score"])
    return {
        "generated_at": datetime.now().isoformat(),
        "total_content": len(data["content"]),
        "recommendations": recommendations,
    }


def get_keyword_performance(keyword: str) -> Dict:
    """Get performance data for content associated with a keyword."""
    data = _load_data()

    matching = []
    for key, content in data["content"].items():
        title = content.get("title", "").lower()
        if keyword.lower() in title or keyword.lower() in key.lower():
            matching.append({
                "title": content.get("title"),
                "views": content.get("latest_views", 0),
                "engagement": content.get("latest_engagement", 0),
                "score": content.get("performance_score", 0),
            })

    return {
        "keyword": keyword,
        "content_count": len(matching),
        "content": matching,
        "avg_score": round(sum(c["score"] for c in matching) / len(matching), 1) if matching else 0,
    }


def get_weekly_snapshot() -> Dict:
    """Generate weekly performance snapshot."""
    data = _load_data()

    total_views = sum(c.get("latest_views", 0) for c in data["content"].values())
    avg_engagement = 0
    if data["content"]:
        avg_engagement = sum(c.get("latest_engagement", 0) for c in data["content"].values()) / len(data["content"])

    top = max(data["content"].values(), key=lambda c: c.get("performance_score", 0), default={})

    snapshot = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_content": len(data["content"]),
        "total_views": total_views,
        "avg_engagement": round(avg_engagement, 1),
        "top_performer": top.get("title", "N/A"),
        "top_score": top.get("performance_score", 0),
        "benchmarks_met": {
            "views": total_views >= BENCHMARKS["blog_views_30d"],
            "engagement": avg_engagement >= BENCHMARKS["engagement_rate"],
        },
    }

    data["weekly_snapshots"].append(snapshot)
    data["weekly_snapshots"] = data["weekly_snapshots"][-52:]  # Keep 1 year
    _save_data(data)

    return snapshot
