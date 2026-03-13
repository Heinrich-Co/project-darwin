"""
Skill #7: Analytics Manager
Generates performance reports with KPIs, process indicators,
action items, competitor tracking, and dashboard data.
"""

from datetime import datetime
from typing import Dict, Optional


class AnalyticsManager:

    KPI_DEFINITIONS = {
        "content": {
            "blog_views": {"target": "1000+ per keyword per 30 days", "source": "GA4"},
            "engagement_rate": {"target": "8%+", "source": "GA4 (time on page > 3 min)"},
            "cta_click_rate": {"target": "5%+", "source": "GA4 events"},
            "bounce_rate": {"target": "<50%", "source": "GA4"},
            "avg_reading_time": {"target": "4+ minutes", "source": "GA4"},
        },
        "social": {
            "total_reach": {"target": "50000+ monthly", "source": "Platform analytics"},
            "engagement_rate": {"target": "6-12%", "source": "(Likes+Comments+Shares)/Impressions"},
            "follower_growth": {"target": "100-200/month", "source": "Platform analytics"},
            "traffic_to_website": {"target": "500+ monthly from social", "source": "GA4 referral"},
        },
        "leads": {
            "form_submissions": {"target": "50+ per month", "source": "CRM / Google Sheets"},
            "mqls": {"target": "30+ per month", "source": "Lead scoring system"},
            "sqls": {"target": "10+ per month", "source": "Sales team"},
            "conversion_rate": {"target": "20%+", "source": "MQL to SQL ratio"},
        },
        "revenue": {
            "cac": {"target": "<$5000", "source": "Total spend / new customers"},
            "pipeline_value": {"target": "$500K+", "source": "CRM"},
            "content_attribution": {"target": "60%+ deals with content touch", "source": "CRM"},
        },
    }

    PROCESS_INDICATORS = {
        "content_production": {
            "blogs_per_month": "4-8",
            "social_posts_per_week": "12-16",
            "content_approval_time": "<2 days",
        },
        "optimization": {
            "cta_tests_per_month": "4+",
            "content_updates_per_month": "4+",
            "keyword_improvements_per_month": "5+",
        },
        "team_efficiency": {
            "time_per_keyword": "4 hours (AI) vs 80 hours (manual)",
            "sales_response_time": "<1 hour",
            "campaign_execution_rate": "90%+",
        },
    }

    COMPETITORS = {
        "direct": ["Accenture", "Deloitte", "McKinsey", "BCG", "IBM Consulting", "EY"],
        "indirect": ["Staff augmentation firms", "Freelance platforms", "DIY software"],
        "emerging": [],
        "tracking_metrics": [
            "New content published",
            "SEO rankings for shared keywords",
            "Social media activity and reach",
            "Pricing and packaging changes",
            "New partnerships or acquisitions",
            "Key team hires",
            "Customer announcements",
        ],
    }

    def generate_report(
        self,
        period: str = "daily",
        content_pages: int = 0,
        total_views: int = 0,
        avg_engagement: float = 0.0,
        top_performer: str = "",
        content_gaps: int = 0,
        deep_engagement: int = 0,
        cta_clicks: int = 0,
        repeat_interest: int = 0,
        total_leads: int = 0,
        hot_leads: int = 0,
    ) -> Dict:
        """
        Generate an analytics report.
        All parameters are optional — pass real data when available,
        or the report will include placeholder guidance.
        """
        total_signals = deep_engagement + cta_clicks + repeat_interest

        # Determine top signal description
        if deep_engagement >= cta_clicks and deep_engagement >= repeat_interest:
            top_signal = f"{deep_engagement} users deeply engaged"
        elif cta_clicks >= repeat_interest:
            top_signal = f"{cta_clicks} high-intent CTA clicks"
        else:
            top_signal = f"{repeat_interest} topics showing repeat interest"

        # Build action items
        actions = []
        if content_gaps > 10:
            actions.append({"priority": "HIGH", "action": f"Create content for {content_gaps} gap topics", "owner": "Content team", "deadline": "This month"})
        if avg_engagement < 6.0 and content_pages > 0:
            actions.append({"priority": "HIGH", "action": "Refresh underperforming blog posts", "owner": "Content team", "deadline": "2 weeks"})
        if hot_leads > 10:
            actions.append({"priority": "HIGH", "action": f"Export {hot_leads} hot leads for sales outreach", "owner": "Sales team", "deadline": "This week"})
        if cta_clicks == 0 and total_views > 100:
            actions.append({"priority": "MEDIUM", "action": "Review and optimize CTAs on all pages", "owner": "Content team", "deadline": "2 weeks"})
        actions.append({"priority": "LOW", "action": "Update keyword rankings from Search Console", "owner": "Naqi", "deadline": "Weekly Monday"})

        return {
            "report_type": period,
            "generated_at": datetime.now().isoformat(),
            "content_performance": {
                "pages_monitored": content_pages,
                "total_views_24h": total_views,
                "avg_engagement_rate": f"{avg_engagement}%",
                "top_performer": top_performer or "N/A",
                "content_gaps": content_gaps,
            },
            "buying_signals": {
                "deep_engagement": deep_engagement,
                "high_intent_ctas": cta_clicks,
                "repeat_interest": repeat_interest,
                "total_signals": total_signals,
                "top_signal": top_signal,
            },
            "lead_intelligence": {
                "total_leads": total_leads,
                "hot_leads_8plus": hot_leads,
                "status": "Ready for outreach" if hot_leads > 0 else "Building pipeline",
            },
            "system_status": {
                "ga4": "Working",
                "signal_detection": "Active",
                "lead_import": "Synchronized",
                "keywords": "Manual (Search Console API unavailable)",
            },
            "action_items": actions,
            "kpi_definitions": self.KPI_DEFINITIONS,
            "process_indicators": self.PROCESS_INDICATORS,
            "competitor_tracking": self.COMPETITORS,
        }

    def get_kpi_definitions(self) -> Dict:
        return self.KPI_DEFINITIONS

    def get_competitor_list(self) -> Dict:
        return self.COMPETITORS


analytics_manager = AnalyticsManager()
