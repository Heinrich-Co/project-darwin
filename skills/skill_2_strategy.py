"""
Skill #2: Strategy Expert
Takes a Snoika keyword and generates a strategic content brief
with 3 angles, blog structure, SEO strategy, and target metrics.
"""

from datetime import datetime
from typing import Dict

from skills.skill_1_brand_guardian import brand_guardian

# Known Snoika keywords with metadata
SNOIKA_KEYWORDS: Dict[str, Dict] = {
    "consulting services it": {"volume": 50000, "yoy": "900%", "competition": "Low", "intent": "commercial"},
    "business consulting services": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "business consulting firms": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "tech consulting firms": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "technology consulting firms": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "sales consulting": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "it consulting firms": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "tech consulting companies": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "management consultants": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "strategy consultants": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "bpo services": {"volume": 50000, "yoy": "900%", "competition": "Low", "intent": "commercial"},
    "business process outsourcing services": {"volume": 50000, "yoy": "900%", "competition": "Low", "intent": "commercial"},
    "bpo it services": {"volume": 50000, "yoy": "900%", "competition": "Low", "intent": "commercial"},
    "generative ai consulting": {"volume": 50000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "ai strategy consulting": {"volume": 5000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "ai consulting services": {"volume": 5000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "ai ml consulting": {"volume": 5000, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "best ai consulting firms": {"volume": 500, "yoy": "900%", "competition": "Low", "intent": "commercial"},
    "applied ai consulting": {"volume": 500, "yoy": "0%", "competition": "Low", "intent": "commercial"},
    "healthcare ai consulting": {"volume": 500, "yoy": "900%", "competition": "Low", "intent": "commercial"},
    "top ai consulting companies": {"volume": 500, "yoy": "900%", "competition": "Low", "intent": "commercial"},
}


class StrategyExpert:

    def __init__(self):
        self.brand = brand_guardian.get_rules_for_skill("strategy")

    def generate_brief(self, keyword: str) -> Dict:
        """Generate a full strategic brief for the given keyword."""
        kw_lower = keyword.lower().strip()
        kw_data = SNOIKA_KEYWORDS.get(kw_lower, {})

        brief_id = f"brief_{kw_lower.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ict = self.brand.get("ict_segment", {})

        return {
            "brief_id": brief_id,
            "keyword": keyword,
            "keyword_data": kw_data if kw_data else {"volume": "unknown", "competition": "unknown", "intent": "commercial"},
            "target_persona": {
                "titles": ict.get("target_audience", "C-suite executives"),
                "company_size": ict.get("company_size", "$1B-$10B"),
                "pain_points": ict.get("pain_points", []),
            },
            "content_angles": [
                {
                    "angle": "Risk Mitigation & Compliance",
                    "hook": f"50% of IT projects fail — here's why {keyword} changes the equation.",
                    "story": "Legacy systems, security risks, compliance challenges",
                    "value_prop": "Proven methodology reduces project failure risk by 80%",
                    "stage": "Awareness / Consideration",
                    "tone": "Serious, expert, data-driven",
                },
                {
                    "angle": "Cost Optimization & ROI",
                    "hook": f"Cut operational costs by 30% while accelerating innovation with {keyword}.",
                    "story": "Technology sprawl, duplicate systems, wasted budget",
                    "value_prop": "Framework that delivers 300% ROI in Year 1",
                    "stage": "Consideration / Decision",
                    "tone": "Data-driven, practical, ROI-focused",
                },
                {
                    "angle": "Speed to Market & Competitive Advantage",
                    "hook": f"Deploy new capabilities 60% faster with the right {keyword} partner.",
                    "story": "Competitors innovating faster, market pressures mounting",
                    "value_prop": "Agile transformation methodology proven at scale",
                    "stage": "Decision",
                    "tone": "Urgent, visionary, action-oriented",
                },
            ],
            "keyword_variations": [
                kw_lower,
                f"{kw_lower} firms",
                f"enterprise {kw_lower}",
                f"best {kw_lower} companies",
                f"{kw_lower} for mid-market",
                f"top {kw_lower}",
                f"{kw_lower} providers",
            ],
            "blog_structure": {
                "title": f"{keyword.title()}: Complete Implementation Guide for Enterprise Leaders",
                "format": "Comprehensive guide (2000-2500 words)",
                "sections": [
                    {"heading": f"Why {keyword.title()} Matters for Enterprise Growth", "words": "250-300"},
                    {"heading": "The 5-Phase Consulting Framework", "words": "800-1000"},
                    {"heading": "ROI Calculation & Business Case", "words": "300-400"},
                    {"heading": "Risk Mitigation Strategies", "words": "300-400"},
                    {"heading": "Real-World Case Study", "words": "400-500"},
                    {"heading": "How to Choose the Right Partner", "words": "300-400"},
                ],
                "conclusion": {"heading": "Getting Started: Your Next Steps", "words": "200-300"},
            },
            "cta_strategy": {
                "primary": f"Schedule a free {keyword.title()} assessment",
                "secondary": "Download our implementation checklist",
                "urgency": "First 10 companies receive a complimentary roadmap",
            },
            "seo_strategy": {
                "focus_keyword": kw_lower,
                "meta_description": f"Learn how {keyword} transforms enterprise operations. ROI-focused strategies, risk mitigation, proven frameworks from Heinrich Co.",
                "internal_links": [
                    "/blog/organizational-intelligence-competitive-advantage",
                    "/blog/intelligent-automation-architecture",
                    "/blog/ai-implementation-without-disruption",
                ],
            },
            "target_metrics": {
                "views_30d": "1000+",
                "engagement_rate": "8%+",
                "leads": "50+ qualified",
                "ranking_target": f"Top 10 for '{kw_lower}' in 90 days",
            },
            "created_at": datetime.now().isoformat(),
            "status": "ready_for_writer",
        }


strategy_expert = StrategyExpert()
