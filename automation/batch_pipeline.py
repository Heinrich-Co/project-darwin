"""
Scale 1: Automated Batch Pipeline
Processes multiple keywords on a schedule without manual triggering.
Integrates with n8n or runs as Railway cron job.

Usage:
  python -m automation.batch_pipeline          # Process next 5 keywords
  python -m automation.batch_pipeline --all    # Process all pending keywords
  Called by: n8n webhook, Railway cron, or /api/automation/run endpoint
"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from handlers import handler
from integrations.staging import list_all, get_weekly_summary

logger = logging.getLogger("automation.batch")

# All 41 Snoika keywords with priority
SNOIKA_KEYWORDS = {
    "priority": [
        {"keyword": "consulting services it", "volume": 50000, "yoy": "900%"},
        {"keyword": "bpo services", "volume": 50000, "yoy": "900%"},
        {"keyword": "business process outsourcing services", "volume": 50000, "yoy": "900%"},
        {"keyword": "bpo it services", "volume": 50000, "yoy": "900%"},
        {"keyword": "best ai consulting firms", "volume": 500, "yoy": "900%"},
        {"keyword": "healthcare ai consulting", "volume": 500, "yoy": "900%"},
        {"keyword": "top ai consulting companies", "volume": 500, "yoy": "900%"},
    ],
    "standard": [
        {"keyword": "business consulting services", "volume": 50000, "yoy": "0%"},
        {"keyword": "business consulting firms", "volume": 50000, "yoy": "0%"},
        {"keyword": "tech consulting firms", "volume": 50000, "yoy": "0%"},
        {"keyword": "technology consulting firms", "volume": 50000, "yoy": "0%"},
        {"keyword": "sales consulting", "volume": 50000, "yoy": "0%"},
        {"keyword": "it consulting firms", "volume": 50000, "yoy": "0%"},
        {"keyword": "tech consulting companies", "volume": 50000, "yoy": "0%"},
        {"keyword": "management consultants", "volume": 50000, "yoy": "0%"},
        {"keyword": "strategy consultants", "volume": 50000, "yoy": "0%"},
        {"keyword": "generative ai consulting", "volume": 50000, "yoy": "0%"},
    ],
    "niche": [
        {"keyword": "ai strategy consulting", "volume": 5000, "yoy": "0%"},
        {"keyword": "ai consulting services", "volume": 5000, "yoy": "0%"},
        {"keyword": "ai ml consulting", "volume": 5000, "yoy": "0%"},
        {"keyword": "applied ai consulting", "volume": 500, "yoy": "0%"},
    ],
}

PROGRESS_FILE = Path(__file__).resolve().parent / "progress.json"


def load_progress() -> Dict:
    """Load progress tracker — which keywords have been processed."""
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"processed": [], "last_run": None, "total_runs": 0}


def save_progress(progress: Dict):
    """Save progress tracker."""
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, default=str), encoding="utf-8")


def get_next_keywords(count: int = 5) -> List[Dict]:
    """Get next unprocessed keywords, prioritizing high-growth ones."""
    progress = load_progress()
    processed = set(progress.get("processed", []))

    all_keywords = (
        SNOIKA_KEYWORDS["priority"]
        + SNOIKA_KEYWORDS["standard"]
        + SNOIKA_KEYWORDS["niche"]
    )

    unprocessed = [kw for kw in all_keywords if kw["keyword"] not in processed]
    return unprocessed[:count]


def process_keyword(keyword_data: Dict, use_ai: bool = True) -> Dict:
    """Run the full pipeline for a single keyword."""
    keyword = keyword_data["keyword"]
    logger.info("Processing keyword: %s", keyword)

    try:
        result = handler.full_pipeline(
            keyword=keyword,
            platform="linkedin",
            campaign="consulting_services",
            use_ai=use_ai,
        )
        return {
            "keyword": keyword,
            "status": "success",
            "pipeline_status": result.get("pipeline_status", "unknown"),
            "items_generated": 4,  # brief + blog + social + designs
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error("Failed to process %s: %s", keyword, e)
        return {
            "keyword": keyword,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }


def run_batch(count: int = 5, use_ai: bool = True) -> Dict:
    """Run batch processing for next N keywords."""
    start = datetime.now()
    keywords = get_next_keywords(count)

    if not keywords:
        return {
            "status": "complete",
            "message": "All 41 keywords have been processed!",
            "total_processed": len(load_progress().get("processed", [])),
        }

    results = []
    progress = load_progress()

    for kw_data in keywords:
        result = process_keyword(kw_data, use_ai=use_ai)
        results.append(result)

        if result["status"] == "success":
            progress["processed"].append(kw_data["keyword"])

    progress["last_run"] = datetime.now().isoformat()
    progress["total_runs"] = progress.get("total_runs", 0) + 1
    save_progress(progress)

    elapsed = (datetime.now() - start).total_seconds()

    return {
        "status": "batch_complete",
        "keywords_processed": len(results),
        "successful": sum(1 for r in results if r["status"] == "success"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "elapsed_seconds": round(elapsed, 2),
        "total_processed_ever": len(progress["processed"]),
        "remaining": 41 - len(progress["processed"]),
        "results": results,
        "next_run_keywords": [kw["keyword"] for kw in get_next_keywords(count)],
    }


def get_batch_status() -> Dict:
    """Get current automation status."""
    progress = load_progress()
    summary = get_weekly_summary()
    next_kws = get_next_keywords(5)

    return {
        "total_keywords": 41,
        "processed": len(progress.get("processed", [])),
        "remaining": 41 - len(progress.get("processed", [])),
        "last_run": progress.get("last_run"),
        "total_runs": progress.get("total_runs", 0),
        "next_keywords": [kw["keyword"] for kw in next_kws],
        "staging_summary": summary,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import argparse

    parser = argparse.ArgumentParser(description="Project Darwin Batch Pipeline")
    parser.add_argument("--count", type=int, default=5, help="Keywords to process")
    parser.add_argument("--all", action="store_true", help="Process all remaining")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--no-ai", action="store_true", help="Skip Claude AI")
    args = parser.parse_args()

    if args.status:
        print(json.dumps(get_batch_status(), indent=2))
    else:
        count = 41 if args.all else args.count
        result = run_batch(count=count, use_ai=not args.no_ai)
        print(json.dumps(result, indent=2))
