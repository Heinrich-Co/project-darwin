"""
Scale 2: Revenue Attribution Engine
Tracks the full journey: Keyword → Content → Lead → Deal → Revenue.
Proves ROI per keyword and content piece.

Usage:
  attribution.record_content(keyword, content_type, content_id)
  attribution.record_lead(content_id, lead_name, lead_source)
  attribution.record_deal(lead_name, deal_value, status)
  attribution.get_keyword_roi(keyword)
  attribution.get_full_attribution_report()
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger("analytics.attribution")

ATTRIBUTION_FILE = Path(__file__).resolve().parent / "attribution_data.json"


def _load_data() -> Dict:
    if ATTRIBUTION_FILE.exists():
        return json.loads(ATTRIBUTION_FILE.read_text(encoding="utf-8"))
    return {
        "content_map": {},    # content_id → {keyword, type, created_at, views, engagement}
        "lead_map": {},       # lead_name → {content_id, keyword, source, score, created_at}
        "deal_map": {},       # deal_id → {lead_name, keyword, value, status, created_at}
        "keyword_stats": {},  # keyword → {content_count, leads, deals, revenue, investment}
    }


def _save_data(data: Dict):
    ATTRIBUTION_FILE.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


# ------------------------------------------------------------------
# Record Events
# ------------------------------------------------------------------

def record_content(keyword: str, content_type: str, content_id: str,
                   title: str = "", views: int = 0, engagement: float = 0.0) -> Dict:
    """Record content creation and attribute to keyword."""
    data = _load_data()

    data["content_map"][content_id] = {
        "keyword": keyword,
        "type": content_type,
        "title": title,
        "views": views,
        "engagement": engagement,
        "created_at": datetime.now().isoformat(),
    }

    # Update keyword stats
    if keyword not in data["keyword_stats"]:
        data["keyword_stats"][keyword] = {
            "content_count": 0, "leads": 0, "deals": 0,
            "revenue": 0, "investment": 0, "first_content": datetime.now().isoformat(),
        }
    data["keyword_stats"][keyword]["content_count"] += 1

    _save_data(data)
    return {"status": "recorded", "content_id": content_id, "keyword": keyword}


def record_lead(lead_name: str, content_id: str, source: str = "organic",
                score: int = 5, company: str = "") -> Dict:
    """Record lead and attribute to content → keyword."""
    data = _load_data()

    content = data["content_map"].get(content_id, {})
    keyword = content.get("keyword", "unknown")

    data["lead_map"][lead_name] = {
        "content_id": content_id,
        "keyword": keyword,
        "source": source,
        "score": score,
        "company": company,
        "created_at": datetime.now().isoformat(),
    }

    if keyword in data["keyword_stats"]:
        data["keyword_stats"][keyword]["leads"] += 1

    _save_data(data)
    return {"status": "recorded", "lead": lead_name, "attributed_keyword": keyword}


def record_deal(deal_id: str, lead_name: str, value: float,
                status: str = "proposal") -> Dict:
    """Record deal and attribute to lead → content → keyword."""
    data = _load_data()

    lead = data["lead_map"].get(lead_name, {})
    keyword = lead.get("keyword", "unknown")

    data["deal_map"][deal_id] = {
        "lead_name": lead_name,
        "keyword": keyword,
        "value": value,
        "status": status,
        "created_at": datetime.now().isoformat(),
    }

    if keyword in data["keyword_stats"]:
        data["keyword_stats"][keyword]["deals"] += 1
        if status in ("won", "closed"):
            data["keyword_stats"][keyword]["revenue"] += value

    _save_data(data)
    return {"status": "recorded", "deal": deal_id, "value": value, "keyword": keyword}


def update_content_metrics(content_id: str, views: int = 0,
                           engagement: float = 0.0) -> Dict:
    """Update content performance metrics (from GA4 data)."""
    data = _load_data()
    if content_id in data["content_map"]:
        data["content_map"][content_id]["views"] = views
        data["content_map"][content_id]["engagement"] = engagement
        data["content_map"][content_id]["last_updated"] = datetime.now().isoformat()
        _save_data(data)
    return {"status": "updated", "content_id": content_id}


# ------------------------------------------------------------------
# Reports
# ------------------------------------------------------------------

def get_keyword_roi(keyword: str) -> Dict:
    """Get ROI for a specific keyword."""
    data = _load_data()
    stats = data["keyword_stats"].get(keyword)
    if not stats:
        return {"keyword": keyword, "status": "no_data"}

    # Calculate pipeline value from deals
    pipeline = sum(
        d["value"] for d in data["deal_map"].values()
        if d.get("keyword") == keyword
    )
    won = sum(
        d["value"] for d in data["deal_map"].values()
        if d.get("keyword") == keyword and d.get("status") in ("won", "closed")
    )

    # Content performance
    content_views = sum(
        c["views"] for c in data["content_map"].values()
        if c.get("keyword") == keyword
    )

    investment = stats.get("investment", 0)
    roi = ((won - investment) / investment * 100) if investment > 0 else 0

    return {
        "keyword": keyword,
        "content_pieces": stats["content_count"],
        "total_views": content_views,
        "leads_generated": stats["leads"],
        "deals_created": stats["deals"],
        "pipeline_value": pipeline,
        "revenue_won": won,
        "investment": investment,
        "roi_percent": round(roi, 1),
        "cost_per_lead": round(investment / stats["leads"], 2) if stats["leads"] > 0 else 0,
    }


def get_full_attribution_report() -> Dict:
    """Complete attribution report across all keywords."""
    data = _load_data()

    keyword_reports = []
    for keyword in data["keyword_stats"]:
        report = get_keyword_roi(keyword)
        keyword_reports.append(report)

    # Sort by pipeline value (highest first)
    keyword_reports.sort(key=lambda x: x.get("pipeline_value", 0), reverse=True)

    # Totals
    total_content = sum(r["content_pieces"] for r in keyword_reports)
    total_views = sum(r["total_views"] for r in keyword_reports)
    total_leads = sum(r["leads_generated"] for r in keyword_reports)
    total_pipeline = sum(r["pipeline_value"] for r in keyword_reports)
    total_revenue = sum(r["revenue_won"] for r in keyword_reports)

    return {
        "generated_at": datetime.now().isoformat(),
        "totals": {
            "keywords_active": len(keyword_reports),
            "content_pieces": total_content,
            "total_views": total_views,
            "leads_generated": total_leads,
            "pipeline_value": total_pipeline,
            "revenue_won": total_revenue,
        },
        "by_keyword": keyword_reports,
        "top_performing_keyword": keyword_reports[0]["keyword"] if keyword_reports else None,
        "top_pipeline_keyword": keyword_reports[0]["keyword"] if keyword_reports else None,
    }


def get_content_journey(lead_name: str) -> Dict:
    """Trace a lead's full journey: which keyword → content → actions → deal."""
    data = _load_data()

    lead = data["lead_map"].get(lead_name)
    if not lead:
        return {"lead": lead_name, "status": "not_found"}

    content = data["content_map"].get(lead.get("content_id", ""), {})
    deals = [d for d in data["deal_map"].values() if d.get("lead_name") == lead_name]

    return {
        "lead_name": lead_name,
        "company": lead.get("company", ""),
        "journey": {
            "keyword": lead.get("keyword"),
            "content_type": content.get("type"),
            "content_title": content.get("title"),
            "content_views": content.get("views", 0),
            "lead_source": lead.get("source"),
            "lead_score": lead.get("score"),
            "lead_created": lead.get("created_at"),
            "deals": [{
                "value": d["value"],
                "status": d["status"],
                "created": d["created_at"],
            } for d in deals],
        },
    }
