"""
Claude API Integration
Sends prompts to Claude API for AI-enhanced content generation.
Falls back to template-based output when API key is not set.
"""

import json
import logging
from typing import Dict, Optional

from config import config

logger = logging.getLogger(__name__)

# Only import anthropic if we have an API key
_client = None


def _get_client():
    """Lazy-initialize the Anthropic client."""
    global _client
    if _client is not None:
        return _client
    if not config.ANTHROPIC_API_KEY:
        return None
    try:
        from anthropic import Anthropic
        _client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        return _client
    except Exception as e:
        logger.warning("Could not initialize Anthropic client: %s", e)
        return None


def call_claude(system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> Optional[str]:
    """
    Send a prompt to Claude and return the text response.
    Returns None if the API is unavailable or errors occur.
    """
    client = _get_client()
    if client is None:
        logger.info("Claude API not available — using template output.")
        return None

    try:
        message = client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        # Extract text from response
        text_parts = [block.text for block in message.content if hasattr(block, "text")]
        return "\n".join(text_parts)
    except Exception as e:
        logger.error("Claude API call failed: %s", e)
        return None


def generate_brief_with_ai(keyword: str, brand_rules: Dict) -> Optional[str]:
    """Use Claude to generate a richer strategic brief."""
    system = (
        "You are a senior content strategist at Heinrich Co., an AI consulting firm. "
        "Generate a strategic content brief for the given keyword. "
        "Include 3 content angles, blog structure, SEO strategy, and target metrics. "
        "Respond in JSON format only, no markdown."
    )
    user = (
        f"Keyword: {keyword}\n"
        f"Brand voice: {json.dumps(brand_rules.get('voice', {}))}\n"
        f"Target audience: {json.dumps(brand_rules.get('ict_segment', {}))}\n"
        "Generate a strategic brief with 3 angles, blog structure, and SEO plan."
    )
    return call_claude(system, user)


def write_blog_with_ai(brief: Dict) -> Optional[str]:
    """Use Claude to write a complete blog post from a brief."""
    system = (
        "You are a senior content writer at Heinrich Co., an AI consulting firm. "
        "Write a comprehensive 2400-word blog post based on the strategic brief provided. "
        "Use professional tone. Include real-world examples and data. "
        "Respond with the blog post text only, no JSON wrapper."
    )
    user = f"Strategic Brief:\n{json.dumps(brief, indent=2)}"
    return call_claude(system, user, max_tokens=8192)


def create_social_with_ai(blog_data: Dict, platform: str) -> Optional[str]:
    """Use Claude to create platform-specific social posts."""
    system = (
        f"You are a social media strategist at Heinrich Co. "
        f"Create 2-3 {platform} posts based on the blog content provided. "
        f"Follow platform best practices. Respond in JSON format."
    )
    title = blog_data.get("title", "")
    keyword = blog_data.get("keyword", "")
    user = f"Blog title: {title}\nKeyword: {keyword}\nPlatform: {platform}"
    return call_claude(system, user)


def generate_linkedin_with_ai(pillar: str, topic: str) -> Optional[str]:
    """Use Claude to generate a LinkedIn post following Camila's framework."""
    system = (
        "You are writing a LinkedIn post for Camila Heinrich, CEO of Heinrich Co. "
        "Follow her editorial framework: provocative hook, personal insight, "
        "professional expertise, clear point of view. "
        "Respond with the post text only (250-300 words). No hashtags in the body."
    )
    user = f"Pillar: {pillar}\nTopic: {topic}"
    return call_claude(system, user)
