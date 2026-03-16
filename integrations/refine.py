"""
Content Refinement for Project Darwin.
When Camila doesn't like content, she sends feedback.
Claude rewrites based on her direction.
"""

import json
import logging
from typing import Dict, Optional

from integrations import call_claude

logger = logging.getLogger(__name__)


def refine_content(content: str, feedback: str, content_type: str = "blog") -> Dict:
    """
    Refine content based on Camila's feedback using Claude AI.
    Falls back to returning the feedback instructions if Claude API unavailable.
    """
    system_prompts = {
        "blog": (
            "You are a senior content editor at Heinrich Co., an AI consulting firm. "
            "Rewrite the blog content based on the feedback provided. "
            "Maintain the same structure and key points, but adjust tone, depth, "
            "and messaging as directed. Keep the Heinrich Co. brand voice: "
            "corporate, direct, precise, executive. "
            "Return the complete rewritten content."
        ),
        "social": (
            "You are a social media editor at Heinrich Co. "
            "Rewrite the social post based on the feedback. "
            "Maintain platform best practices. Keep it concise and engaging. "
            "Return the complete rewritten post."
        ),
        "brief": (
            "You are a content strategist at Heinrich Co. "
            "Revise the strategic brief based on the feedback. "
            "Adjust angles, positioning, or structure as directed. "
            "Return the complete revised brief."
        ),
        "linkedin": (
            "You are editing a LinkedIn post for Camila Heinrich, CEO of Heinrich Co. "
            "Revise based on her feedback. Maintain her authentic voice: "
            "provocative, insightful, story-driven. 250-300 words. "
            "Return the complete rewritten post."
        ),
    }

    system = system_prompts.get(content_type, system_prompts["blog"])

    user_prompt = (
        f"ORIGINAL CONTENT:\n{content}\n\n"
        f"FEEDBACK FROM CAMILA:\n{feedback}\n\n"
        f"Please rewrite the content incorporating this feedback."
    )

    ai_result = call_claude(system, user_prompt, max_tokens=8192)

    if ai_result:
        return {
            "status": "refined",
            "original_length": len(content.split()),
            "refined_length": len(ai_result.split()),
            "refined_content": ai_result,
            "feedback_applied": feedback,
            "content_type": content_type,
        }
    else:
        return {
            "status": "ai_unavailable",
            "message": "Claude API not available. Feedback saved for manual revision.",
            "original_content": content,
            "feedback": feedback,
            "content_type": content_type,
        }
