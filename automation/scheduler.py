"""
Scale 1: Content Scheduler
Runs as a background thread in Flask or standalone cron job.
Triggers batch pipeline on schedule (e.g., every Monday 9 AM).
Also handles n8n webhook integration.
"""

import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

from automation.batch_pipeline import run_batch, get_batch_status

logger = logging.getLogger("automation.scheduler")

# Schedule configuration
SCHEDULE_CONFIG = {
    "content_generation": {
        "day": "monday",
        "hour": 9,
        "minute": 0,
        "keywords_per_run": 5,
        "enabled": True,
    },
    "linkedin_posts": {
        "days": ["tuesday", "wednesday", "thursday"],
        "hour": 8,
        "minute": 0,
        "enabled": True,
    },
    "weekly_report": {
        "day": "friday",
        "hour": 16,
        "minute": 0,
        "enabled": True,
    },
}


class ContentScheduler:
    """Background scheduler for automated content generation."""

    def __init__(self):
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.run_log: list = []

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        logger.info("Scheduler started")

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Scheduler stopped")

    def _loop(self):
        while self._running:
            now = datetime.now()
            day_name = now.strftime("%A").lower()
            hour = now.hour
            minute = now.minute

            # Check content generation schedule
            cfg = SCHEDULE_CONFIG["content_generation"]
            if (cfg["enabled"] and day_name == cfg["day"]
                    and hour == cfg["hour"] and minute == cfg["minute"]):
                self._run_content_batch(cfg["keywords_per_run"])

            # Check weekly report schedule
            cfg = SCHEDULE_CONFIG["weekly_report"]
            if (cfg["enabled"] and day_name == cfg["day"]
                    and hour == cfg["hour"] and minute == cfg["minute"]):
                self._generate_weekly_report()

            time.sleep(60)  # Check every minute

    def _run_content_batch(self, count: int):
        logger.info("Scheduled batch run: %d keywords", count)
        try:
            result = run_batch(count=count, use_ai=True)
            self.run_log.append({
                "type": "content_batch",
                "timestamp": datetime.now().isoformat(),
                "result": result,
            })
        except Exception as e:
            logger.error("Scheduled batch failed: %s", e)

    def _generate_weekly_report(self):
        logger.info("Generating weekly report")
        try:
            status = get_batch_status()
            self.run_log.append({
                "type": "weekly_report",
                "timestamp": datetime.now().isoformat(),
                "status": status,
            })
        except Exception as e:
            logger.error("Weekly report failed: %s", e)

    def get_status(self) -> Dict:
        return {
            "running": self._running,
            "schedule": SCHEDULE_CONFIG,
            "recent_runs": self.run_log[-10:],
            "next_content_run": self._next_run_time("content_generation"),
        }

    def _next_run_time(self, schedule_name: str) -> str:
        cfg = SCHEDULE_CONFIG.get(schedule_name, {})
        if not cfg.get("enabled"):
            return "Disabled"
        day = cfg.get("day", "monday")
        days_map = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                    "friday": 4, "saturday": 5, "sunday": 6}
        target = days_map.get(day, 0)
        now = datetime.now()
        days_ahead = (target - now.weekday()) % 7
        if days_ahead == 0 and now.hour >= cfg.get("hour", 9):
            days_ahead = 7
        next_date = now + timedelta(days=days_ahead)
        return next_date.strftime("%A, %B %d at %d:%02d AM" % (cfg["hour"], cfg["minute"]))


# Webhook handler for n8n integration
def handle_n8n_webhook(payload: Dict) -> Dict:
    """Process webhook from n8n automation platform."""
    action = payload.get("action", "run_batch")

    if action == "run_batch":
        count = payload.get("count", 5)
        return run_batch(count=count, use_ai=True)
    elif action == "status":
        return get_batch_status()
    elif action == "linkedin":
        from handlers import handler as h
        pillar = payload.get("pillar", "structural_intelligence")
        return h.linkedin_post(pillar, use_ai=True)
    else:
        return {"error": f"Unknown action: {action}"}


# Global scheduler instance
scheduler = ContentScheduler()
