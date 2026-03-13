"""
Project Darwin — The Heinrich Co. Brain Model
Main Flask application with all API endpoints.

Endpoints
---------
GET  /                       Health check
GET  /api/brand-rules        Get brand guidelines
POST /api/validate           Validate content against brand
POST /api/generate-brief     Skill #2 — Strategic brief
POST /api/write-blog         Skill #3 — Blog post
POST /api/create-social      Skill #4 — Social posts
POST /api/design-visuals     Skill #5 — Design prompts
POST /api/qualify-leads      Skill #6 — Lead qualification
POST /api/track-engagement   Skill #6b — Engagement tracking
POST /api/analytics-report   Skill #7 — Analytics report
POST /api/linkedin-post      Skill #8 — LinkedIn post
POST /api/full-pipeline      Full end-to-end pipeline
"""

import os
import logging
from datetime import datetime

from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from handlers import handler  # noqa: E402 (must be after load_dotenv)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("darwin")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _json_error(msg: str, code: int = 400):
    return jsonify({"status": "error", "message": msg}), code


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "project": "Project Darwin — The Heinrich Co. Brain Model",
        "version": "2.0",
        "skills": [
            "1. Brand Guardian",
            "2. Strategy Expert",
            "3. Content Writer",
            "4. Social Creator",
            "5. Visual Designer",
            "6. Lead Qualifier",
            "7. Analytics Manager",
            "8. LinkedIn Optimizer",
        ],
        "timestamp": datetime.now().isoformat(),
    })


# ---------------------------------------------------------------------------
# Brand Rules (GET)
# ---------------------------------------------------------------------------
@app.route("/api/brand-rules", methods=["GET"])
def brand_rules():
    return jsonify({"status": "success", "rules": handler.get_brand_rules()})


# ---------------------------------------------------------------------------
# Validate Content (POST)
# ---------------------------------------------------------------------------
@app.route("/api/validate", methods=["POST"])
def validate_content():
    data = request.get_json(silent=True) or {}
    content = data.get("content", "")
    content_type = data.get("content_type", "blog")
    if not content:
        return _json_error("'content' is required.")
    result = handler.validate_content(content, content_type)
    return jsonify({"status": "success", "validation": result})


# ---------------------------------------------------------------------------
# Skill #2 — Generate Brief
# ---------------------------------------------------------------------------
@app.route("/api/generate-brief", methods=["POST"])
def generate_brief():
    data = request.get_json(silent=True) or {}
    keyword = data.get("keyword", "")
    if not keyword:
        return _json_error("'keyword' is required.")
    use_ai = data.get("use_ai", False)
    try:
        brief = handler.generate_brief(keyword, use_ai=use_ai)
        return jsonify({"status": "success", "brief": brief})
    except Exception as e:
        logger.exception("generate-brief failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #3 — Write Blog
# ---------------------------------------------------------------------------
@app.route("/api/write-blog", methods=["POST"])
def write_blog():
    data = request.get_json(silent=True) or {}
    # Accept either a full brief object or a keyword
    brief = data.get("brief")
    if not brief:
        keyword = data.get("keyword", "")
        if not keyword:
            return _json_error("'brief' object or 'keyword' string is required.")
        brief = handler.generate_brief(keyword)
    use_ai = data.get("use_ai", False)
    try:
        blog = handler.write_blog(brief, use_ai=use_ai)
        return jsonify({"status": "success", "blog": blog})
    except Exception as e:
        logger.exception("write-blog failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #4 — Create Social Posts
# ---------------------------------------------------------------------------
@app.route("/api/create-social", methods=["POST"])
def create_social():
    data = request.get_json(silent=True) or {}
    blog_data = data.get("blog_data", data)
    platform = data.get("platform", "linkedin")
    campaign = data.get("campaign", "consulting_services")
    content_format = data.get("format", "static")
    use_ai = data.get("use_ai", False)
    try:
        posts = handler.create_social(blog_data, platform, campaign, content_format, use_ai)
        return jsonify({"status": "success", "social": posts})
    except Exception as e:
        logger.exception("create-social failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #5 — Design Visuals
# ---------------------------------------------------------------------------
@app.route("/api/design-visuals", methods=["POST"])
def design_visuals():
    data = request.get_json(silent=True) or {}
    blog_data = data.get("blog_data", data)
    try:
        prompts = handler.design_visuals(blog_data)
        return jsonify({"status": "success", "designs": prompts})
    except Exception as e:
        logger.exception("design-visuals failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #6 — Qualify Leads
# ---------------------------------------------------------------------------
@app.route("/api/qualify-leads", methods=["POST"])
def qualify_leads():
    data = request.get_json(silent=True) or {}
    leads = data.get("leads", [])
    if not leads:
        return _json_error("'leads' array is required.")
    try:
        result = handler.qualify_leads(leads)
        return jsonify({"status": "success", "qualification": result})
    except Exception as e:
        logger.exception("qualify-leads failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #6b — Track Engagement
# ---------------------------------------------------------------------------
@app.route("/api/track-engagement", methods=["POST"])
def track_engagement():
    data = request.get_json(silent=True) or {}
    lead_id = data.get("lead_id", "")
    event_type = data.get("event_type", "")
    if not lead_id or not event_type:
        return _json_error("'lead_id' and 'event_type' are required.")
    try:
        result = handler.track_engagement(lead_id, event_type)
        return jsonify({"status": "success", "engagement": result})
    except Exception as e:
        logger.exception("track-engagement failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #7 — Analytics Report
# ---------------------------------------------------------------------------
@app.route("/api/analytics-report", methods=["POST"])
def analytics_report():
    data = request.get_json(silent=True) or {}
    try:
        report = handler.analytics_report(data)
        return jsonify({"status": "success", "report": report})
    except Exception as e:
        logger.exception("analytics-report failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Skill #8 — LinkedIn Post
# ---------------------------------------------------------------------------
@app.route("/api/linkedin-post", methods=["POST"])
def linkedin_post():
    data = request.get_json(silent=True) or {}
    pillar = data.get("pillar", "")
    if not pillar:
        return _json_error("'pillar' is required. Options: structural_intelligence, leadership_mindset, culture_future_work, community_connection")
    topic = data.get("topic")
    use_ai = data.get("use_ai", False)
    try:
        post = handler.linkedin_post(pillar, topic, use_ai=use_ai)
        if "error" in post:
            return _json_error(post["error"])
        return jsonify({"status": "success", "post": post})
    except Exception as e:
        logger.exception("linkedin-post failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Full Pipeline — End-to-End
# ---------------------------------------------------------------------------
@app.route("/api/full-pipeline", methods=["POST"])
def full_pipeline():
    data = request.get_json(silent=True) or {}
    keyword = data.get("keyword", "")
    if not keyword:
        return _json_error("'keyword' is required.")
    platform = data.get("platform", "linkedin")
    campaign = data.get("campaign", "consulting_services")
    use_ai = data.get("use_ai", False)
    try:
        result = handler.full_pipeline(keyword, platform, campaign, use_ai)
        return jsonify({"status": "success", "pipeline": result})
    except Exception as e:
        logger.exception("full-pipeline failed")
        return _json_error(str(e), 500)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
