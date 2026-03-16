"""
Project Darwin — The Heinrich Co. Brain Model
Main Flask application.

CONTENT FLOW:
  Skills generate → Staging → Camila reviews → Approved → Notion (team)

ENDPOINTS:
  GET  /                         Health check
  GET  /api/brand-rules          Brand guidelines
  POST /api/validate             Validate content
  POST /api/generate-brief       Skill #2
  POST /api/write-blog           Skill #3
  POST /api/create-social        Skill #4
  POST /api/design-visuals       Skill #5
  POST /api/qualify-leads        Skill #6
  POST /api/track-engagement     Skill #6b
  POST /api/analytics-report     Skill #7
  POST /api/linkedin-post        Skill #8
  POST /api/full-pipeline        End-to-end
  GET  /api/staging/pending      Pending review items
  GET  /api/staging/all          All staged items
  POST /api/staging/review       View staged content
  POST /api/staging/approve      Approve → push to Notion
  POST /api/staging/revise       Send back with feedback
  POST /api/staging/refine       Claude rewrites based on feedback
  GET  /api/staging/summary      Weekly summary
  GET  /api/notion-status        Notion connection check
"""

import os
import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from handlers import handler  # noqa: E402

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("darwin")


def _err(msg, code=400):
    return jsonify({"status": "error", "message": msg}), code


# === Health ===
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "project": "Project Darwin — The Heinrich Co. Brain Model",
        "version": "3.0",
        "content_flow": "Generate → Stage → Camila Reviews → Approve → Notion",
        "skills": 8,
        "endpoints": 19,
        "timestamp": datetime.now().isoformat(),
    })


# === Brand Rules ===
@app.route("/api/brand-rules", methods=["GET"])
def brand_rules():
    return jsonify({"status": "success", "rules": handler.get_brand_rules()})


# === Validate ===
@app.route("/api/validate", methods=["POST"])
def validate():
    d = request.get_json(silent=True) or {}
    if not d.get("content"):
        return _err("'content' required")
    return jsonify({"status": "success", "validation": handler.validate_content(d["content"], d.get("content_type", "blog"))})


# === Skill #2 ===
@app.route("/api/generate-brief", methods=["POST"])
def generate_brief():
    d = request.get_json(silent=True) or {}
    if not d.get("keyword"):
        return _err("'keyword' required")
    try:
        return jsonify({"status": "success", "brief": handler.generate_brief(d["keyword"], d.get("use_ai", False))})
    except Exception as e:
        logger.exception("generate-brief failed")
        return _err(str(e), 500)


# === Skill #3 ===
@app.route("/api/write-blog", methods=["POST"])
def write_blog():
    d = request.get_json(silent=True) or {}
    brief = d.get("brief")
    if not brief:
        kw = d.get("keyword", "")
        if not kw:
            return _err("'brief' or 'keyword' required")
        brief = handler.generate_brief(kw)
    try:
        return jsonify({"status": "success", "blog": handler.write_blog(brief, d.get("use_ai", False))})
    except Exception as e:
        logger.exception("write-blog failed")
        return _err(str(e), 500)


# === Skill #4 ===
@app.route("/api/create-social", methods=["POST"])
def create_social():
    d = request.get_json(silent=True) or {}
    try:
        return jsonify({"status": "success", "social": handler.create_social(
            d.get("blog_data", d), d.get("platform", "linkedin"),
            d.get("campaign", "consulting_services"), d.get("format", "static"), d.get("use_ai", False))})
    except Exception as e:
        logger.exception("create-social failed")
        return _err(str(e), 500)


# === Skill #5 ===
@app.route("/api/design-visuals", methods=["POST"])
def design_visuals():
    d = request.get_json(silent=True) or {}
    try:
        return jsonify({"status": "success", "designs": handler.design_visuals(d.get("blog_data", d))})
    except Exception as e:
        return _err(str(e), 500)


# === Skill #6 ===
@app.route("/api/qualify-leads", methods=["POST"])
def qualify_leads():
    d = request.get_json(silent=True) or {}
    if not d.get("leads"):
        return _err("'leads' array required")
    try:
        return jsonify({"status": "success", "qualification": handler.qualify_leads(d["leads"])})
    except Exception as e:
        return _err(str(e), 500)


