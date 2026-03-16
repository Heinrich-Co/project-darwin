"""
Plugin Handler — Command Router for Project Darwin.

FLOW: Skills generate → Staging (for Camila review) → Approved → Notion (team)
Content NEVER goes directly to Notion. Camila reviews first.
"""

import logging
from typing import Dict

from skills.skill_1_brand_guardian import brand_guardian
from skills.skill_2_strategy import strategy_expert
from skills.skill_3_writer import content_writer
from skills.skill_4_social import social_creator
from skills.skill_5_designer import visual_designer
from skills.skill_6_qualifier import lead_qualifier
from skills.skill_7_analytics import analytics_manager
from skills.skill_8_linkedin import linkedin_optimizer

from integrations import (
    generate_brief_with_ai, write_blog_with_ai,
    create_social_with_ai, generate_linkedin_with_ai,
)
from integrations.staging import (
    stage_brief, stage_blog, stage_social, stage_designs, stage_linkedin,
    list_pending, list_all, get_staged_content, approve_content,
    request_revision, mark_pushed_to_notion, get_weekly_summary,
)
from integrations.notion_sync import (
    sync_brief, sync_blog, sync_social_posts, sync_leads, sync_analytics,
)
from integrations.refine import refine_content

logger = logging.getLogger(__name__)


