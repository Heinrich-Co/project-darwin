"""
Skill #1: Brand Guardian
Validates all content against Heinrich Co. brand guidelines.
Every piece of content passes through this before output.
"""

from typing import Dict, List


class BrandGuardian:

    BRAND_RULES = {
        "core_mission": "Transform impact organizations into AI-Native companies",
        "voice": {
            "primary": "Professional, strategic, visionary",
            "secondary": "Educational, approachable, thought-leading",
            "avoid": "Salesy, jargon-heavy, generic",
            "personality": "Expert advisor, not vendor",
            "editorial_tone": "Corporate, Direct, Precise, Executive",
        },
        "visual": {
            "deep_black": "#1B1D1E",
            "off_white": "#F2F2F2",
            "signature_light_green": "#CAD3AC",
            "grayish_beige": "#C1B9AD",
            "font": "Work Sans",
            "max_weight": "SemiBold",
            "style": "Clean, minimal, enterprise-professional",
        },
        "ict_segment": {
            "target_audience": "C-suite executives, CTOs, IT directors",
            "company_size": "$1B-$10B revenue",
            "pain_points": [
                "Legacy system modernization",
                "Digital transformation ROI",
                "Talent gap in technical skills",
                "Integration complexity",
                "Cost optimization",
            ],
            "messaging_angles": [
                "Risk mitigation",
                "Cost optimization",
                "Speed to market",
                "Competitive advantage",
                "Scalability",
            ],
        },
        "forbidden_words": [
            "amazing", "awesome", "revolutionary", "game-changing",
            "disruptive", "synergy", "leverage", "paradigm shift",
            "bleeding edge", "world-class", "best-in-class",
        ],
        "content_structure": {
            "blog_length": "1800-2500 words",
            "sections": "6-8",
            "section_length": "200-400 words",
            "categories": [
                "AI Strategy & Transformation",
                "Industry Intelligence",
                "Customer Success Stories",
                "Thought Leadership",
                "Technical Implementation",
                "Market Insights",
            ],
        },
        "linkedin_strategy": {
            "frequency": "3-4 per week",
            "times": "Tuesday-Thursday, 9-12 AM CET",
            "tuesday": "Structural Intelligence",
            "wednesday": "Leadership & Mindset",
            "thursday": "Culture & Future of Work",
            "last_thursday": "Community Connection",
            "mix": {
                "thought_leadership": "40%",
                "case_studies": "30%",
                "industry_insights": "20%",
                "company_updates": "10%",
            },
        },
        "social_rules": {
            "carousel_slides": "5-7",
            "linkedin_hook_length": "150-250 characters",
            "linkedin_format": "Problem > Solution > Insight",
            "instagram_frequency": "Every other day + daily stories",
            "instagram_tone": "Lighter than LinkedIn, visual storytelling",
        },
    }

    def get_brand_rules(self) -> Dict:
        """Return complete brand rules dictionary."""
        return self.BRAND_RULES

    def get_rules_for_skill(self, skill_name: str) -> Dict:
        """Return only the brand rules relevant to a specific skill."""
        mapping = {
            "strategy": ["voice", "ict_segment", "content_structure"],
            "writer": ["voice", "content_structure", "ict_segment"],
            "social": ["voice", "social_rules", "linkedin_strategy"],
            "designer": ["visual"],
            "linkedin": ["voice", "linkedin_strategy", "social_rules"],
        }
        keys = mapping.get(skill_name, [])
        return {k: self.BRAND_RULES[k] for k in keys if k in self.BRAND_RULES}

    def validate(self, content: str, content_type: str = "blog") -> Dict:
        """
        Validate content against brand guidelines.
        Returns dict with 'approved' bool, list of 'issues', and list of 'warnings'.
        """
        issues: List[str] = []
        warnings: List[str] = []
        lower = content.lower()

        # Check forbidden words
        for word in self.BRAND_RULES["forbidden_words"]:
            if word in lower:
                issues.append(f"Forbidden word found: '{word}'")

        # Check length for blog posts
        if content_type == "blog":
            word_count = len(content.split())
            if word_count < 1800:
                warnings.append(f"Blog is {word_count} words; target is 1800-2500.")
            elif word_count > 2600:
                warnings.append(f"Blog is {word_count} words; consider trimming to 2500.")

        # Check tone markers
        salesy_phrases = ["buy now", "limited time", "act fast", "don't miss out", "guaranteed"]
        for phrase in salesy_phrases:
            if phrase in lower:
                issues.append(f"Salesy language detected: '{phrase}'")

        # Check for generic filler
        filler = ["in today's world", "it goes without saying", "at the end of the day"]
        for phrase in filler:
            if phrase in lower:
                warnings.append(f"Generic filler phrase: '{phrase}'")

        approved = len(issues) == 0
        return {
            "approved": approved,
            "issues": issues,
            "warnings": warnings,
            "content_type": content_type,
            "word_count": len(content.split()),
        }


brand_guardian = BrandGuardian()
