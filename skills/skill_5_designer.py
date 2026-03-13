"""
Skill #5: Visual Designer
Generates design briefs / Nano Banana prompts for graphics
aligned with Heinrich Co. visual identity.
"""

from datetime import datetime
from typing import Dict


class VisualDesigner:

    BRAND_COLORS = {
        "deep_black": "#1B1D1E",
        "off_white": "#F2F2F2",
        "light_green": "#CAD3AC",
        "grayish_beige": "#C1B9AD",
    }

    def generate_prompts(self, blog_data: Dict) -> Dict:
        """
        Generate 5 design brief / Nano Banana prompts for a blog post.
        Each prompt is ready to paste into Nano Banana or any AI image tool.
        """
        title = blog_data.get("title", "Consulting Guide")
        keyword = blog_data.get("keyword", "consulting")

        prompts = {
            "blog_featured_image": {
                "dimensions": "1200x800",
                "use": "Blog hero / featured image",
                "prompt": (
                    f"Professional split-screen infographic for '{title}'. "
                    f"LEFT side: Legacy chaos — old servers, tangled cables, stressed team. "
                    f"Dark grays and blacks. RIGHT side: Modern cloud — clean infrastructure, "
                    f"organized team, upward graphs. Brand colors: {self.BRAND_COLORS['deep_black']} "
                    f"and {self.BRAND_COLORS['light_green']}. CENTER: Large forward arrow. "
                    f"Overlay metrics: '60% Faster', '$8M Savings', '99.95% Uptime'. "
                    f"Style: Enterprise-professional, high contrast, minimalist. "
                    f"Font: Work Sans SemiBold."
                ),
            },
            "instagram_carousel": {
                "dimensions": "1080x1080",
                "use": "Instagram carousel slide / social card",
                "prompt": (
                    f"Clean infographic: '5-Phase Consulting Framework'. "
                    f"5 numbered boxes in a horizontal flow with subtle connecting arrows. "
                    f"1. Discovery (magnifying glass icon) 2. Strategy (roadmap icon) "
                    f"3. Validation (handshake icon) 4. Implementation (rocket icon) "
                    f"5. Optimization (chart-up icon). Each box shows phase number, name, "
                    f"and duration. Background: {self.BRAND_COLORS['off_white']}. "
                    f"Primary color: {self.BRAND_COLORS['deep_black']}. "
                    f"Accent: {self.BRAND_COLORS['light_green']}. "
                    f"Style: Clean, minimal, enterprise. Font: Work Sans."
                ),
            },
            "linkedin_article_image": {
                "dimensions": "1200x800",
                "use": "LinkedIn post / article image",
                "prompt": (
                    f"ROI Dashboard mockup for '{keyword}'. "
                    f"TOP: Title 'ROI Calculator — {keyword.title()}'. "
                    f"KPI cards: Investment $500K | Year 1 Benefits $2M | ROI 400% | "
                    f"Payback 3 months. BOTTOM: Bar chart showing ROI growth over 3 years "
                    f"(Yr1: 300%, Yr2: 600%, Yr3: 1200%). "
                    f"Style: Modern SaaS dashboard. Colors: {self.BRAND_COLORS['deep_black']} "
                    f"background, {self.BRAND_COLORS['light_green']} accent bars, "
                    f"{self.BRAND_COLORS['off_white']} text. Font: Work Sans."
                ),
            },
            "infographic": {
                "dimensions": "1080x1080",
                "use": "Data visualization / infographic",
                "prompt": (
                    f"Pie chart infographic: 'Why IT Projects Fail'. "
                    f"Segments: No Strategy 30% (red), Poor Change Mgmt 25% (orange), "
                    f"Wrong Vendor 20% (yellow), No Exec Support 15% (blue), "
                    f"No Risk Mgmt 10% (dark blue). "
                    f"Callout bubble: 'With professional consulting, failure risk drops to <5%'. "
                    f"Background: {self.BRAND_COLORS['off_white']}. "
                    f"Style: Clean, data-focused, enterprise. Font: Work Sans."
                ),
            },
            "landing_page_hero": {
                "dimensions": "1920x1080",
                "use": "Website landing page hero section",
                "prompt": (
                    f"Landing page hero for '{title}'. "
                    f"Background: Gradient from {self.BRAND_COLORS['deep_black']} to dark navy. "
                    f"Main heading in {self.BRAND_COLORS['off_white']}: '{title}'. "
                    f"Sub-heading: 'Transform Legacy Systems Into Competitive Advantages'. "
                    f"Right side: Diverse professional team in modern office, soft bokeh. "
                    f"Left side: Abstract cloud/network visualization with "
                    f"{self.BRAND_COLORS['light_green']} nodes. "
                    f"Generous white space. Style: Minimalist cinematography, editorial. "
                    f"Font: Work Sans SemiBold."
                ),
            },
        }

        return {
            "keyword": keyword,
            "title": title,
            "design_prompts": prompts,
            "brand_colors": self.BRAND_COLORS,
            "notes": "Execute each prompt in Nano Banana. Export as PNG. Approx 30 min per image.",
            "created_at": datetime.now().isoformat(),
        }


visual_designer = VisualDesigner()