class PluginHandler:

    # --- Skill #2 Strategy ---
    def generate_brief(self, keyword: str, use_ai: bool = False) -> Dict:
        brief = strategy_expert.generate_brief(keyword)
        if use_ai:
            rules = brand_guardian.get_rules_for_skill("strategy")
            ai = generate_brief_with_ai(keyword, rules)
            if ai:
                brief["ai_enhanced"] = True
                brief["ai_content"] = ai
        brief["brand_validation"] = brand_guardian.validate(
            brief.get("blog_structure", {}).get("title", keyword), "brief")
        brief["staging_file"] = stage_brief(brief)
        return brief

    # --- Skill #3 Writer ---
    def write_blog(self, brief: Dict, use_ai: bool = False) -> Dict:
        blog = content_writer.write_blog(brief)
        if use_ai:
            ai = write_blog_with_ai(brief)
            if ai:
                blog["ai_enhanced"] = True
                blog["ai_content"] = ai
        full = blog.get("introduction", "")
        for s in blog.get("sections", []):
            full += " " + s.get("content", "")
        full += " " + blog.get("conclusion", "")
        blog["brand_validation"] = brand_guardian.validate(full, "blog")
        blog["staging_file"] = stage_blog(blog)
        return blog

    # --- Skill #4 Social ---
    def create_social(self, blog_data: Dict, platform: str = "linkedin",
                      campaign: str = "consulting_services",
                      content_format: str = "static", use_ai: bool = False) -> Dict:
        posts = social_creator.generate_posts(blog_data, platform, campaign, content_format)
        if use_ai:
            ai = create_social_with_ai(blog_data, platform)
            if ai:
                posts["ai_enhanced"] = True
                posts["ai_content"] = ai
        posts["staging_file"] = stage_social(posts)
        return posts

    # --- Skill #5 Designer ---
    def design_visuals(self, blog_data: Dict) -> Dict:
        designs = visual_designer.generate_prompts(blog_data)
        designs["staging_file"] = stage_designs(designs)
        return designs

    # --- Skill #6 Lead Qualifier (direct to Notion — no approval needed) ---
    def qualify_leads(self, leads: list) -> Dict:
        result = lead_qualifier.qualify_batch(leads)
        try:
            sync_leads(result)
        except Exception as e:
            logger.warning("Notion sync (leads) failed: %s", e)
        return result

    def track_engagement(self, lead_id: str, event_type: str) -> Dict:
        return lead_qualifier.track_engagement(lead_id, event_type)

    # --- Skill #7 Analytics (direct to Notion — data not content) ---
    def analytics_report(self, params: Dict) -> Dict:
        report = analytics_manager.generate_report(
            period=params.get("period", "daily"),
            content_pages=params.get("content_pages", 0),
            total_views=params.get("total_views", 0),
            avg_engagement=params.get("avg_engagement", 0.0),
            top_performer=params.get("top_performer", ""),
            content_gaps=params.get("content_gaps", 0),
            deep_engagement=params.get("deep_engagement", 0),
            cta_clicks=params.get("cta_clicks", 0),
            repeat_interest=params.get("repeat_interest", 0),
            total_leads=params.get("total_leads", 0),
            hot_leads=params.get("hot_leads", 0),
        )
        try:
            sync_analytics(report)
        except Exception as e:
            logger.warning("Notion sync (analytics) failed: %s", e)
        return report

    # --- Skill #8 LinkedIn ---
    def linkedin_post(self, pillar: str, topic: str = None, use_ai: bool = False) -> Dict:
        post = linkedin_optimizer.generate_post(pillar, topic)
        if use_ai and "error" not in post:
            ai = generate_linkedin_with_ai(pillar, topic or pillar)
            if ai:
                post["ai_enhanced"] = True
                post["ai_content"] = ai
        if "error" not in post:
            post["staging_file"] = stage_linkedin(post)
        return post

    # --- Full Pipeline ---
    def full_pipeline(self, keyword: str, platform: str = "linkedin",
                      campaign: str = "consulting_services", use_ai: bool = False) -> Dict:
        brief = self.generate_brief(keyword, use_ai=use_ai)
        blog = self.write_blog(brief, use_ai=use_ai)
        social = self.create_social(
            {"keyword": keyword, "title": blog.get("title", keyword)},
            platform=platform, campaign=campaign, use_ai=use_ai)
        designs = self.design_visuals({"keyword": keyword, "title": blog.get("title", keyword)})
        return {
            "keyword": keyword, "brief": brief, "blog": blog,
            "social": social, "designs": designs,
            "pipeline_status": "staged_for_review",
            "message": "All content staged for Camila's review. Approve to push to Notion.",
        }

    # --- Staging: Review & Approval ---
    def get_pending_review(self) -> Dict:
        items = list_pending()
        return {"pending": items, "total": len(items)}

    def get_all_staged(self, status: str = None) -> Dict:
        items = list_all(status)
        return {"items": items, "total": len(items)}

    def review_content(self, file_name: str) -> Dict:
        content = get_staged_content(file_name)
        return content if content else {"error": f"Not found: {file_name}"}

    def approve_and_push(self, file_name: str) -> Dict:
        entry = approve_content(file_name)
        if not entry:
            return {"error": f"Not found: {file_name}"}
        data = entry.get("data", {})
        ctype = entry.get("type", "")
        notion_ok = False
        try:
            if ctype == "brief":
                notion_ok = sync_brief(data) is not None
            elif ctype == "blog":
                notion_ok = sync_blog(data) is not None
            elif ctype == "social":
                notion_ok = sync_social_posts(data) is not None
            if notion_ok:
                mark_pushed_to_notion(file_name)
        except Exception as e:
            logger.warning("Notion push failed: %s", e)
        return {"status": "approved", "notion_synced": notion_ok, "type": ctype, "file": file_name}

    def send_for_revision(self, file_name: str, feedback: str) -> Dict:
        entry = request_revision(file_name, feedback)
        return {"status": "revision_requested", "feedback": feedback} if entry else {"error": "Not found"}

    def refine_staged_content(self, file_name: str, feedback: str) -> Dict:
        entry = get_staged_content(file_name)
        if not entry:
            return {"error": f"Not found: {file_name}"}
        ctype = entry.get("type", "blog")
        data = entry.get("data", {})
        if ctype == "blog":
            original = data.get("ai_content") or data.get("introduction", "")
        elif ctype == "linkedin":
            original = data.get("ai_content") or data.get("copy", "")
        elif ctype == "social":
            original = "\n\n".join(p.get("copy", "") for p in data.get("posts", []))
        else:
            original = str(data)[:3000]
        return refine_content(original, feedback, ctype)

    def weekly_summary(self) -> Dict:
        return get_weekly_summary()

    # --- Brand ---
    def validate_content(self, content: str, content_type: str = "blog") -> Dict:
        return brand_guardian.validate(content, content_type)

    def get_brand_rules(self) -> Dict:
        return brand_guardian.get_brand_rules()


handler = PluginHandler()
