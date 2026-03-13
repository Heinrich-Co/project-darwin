"""
Skill #4: Social Creator
Creates platform-specific social posts (LinkedIn, Instagram, YouTube)
with campaign messaging for Heinrich Co.
"""

from datetime import datetime
from typing import Dict, Optional


CAMPAIGN_ANGLES = {
    "consulting_services": {
        "linkedin": {"angle": "Strategic transformation", "hook": "50% of IT projects fail. Strategy is the difference."},
        "instagram": {"angle": "Business transformation journey", "hook": "From chaos to clarity."},
        "youtube": {"angle": "Complete Consulting Guide", "format": "5-phase framework explainer"},
    },
    "ai_skill_builder": {
        "linkedin": {"angle": "Professional development through AI", "hook": "AI isn't replacing your skills. It's supercharging them."},
        "instagram": {"angle": "Empowerment through learning", "hook": "From curious to confident."},
        "youtube": {"angle": "Deep-dive skill building guide", "format": "Tutorial series"},
    },
    "knowledge_transfer": {
        "linkedin": {"angle": "Institutionalizing expertise", "hook": "Your team's knowledge shouldn't walk out the door."},
        "instagram": {"angle": "Team strength through knowledge sharing", "hook": "Knowledge is power. Shared knowledge is unstoppable."},
        "youtube": {"angle": "Knowledge Transfer Frameworks", "format": "Framework deep-dives + case studies"},
    },
    "adoption": {
        "linkedin": {"angle": "Technology adoption", "hook": "The best technology fails without adoption strategy."},
        "instagram": {"angle": "Change management", "hook": "Technology changes fast. People, not so much."},
        "youtube": {"angle": "Adoption best practices", "format": "Step-by-step guides"},
    },
    "human_first": {
        "linkedin": {"angle": "People-centric transformation", "hook": "AI amplifies humans. It doesn't replace them."},
        "instagram": {"angle": "Human + AI collaboration", "hook": "The future is human-first."},
        "youtube": {"angle": "Human-First AI Framework", "format": "Thought leadership"},
    },
    "social_proof": {
        "linkedin": {"angle": "Results and evidence", "hook": "400% ROI in Year 1. Here's how."},
        "instagram": {"angle": "Success stories", "hook": "Real results. Real companies."},
        "youtube": {"angle": "Client case study deep-dive", "format": "Interview + data walkthrough"},
    },
}


