"""
Plugin Handler — Command Router for Project Darwin.
Routes all /api/* requests to the appropriate skill,
optionally enhancing output with Claude API.
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
    generate_brief_with_ai,
    write_blog_with_ai,
    create_social_with_ai,
    generate_linkedin_with_ai,
)

logger = logging.getLogger(__name__)


class PluginHandler:
    """Central router that connects API endpoints to skills."""

    # ------------------------------------------------------------------
    # Skill #2 — Strategy Expert
    # ------------------------------------------------------------------
    def generate_brief(self, keyword: str, use_ai: bool = False) -> Dict:
        """Generate a strategic content brief for a keyword."""
        # Template-based brief (always works)
        brief = strategy_expert.generate_brief(keyword)

        # Optionally enhance with Claude AI
        if use_ai:
            brand_rules = brand_guardian.get_rules_for_skill("strategy")
            ai_result = generate_brief_with_ai(keyword, brand_rules)
            if ai_result:
                brief["ai_enhanced"] = True
                brief["ai_content"] = ai_result

        # Validate against brand
        validation = brand_guardian.validate(
            brief.get("blog_structure", {}).get("title", keyword), "brief"
        )
        brief["brand_validation"] = validation
        return brief

    # ------------------------------------------------------------------
    # Skill #3 — Content Writer
    # ------------------------------------------------------------------
    def write_blog(self, brief: Dict, use_ai: bool = False) -> Dict:
        """Write a blog post from a strategic brief."""
        blog = content_writer.write_blog(brief)

        if use_ai:
            ai_result = write_blog_with_ai(brief)
            if ai_result:
                blog["ai_enhanced"] = True
                blog["ai_content"] = ai_result

        # Validate
        full_text = blog.get("introduction", "")
        for s in blog.get("sections", []):
            full_text += " " + s.get("content", "")
        full_text += " " + blog.get("conclusion", "")
        blog["brand_validation"] = brand_guardian.validate(full_text, "blog")
        return blog

    # ------------------------------------------------------------------
    # Skill #4 — Social Creator
    # ------------------------------------------------------------------
    def create_social(
        self,
        blog_data: Dict,
        platform: str = "linkedin",
        campaign: str = "consulting_services",
        content_format: str = "static",
        use_ai: bool = False,
    ) -> Dict:
        """Create platform-specific social posts."""
        posts = social_creator.generate_posts(blog_data, platform, campaign, content_format)

        if use_ai:
            ai_result = create_social_with_ai(blog_data, platform)
            if ai_result:
                posts["ai_enhanced"] = True
                posts["ai_content"] = ai_result

        return posts

    # ------------------------------------------------------------------
    # Skill #5 — Visual Designer
    # ------------------------------------------------------------------
    def design_visuals(self, blog_data: Dict) -> Dict:
        """Generate Nano Banana design prompts."""
        return visual_designer.generate_prompts(blog_data)

    # ------------------------------------------------------------------
    # Skill #6 — Lead Qualifier
    # ------------------------------------------------------------------
    def qualify_leads(self, leads: list) -> Dict:
        """Qualify a batch of leads."""
        return lead_qualifier.qualify_batch(leads)

    def track_engagement(self, lead_id: str, event_type: str) -> Dict:
        """Track a single engagement event."""
        return lead_qualifier.track_engagement(lead_id, event_type)

    # ------------------------------------------------------------------
    # Skill #7 — Analytics Manager
    # ------------------------------------------------------------------
    def analytics_report(self, params: Dict) -> Dict:
        """Generate an analytics report."""
        return analytics_manager.generate_report(
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

    # ------------------------------------------------------------------
    # Skill #8 — LinkedIn Optimizer
    # ------------------------------------------------------------------
    def linkedin_post(self, pillar: str, topic: str = None, use_ai: bool = False) -> Dict:
        """Generate a LinkedIn post for Camila."""
        post = linkedin_optimizer.generate_post(pillar, topic)

        if use_ai and "error" not in post:
            ai_result = generate_linkedin_with_ai(pillar, topic or pillar)
            if ai_result:
                post["ai_enhanced"] = True
                post["ai_content"] = ai_result

        return post

    # ------------------------------------------------------------------
    # Full Pipeline — End-to-End for one keyword
    # ------------------------------------------------------------------
    def full_pipeline(self, keyword: str, platform: str = "linkedin",
                      campaign: str = "consulting_services", use_ai: bool = False) -> Dict:
        """
        Run the complete content pipeline for a single keyword.
        Returns brief + blog + social + design prompts.
        """
        brief = self.generate_brief(keyword, use_ai=use_ai)
        blog = self.write_blog(brief, use_ai=use_ai)
        social = self.create_social(
            {"keyword": keyword, "title": blog.get("title", keyword)},
            platform=platform, campaign=campaign, use_ai=use_ai,
        )
        designs = self.design_visuals({"keyword": keyword, "title": blog.get("title", keyword)})

        return {
            "keyword": keyword,
            "brief": brief,
            "blog": blog,
            "social": social,
            "designs": designs,
            "pipeline_status": "complete",
        }

    # ------------------------------------------------------------------
    # Brand validation
    # ------------------------------------------------------------------
    def validate_content(self, content: str, content_type: str = "blog") -> Dict:
        """Validate any content against brand guidelines."""
        return brand_guardian.validate(content, content_type)

    def get_brand_rules(self) -> Dict:
        """Return complete brand rules."""
        return brand_guardian.get_brand_rules()


handler = PluginHandler()
