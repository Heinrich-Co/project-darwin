"""
Skill #8: LinkedIn Content Optimizer
Generates LinkedIn posts following Camila Heinrich's editorial framework.
4 pillars: Structural Intelligence, Leadership & Mindset,
           Culture & Future of Work, Community Connection.
"""

from datetime import datetime
from typing import Dict, Optional


class LinkedInOptimizer:

    PILLARS = {
        "structural_intelligence": {
            "day": "Tuesday",
            "theme": "Before being tech-driven, you need to be structure-driven",
            "format": "Text + bold opener",
            "tone": "Provocative, lucid, direct",
            "formula": {
                "hook": "Provocative statement (NOT a question)",
                "tension": "What people get wrong (lines 2-5)",
                "reframe": "Your perspective (lines 6-12)",
                "cta": "Implicit statement (final line)",
            },
        },
        "leadership_mindset": {
            "day": "Wednesday",
            "theme": "Transforming companies begins with transforming leaders",
            "format": "1st person storytelling",
            "tone": "Humane, reflective, elegant",
            "formula": {
                "opening": "1st person story ('At [event]...')",
                "middle": "The framework / insight",
                "closing": "Conviction statement",
            },
        },
        "culture_future_work": {
            "day": "Thursday",
            "theme": "Technology changes fast. People, not so much",
            "format": "Essay-style, analytical",
            "tone": "Analytical, accessible",
            "formula": {
                "thesis": "Bold opening statement",
                "exploration": "Deep analysis with nuance",
                "synthesis": "Bring it together + implication",
            },
        },
        "community_connection": {
            "day": "Last Thursday of month",
            "theme": "Direct engagement with audience",
            "format": "Poll or open question",
            "tone": "Conversational, collaborative",
            "formula": {
                "format": "Poll or open question",
                "rule": "Respond to EVERY comment",
            },
        },
    }

    ENGAGEMENT_PLAYBOOK = {
        "pre_posting": {
            "target": "20-30 C-level executives/founders in EMEA/LATAM",
            "timing": "2-3 days before posting",
            "action": "Substantive comment (3-4 sentences) on their posts",
        },
        "posting_timing": "9-10 AM CET, Tuesday/Wednesday/Thursday",
        "first_hour": {
            "monitor": "All comments immediately",
            "respond": "With substance (not just 'thanks')",
            "pin": "Best comments to top",
        },
    }

    def generate_post(self, pillar: str, topic: Optional[str] = None) -> Dict:
        """Generate a LinkedIn post for the specified pillar."""
        pillar_key = pillar.lower().replace(" ", "_").replace("&", "and")
        pillar_info = self.PILLARS.get(pillar_key)

        if not pillar_info:
            return {"error": f"Unknown pillar: '{pillar}'. Options: {list(self.PILLARS.keys())}"}

        generators = {
            "structural_intelligence": self._structural,
            "leadership_mindset": self._leadership,
            "culture_future_work": self._culture,
            "community_connection": self._community,
        }
        gen = generators.get(pillar_key, self._structural)
        copy = gen(topic)

        return {
            "pillar": pillar_key,
            "day": pillar_info["day"],
            "theme": pillar_info["theme"],
            "tone": pillar_info["tone"],
            "topic": topic or pillar_info["theme"],
            "copy": copy,
            "posting_time": "9-10 AM CET",
            "engagement_playbook": self.ENGAGEMENT_PLAYBOOK,
            "hashtags": "#HeinrichCo #AITransformation #Leadership #InstitutionalIntelligence",
            "created_at": datetime.now().isoformat(),
        }

    # ------------------------------------------------------------------

    def _structural(self, topic: Optional[str]) -> str:
        return (
            "Most AI implementations fail before they start.\n\n"
            "Here's what I've seen across 40+ countries, 15 years:\n\n"
            "Companies don't fail at transformation because technology isn't good enough.\n\n"
            "They fail because they're trying to solve a structural problem with a technology solution.\n\n"
            "The real issue? Knowledge lives in people, not processes.\n\n"
            "When your best person leaves, so does your competitive advantage.\n\n"
            "This is what I call the 'people-dependent organization' — invisible until "
            "transformation hits.\n\n"
            "The organizations that win aren't the most technological.\n"
            "They're the most self-aware.\n\n"
            "Are you solving for structure, or just buying better tools?"
        )

    def _leadership(self, topic: Optional[str]) -> str:
        return (
            "Last week in a boardroom, a CEO said something that stopped everything:\n\n"
            "'We can buy all the technology we want. But if my team doesn't believe "
            "transformation is possible, nothing changes.'\n\n"
            "She was right.\n\n"
            "Transformation is 20% methodology, 80% belief.\n\n"
            "The organizations that actually transform are led by people who believe:\n"
            "• Their teams are capable of more\n"
            "• Change is possible even when it's hard\n"
            "• The cost of staying the same is higher than the cost of change\n\n"
            "That belief has to come first.\n\n"
            "The best technology in the world won't help a team that doesn't believe "
            "they can be better.\n\n"
            "What belief do YOUR people need from you right now?"
        )

    def _culture(self, topic: Optional[str]) -> str:
        return (
            "Technology changes fast. People, not so much.\n\n"
            "Companies spend billions on new systems. Then they're shocked when adoption "
            "is slow and resistance is high.\n\n"
            "The assumption: If we have the right technology, people will figure it out.\n\n"
            "The reality: If people don't trust leadership, understand why, or see "
            "themselves in the future state — technology is just expensive friction.\n\n"
            "The organizations that transform successfully aren't those with the newest AI.\n"
            "They're those where:\n"
            "• Leadership is visible during the hard parts\n"
            "• People understand WHY change matters\n"
            "• They see how change makes their work more meaningful\n"
            "• Culture shifts BEFORE technology does\n\n"
            "Culture is the bottleneck.\n"
            "Technology is just the expression of culture.\n\n"
            "What's the culture work that needs to happen in YOUR organization?"
        )

    def _community(self, topic: Optional[str]) -> str:
        t = topic or "AI adoption"
        return (
            f"Quick question for my network:\n\n"
            f"What's the single biggest barrier to {t} in your organization right now?\n\n"
            f"A) Leadership buy-in\n"
            f"B) Budget constraints\n"
            f"C) Team skills gap\n"
            f"D) Cultural resistance\n"
            f"E) Something else (tell me in comments)\n\n"
            f"I'll share insights from the responses next week.\n\n"
            f"Drop your answer below 👇"
        )


linkedin_optimizer = LinkedInOptimizer()