class SocialCreator:

    def generate_posts(
        self,
        blog_data: Dict,
        platform: str = "linkedin",
        campaign: str = "consulting_services",
        content_format: str = "static",
    ) -> Dict:
        """Generate platform-specific social posts from blog data."""
        keyword = blog_data.get("keyword", blog_data.get("title", "consulting"))
        title = blog_data.get("title", keyword.title())
        campaign_info = CAMPAIGN_ANGLES.get(campaign, CAMPAIGN_ANGLES["consulting_services"])
        platform_info = campaign_info.get(platform, campaign_info.get("linkedin", {}))
        hook = platform_info.get("hook", f"Why {keyword} matters now.")

        generators = {
            "linkedin": self._linkedin_posts,
            "instagram": self._instagram_posts,
            "youtube": self._youtube_content,
        }
        gen = generators.get(platform, self._linkedin_posts)
        posts = gen(keyword, title, hook, platform_info, content_format)

        return {
            "platform": platform,
            "campaign": campaign,
            "keyword": keyword,
            "format": content_format,
            "posts": posts,
            "created_at": datetime.now().isoformat(),
        }

    # ------------------------------------------------------------------
    def _linkedin_posts(self, keyword, title, hook, info, fmt) -> list:
        static_post = (
            f"{hook}\n\n"
            f"After working with enterprises across 40+ countries over 15 years, one pattern is clear:\n\n"
            f"The organizations that succeed with {keyword} aren't the ones with the biggest budgets.\n"
            f"They're the ones with the clearest strategy.\n\n"
            f"In our latest guide, we break down:\n"
            f"• The 5-phase framework proven at scale\n"
            f"• Real metrics: 300-400% ROI in Year 1\n"
            f"• Why 50% of IT projects fail (and how to be in the other 50%)\n\n"
            f"Read the full guide: [LINK]\n\n"
            f"What's the biggest challenge you've faced with {keyword}? Share below 👇\n\n"
            f"#AITransformation #EnterpriseStrategy #DigitalTransformation #HeinrichCo #CTO"
        )
        carousel_post = (
            f"CAROUSEL: {title}\n\n"
            f"Slide 1 (HOOK): {hook}\n"
            f"Slide 2: The problem — 50% of projects fail\n"
            f"Slide 3: Phase 1-2 — Discovery & Strategy\n"
            f"Slide 4: Phase 3-4 — Validation & Implementation\n"
            f"Slide 5: Phase 5 — Optimization & Results\n"
            f"Slide 6: Real results — 400% ROI case study\n"
            f"Slide 7 (CTA): Schedule your assessment → [LINK]\n\n"
            f"Caption: {hook} Swipe to see how we help enterprises transform.\n\n"
            f"#Consulting #Strategy #DigitalTransformation #HeinrichCo"
        )
        return [
            {"type": "static", "copy": static_post, "hashtags": 5, "cta": "soft"},
            {"type": "carousel", "copy": carousel_post, "slides": 7, "cta": "direct"},
        ]

    def _instagram_posts(self, keyword, title, hook, info, fmt) -> list:
        carousel = (
            f"CAROUSEL (1080x1080):\n"
            f"Slide 1: {hook} (bold text on brand background)\n"
            f"Slide 2: The 5-Phase Framework (infographic)\n"
            f"Slide 3: ROI — 300-400% in Year 1 (data visual)\n"
            f"Slide 4: Case study — $8M savings (results card)\n"
            f"Slide 5: CTA — Link in bio\n\n"
            f"Caption:\n{hook}\n\n"
            f"Here's the proven framework that transforms {keyword} from cost center to competitive advantage.\n\n"
            f"Swipe to see the 5 phases → \n\n"
            f"Link in bio for the full guide.\n\n"
            f"#HeinrichCo #AITransformation #BusinessStrategy #Consulting "
            f"#DigitalTransformation #Leadership #Innovation #TechStrategy"
        )
        reel = (
            f"REEL SCRIPT (15-30 sec):\n"
            f"Hook (0-3s): \"{hook}\"\n"
            f"Problem (3-8s): \"Most companies waste millions on the wrong approach.\"\n"
            f"Solution (8-20s): \"Our 5-phase framework delivers 400% ROI.\"\n"
            f"CTA (20-30s): \"Link in bio for the complete guide.\"\n"
            f"Audio: Trending business/tech sound\n"
            f"Visuals: Quick cuts of team, data dashboards, transformation moments"
        )
        return [
            {"type": "carousel", "copy": carousel, "slides": 5, "dimensions": "1080x1080"},
            {"type": "reel", "copy": reel, "duration_sec": 30, "dimensions": "1080x1920"},
        ]

    def _youtube_content(self, keyword, title, hook, info, fmt) -> list:
        video = (
            f"VIDEO: {title}\n"
            f"Length: 10-15 minutes\n\n"
            f"Intro (0:00-1:00): {hook} + what you'll learn\n"
            f"Section 1 (1:00-3:00): Why most {keyword} projects fail\n"
            f"Section 2 (3:00-7:00): The 5-Phase Framework\n"
            f"Section 3 (7:00-10:00): ROI calculation + case study\n"
            f"Section 4 (10:00-13:00): How to choose the right partner\n"
            f"Outro (13:00-15:00): CTA + subscribe\n\n"
            f"Thumbnail: Split-screen before/after with text overlay\n"
            f"Description: 500+ words with timestamps, links, and keywords\n"
            f"Tags: {keyword}, consulting, digital transformation, AI, enterprise"
        )
        return [{"type": "long_video", "copy": video, "duration_min": 15}]


social_creator = SocialCreator()