@app.route("/api/track-engagement", methods=["POST"])
def track_engagement():
    d = request.get_json(silent=True) or {}
    if not d.get("lead_id") or not d.get("event_type"):
        return _err("'lead_id' and 'event_type' required")
    return jsonify({"status": "success", "engagement": handler.track_engagement(d["lead_id"], d["event_type"])})


# === Skill #7 ===
@app.route("/api/analytics-report", methods=["POST"])
def analytics_report():
    d = request.get_json(silent=True) or {}
    try:
        return jsonify({"status": "success", "report": handler.analytics_report(d)})
    except Exception as e:
        return _err(str(e), 500)


# === Skill #8 ===
@app.route("/api/linkedin-post", methods=["POST"])
def linkedin_post():
    d = request.get_json(silent=True) or {}
    if not d.get("pillar"):
        return _err("'pillar' required")
    try:
        post = handler.linkedin_post(d["pillar"], d.get("topic"), d.get("use_ai", False))
        if "error" in post:
            return _err(post["error"])
        return jsonify({"status": "success", "post": post})
    except Exception as e:
        return _err(str(e), 500)


# === Full Pipeline ===
@app.route("/api/full-pipeline", methods=["POST"])
def full_pipeline():
    d = request.get_json(silent=True) or {}
    if not d.get("keyword"):
        return _err("'keyword' required")
    try:
        return jsonify({"status": "success", "pipeline": handler.full_pipeline(
            d["keyword"], d.get("platform", "linkedin"),
            d.get("campaign", "consulting_services"), d.get("use_ai", False))})
    except Exception as e:
        logger.exception("full-pipeline failed")
        return _err(str(e), 500)


# =====================================================================
# STAGING — Camila's Review & Approval System
# =====================================================================

@app.route("/api/staging/pending", methods=["GET"])
def staging_pending():
    """List all content waiting for Camila's review."""
    return jsonify({"status": "success", "review_queue": handler.get_pending_review()})


@app.route("/api/staging/all", methods=["GET"])
def staging_all():
    """List all staged content (optional ?status= filter)."""
    status = request.args.get("status")
    return jsonify({"status": "success", "staged": handler.get_all_staged(status)})


@app.route("/api/staging/review", methods=["POST"])
def staging_review():
    """View full content of a staged item."""
    d = request.get_json(silent=True) or {}
    if not d.get("file"):
        return _err("'file' (staging filename) required")
    content = handler.review_content(d["file"])
    if "error" in content:
        return _err(content["error"], 404)
    return jsonify({"status": "success", "content": content})


@app.route("/api/staging/approve", methods=["POST"])
def staging_approve():
    """Approve content → push to Notion for team."""
    d = request.get_json(silent=True) or {}
    if not d.get("file"):
        return _err("'file' required")
    result = handler.approve_and_push(d["file"])
    if "error" in result:
        return _err(result["error"], 404)
    return jsonify({"status": "success", "approval": result})


@app.route("/api/staging/revise", methods=["POST"])
def staging_revise():
    """Send content back for revision with feedback."""
    d = request.get_json(silent=True) or {}
    if not d.get("file") or not d.get("feedback"):
        return _err("'file' and 'feedback' required")
    result = handler.send_for_revision(d["file"], d["feedback"])
    if "error" in result:
        return _err(result["error"], 404)
    return jsonify({"status": "success", "revision": result})


@app.route("/api/staging/refine", methods=["POST"])
def staging_refine():
    """Claude rewrites content based on Camila's feedback."""
    d = request.get_json(silent=True) or {}
    if not d.get("file") or not d.get("feedback"):
        return _err("'file' and 'feedback' required")
    try:
        result = handler.refine_staged_content(d["file"], d["feedback"])
        if "error" in result:
            return _err(result["error"], 404)
        return jsonify({"status": "success", "refined": result})
    except Exception as e:
        return _err(str(e), 500)


@app.route("/api/staging/summary", methods=["GET"])
def staging_summary():
    """Weekly summary — how many items pending, approved, revised."""
    return jsonify({"status": "success", "summary": handler.weekly_summary()})


# === Notion Status ===
@app.route("/api/notion-status", methods=["GET"])
def notion_status():
    from integrations.notion_sync import check_connection
    return jsonify({"status": "success", "notion": check_connection()})


# === Run ===
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
