"""
Skill #6: Lead Qualifier
Scores incoming leads 0-10, determines qualification stage,
checks ICP fit, and recommends next actions.
Designed to work with Presto, Maverick, and Sales Navigator data.
"""

from datetime import datetime
from typing import Dict, List


# ICP definition for Heinrich Co.
ICP_CRITERIA = {
    "target_titles": [
        "ceo", "cto", "cio", "coo", "cfo", "vp", "vice president",
        "director", "head of", "chief", "founder", "co-founder",
        "managing director", "partner", "general manager",
    ],
    "target_industries": [
        "technology", "financial services", "healthcare", "manufacturing",
        "consulting", "telecommunications", "energy", "retail", "logistics",
    ],
    "company_size_min_revenue": 1_000_000,  # $1M minimum
    "company_size_ideal_revenue": 1_000_000_000,  # $1B ideal
    "regions": ["EMEA", "LATAM", "North America", "APAC"],
}


ENGAGEMENT_SIGNALS = {
    "page_view": {"value": 1, "stage": "Awareness"},
    "time_on_page_3min": {"value": 2, "stage": "Interest"},
    "multiple_pages": {"value": 3, "stage": "Interest"},
    "blog_cta_click": {"value": 5, "stage": "Consideration"},
    "social_click": {"value": 3, "stage": "Interest"},
    "social_comment": {"value": 2, "stage": "Interest"},
    "social_share": {"value": 3, "stage": "Interest"},
    "social_dm": {"value": 8, "stage": "Consideration"},
    "form_submission": {"value": 10, "stage": "Decision"},
    "contact_form": {"value": 10, "stage": "Decision"},
    "phone_call": {"value": 15, "stage": "Decision"},
    "calendar_booking": {"value": 15, "stage": "Decision"},
    "download": {"value": 6, "stage": "Consideration"},
    "email_open": {"value": 1, "stage": "Awareness"},
    "email_click": {"value": 4, "stage": "Interest"},
    "demo_request": {"value": 15, "stage": "Decision"},
}


class LeadQualifier:

    def qualify_lead(self, lead: Dict) -> Dict:
        """
        Score and qualify a single lead.
        Expects dict with keys like: name, company, title, email, source, notes, buying_signal_score.
        Returns enriched lead dict with score, stage, icp_fit, and recommended actions.
        """
        title = (lead.get("title") or lead.get("notes") or "").lower()
        company = (lead.get("company") or "").lower()
        source = (lead.get("source") or "").lower()
        existing_score = lead.get("buying_signal_score", 0)
        if isinstance(existing_score, str):
            try:
                existing_score = int(existing_score)
            except ValueError:
                existing_score = 0

        # --- ICP Fit ---
        title_match = any(t in title for t in ICP_CRITERIA["target_titles"])
        industry_match = any(i in company for i in ICP_CRITERIA["target_industries"])
        icp_score = 0
        if title_match:
            icp_score += 4
        if industry_match:
            icp_score += 3
        if source in ("presto", "maverick", "sales navigator"):
            icp_score += 2
        icp_fit = min(10, icp_score)

        # --- Combined score ---
        combined = min(10, round((existing_score * 0.5) + (icp_fit * 0.5)))

        # --- Stage ---
        if combined >= 8:
            stage = "Decision"
            actions = ["Immediate sales outreach", "Send personalized proposal", "Book discovery call"]
        elif combined >= 5:
            stage = "Consideration"
            actions = ["Add to nurture email sequence", "Send relevant case study", "Invite to webinar"]
        elif combined >= 3:
            stage = "Interest"
            actions = ["Add to marketing automation", "Send educational content", "Track engagement"]
        else:
            stage = "Awareness"
            actions = ["Add to newsletter", "Set retargeting", "Monitor activity"]

        return {
            "lead_id": lead.get("lead_id") or lead.get("name", "unknown"),
            "name": lead.get("name", ""),
            "company": lead.get("company", ""),
            "title": lead.get("title", title),
            "email": lead.get("email", ""),
            "source": lead.get("source", ""),
            "original_score": existing_score,
            "icp_fit": icp_fit,
            "combined_score": combined,
            "stage": stage,
            "title_match": title_match,
            "industry_match": industry_match,
            "recommended_actions": actions,
            "qualified_at": datetime.now().isoformat(),
        }

    def qualify_batch(self, leads: List[Dict]) -> Dict:
        """Qualify a batch of leads and return summary statistics."""
        results = [self.qualify_lead(lead) for lead in leads]
        hot = [r for r in results if r["combined_score"] >= 8]
        warm = [r for r in results if 5 <= r["combined_score"] < 8]
        cold = [r for r in results if r["combined_score"] < 5]

        return {
            "total": len(results),
            "hot_leads": len(hot),
            "warm_leads": len(warm),
            "cold_leads": len(cold),
            "leads": results,
            "top_10": sorted(results, key=lambda x: x["combined_score"], reverse=True)[:10],
            "summary": f"{len(hot)} hot, {len(warm)} warm, {len(cold)} cold out of {len(results)} total",
            "processed_at": datetime.now().isoformat(),
        }

    def track_engagement(self, lead_id: str, event_type: str) -> Dict:
        """Record an engagement event and return the signal value."""
        signal = ENGAGEMENT_SIGNALS.get(event_type, {"value": 0, "stage": "Unknown"})
        return {
            "lead_id": lead_id,
            "event": event_type,
            "signal_value": signal["value"],
            "stage": signal["stage"],
            "timestamp": datetime.now().isoformat(),
        }


lead_qualifier = LeadQualifier()
