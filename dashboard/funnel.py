"""
Scale 4: Sales Funnel Dashboard Generator
Creates a live HTML dashboard showing the complete sales funnel,
content performance, and lead pipeline — embeddable in Notion.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

logger = logging.getLogger("dashboard.generator")


def generate_dashboard(data: Dict = None) -> str:
    """Generate a complete sales funnel dashboard as HTML.
    
    data should contain:
    - funnel: {invites, connected, messaged, responses, meetings, proposals, sales}
    - campaigns: [{name, invites, connected, responses, meetings}]
    - leads: {total, hot, warm, cold, by_source: {presto, maverick, ambassador, seo}}
    - content: {total, views, engagement, top_performer}
    - keywords: {processed, remaining, top_keyword}
    """
    if not data:
        data = _get_sample_data()

    funnel = data.get("funnel", {})
    campaigns = data.get("campaigns", [])
    leads = data.get("leads", {})
    content = data.get("content", {})
    keywords = data.get("keywords", {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Project Darwin — Sales Funnel Dashboard</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700&display=swap');
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Work Sans', sans-serif; background: #F2F2F2; color: #1B1D1E; }}
.dash {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
.header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }}
.logo {{ font-size: 24px; font-weight: 700; color: #1B1D1E; }}
.logo span {{ color: #CAD3AC; }}
.updated {{ font-size: 12px; color: #908A82; }}
.kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
.kpi {{ background: #fff; border-radius: 12px; padding: 20px; border: 1px solid #E8E5E0; }}
.kpi-label {{ font-size: 11px; font-weight: 600; color: #908A82; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
.kpi-value {{ font-size: 36px; font-weight: 700; color: #1B1D1E; line-height: 1; }}
.kpi-sub {{ font-size: 13px; color: #6F6B65; margin-top: 6px; }}
.kpi-tag {{ display: inline-block; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 10px; margin-top: 8px; }}
.tag-green {{ background: #E8EED9; color: #4a6020; }}
.tag-dark {{ background: #E0DDD8; color: #4F4C49; }}
.section {{ background: #fff; border-radius: 12px; border: 1px solid #E8E5E0; margin-bottom: 20px; overflow: hidden; }}
.section-head {{ padding: 16px 24px; border-bottom: 1px solid #F0EDE8; display: flex; justify-content: space-between; align-items: center; }}
.section-title {{ font-size: 16px; font-weight: 600; }}
.badge {{ background: #1B1D1E; color: #CAD3AC; font-size: 11px; font-weight: 600; padding: 4px 12px; border-radius: 12px; }}
.funnel {{ padding: 24px; display: flex; align-items: flex-end; gap: 12px; height: 280px; }}
.funnel-bar {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; }}
.bar {{ width: 100%; border-radius: 8px 8px 0 0; transition: height 0.5s; min-height: 4px; }}
.bar-label {{ font-size: 11px; color: #908A82; margin-top: 8px; text-align: center; font-weight: 500; }}
.bar-value {{ font-size: 20px; font-weight: 700; color: #1B1D1E; margin-bottom: 6px; }}
.bar-pct {{ font-size: 11px; color: #CAD3AC; font-weight: 600; margin-bottom: 4px; }}
.campaigns {{ padding: 16px 24px; }}
.camp-row {{ display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #F0EDE8; }}
.camp-row:last-child {{ border-bottom: none; }}
.camp-name {{ flex: 1; font-size: 14px; font-weight: 500; }}
.camp-stat {{ width: 80px; text-align: center; font-size: 13px; color: #6F6B65; }}
.camp-stat strong {{ color: #1B1D1E; display: block; font-size: 18px; }}
.pipeline {{ padding: 24px; display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; }}
.pipe-stage {{ text-align: center; padding: 12px 8px; border-radius: 8px; background: #FAFAF8; border: 1px solid #F0EDE8; }}
.pipe-count {{ font-size: 24px; font-weight: 700; color: #1B1D1E; }}
.pipe-label {{ font-size: 10px; color: #908A82; font-weight: 600; text-transform: uppercase; margin-top: 4px; }}
.source-grid {{ padding: 24px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
.source-card {{ text-align: center; padding: 16px; border-radius: 8px; border: 1px solid #E8E5E0; }}
.source-count {{ font-size: 28px; font-weight: 700; color: #1B1D1E; }}
.source-name {{ font-size: 12px; color: #908A82; font-weight: 500; margin-top: 4px; }}
.footer {{ text-align: center; padding: 20px; font-size: 12px; color: #C1B9AD; }}
@media (max-width: 768px) {{ .kpi-row {{ grid-template-columns: repeat(2, 1fr); }} .pipeline {{ grid-template-columns: repeat(4, 1fr); }} }}
</style>
</head>
<body>
<div class="dash">
  <div class="header">
    <div class="logo">Project <span>Darwin</span> Dashboard</div>
    <div class="updated">Last updated: {datetime.now().strftime("%B %d, %Y %H:%M")}</div>
  </div>

  <div class="kpi-row">
    <div class="kpi">
      <div class="kpi-label">Total Leads</div>
      <div class="kpi-value">{leads.get('total', 179)}</div>
      <div class="kpi-sub">Across all sources</div>
      <span class="kpi-tag tag-green">{leads.get('hot', 24)} hot leads</span>
    </div>
    <div class="kpi">
      <div class="kpi-label">Content Pieces</div>
      <div class="kpi-value">{content.get('total', 7)}</div>
      <div class="kpi-sub">{content.get('views', 14)} total views</div>
      <span class="kpi-tag tag-dark">{content.get('engagement', '0.0')}% engagement</span>
    </div>
    <div class="kpi">
      <div class="kpi-label">Keywords</div>
      <div class="kpi-value">{keywords.get('processed', 4)}/41</div>
      <div class="kpi-sub">Processed through pipeline</div>
      <span class="kpi-tag tag-green">{keywords.get('remaining', 37)} remaining</span>
    </div>
    <div class="kpi">
      <div class="kpi-label">Pipeline Value</div>
      <div class="kpi-value">$0</div>
      <div class="kpi-sub">Deals in progress</div>
      <span class="kpi-tag tag-dark">Building pipeline</span>
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div class="section-title">Sales Funnel — All Campaigns</div>
      <span class="badge">{len(campaigns)} campaigns</span>
    </div>
    <div class="funnel">
      {_render_funnel_bars(funnel)}
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div class="section-title">Campaign Breakdown</div>
    </div>
    <div class="campaigns">
      <div class="camp-row" style="border-bottom: 2px solid #E8E5E0;">
        <div class="camp-name" style="font-weight:600; color:#908A82; font-size:12px;">CAMPAIGN</div>
        <div class="camp-stat" style="font-size:11px; color:#908A82; font-weight:600;">INVITES</div>
        <div class="camp-stat" style="font-size:11px; color:#908A82; font-weight:600;">CONNECTED</div>
        <div class="camp-stat" style="font-size:11px; color:#908A82; font-weight:600;">RESPONSES</div>
        <div class="camp-stat" style="font-size:11px; color:#908A82; font-weight:600;">MEETINGS</div>
      </div>
      {''.join(_render_campaign_row(c) for c in campaigns)}
    </div>
  </div>

  <div class="section">
    <div class="section-head">
      <div class="section-title">Lead Pipeline</div>
      <span class="badge">{leads.get('total', 179)} leads</span>
    </div>
    <div class="source-grid">
      <div class="source-card">
        <div class="source-count">{leads.get('by_source', {}).get('presto', 179)}</div>
        <div class="source-name">Presto</div>
      </div>
      <div class="source-card">
        <div class="source-count">{leads.get('by_source', {}).get('maverick', 7)}</div>
        <div class="source-name">Maverick</div>
      </div>
      <div class="source-card">
        <div class="source-count">{leads.get('by_source', {}).get('ambassador', 0)}</div>
        <div class="source-name">Ambassadors</div>
      </div>
      <div class="source-card">
        <div class="source-count">{leads.get('by_source', {}).get('seo', 0)}</div>
        <div class="source-name">SEO / Noa</div>
      </div>
    </div>
  </div>

  <div class="footer">
    Project Darwin v4.1 — Heinrich Co. Intelligence System — Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}
  </div>
</div>
</body>
</html>"""
    return html


def _render_funnel_bars(funnel: Dict) -> str:
    stages = [
        ("Invites", funnel.get("invites", 301), "#E8638B"),
        ("Connected", funnel.get("connected", 121), "#E87B8B"),
        ("Messaged", funnel.get("messaged", 115), "#D4776E"),
        ("Responses", funnel.get("responses", 7), "#C49070"),
        ("Meetings", funnel.get("meetings", 1), "#D4C4A0"),
        ("Proposals", funnel.get("proposals", 0), "#B8A090"),
        ("Sales", funnel.get("sales", 0), "#D4A050"),
    ]
    max_val = max(s[1] for s in stages) or 1
    bars = ""
    for label, value, color in stages:
        height = max(4, int((value / max_val) * 200))
        pct = f"{(value / stages[0][1] * 100):.0f}%" if stages[0][1] > 0 else "0%"
        bars += f"""<div class="funnel-bar">
            <div class="bar-value">{value}</div>
            <div class="bar-pct">{pct}</div>
            <div class="bar" style="height:{height}px; background:{color};"></div>
            <div class="bar-label">{label}</div>
        </div>"""
    return bars


def _render_campaign_row(campaign: Dict) -> str:
    return f"""<div class="camp-row">
        <div class="camp-name">{campaign.get('name', '')}</div>
        <div class="camp-stat"><strong>{campaign.get('invites', 0)}</strong></div>
        <div class="camp-stat"><strong>{campaign.get('connected', 0)}</strong></div>
        <div class="camp-stat"><strong>{campaign.get('responses', 0)}</strong></div>
        <div class="camp-stat"><strong>{campaign.get('meetings', 0)}</strong></div>
    </div>"""


def _get_sample_data() -> Dict:
    """Real data from Fastdezine report + Presto + Project Darwin."""
    return {
        "funnel": {
            "invites": 301, "connected": 121, "messaged": 115,
            "responses": 7, "meetings": 1, "proposals": 0, "sales": 0,
        },
        "campaigns": [
            {"name": "AI Skill Builder Healthcare A", "invites": 121, "connected": 50, "responses": 4, "meetings": 0},
            {"name": "AI Skill Builder Healthcare B", "invites": 105, "connected": 42, "responses": 3, "meetings": 1},
            {"name": "AI Skill Builder Retail", "invites": 21, "connected": 14, "responses": 0, "meetings": 0},
            {"name": "AI Skill Builder Manufacturing", "invites": 54, "connected": 15, "responses": 0, "meetings": 0},
        ],
        "leads": {
            "total": 179, "hot": 24, "warm": 95, "cold": 60,
            "by_source": {"presto": 179, "maverick": 7, "ambassador": 0, "seo": 0},
        },
        "content": {"total": 7, "views": 14, "engagement": "0.0", "top_performer": "Foreword Blog"},
        "keywords": {"processed": 4, "remaining": 37, "top_keyword": "consulting services it"},
    }


def save_dashboard(output_path: str = None) -> str:
    """Generate and save dashboard HTML file."""
    html = generate_dashboard()
    path = output_path or str(Path(__file__).resolve().parent / "sales_funnel_dashboard.html")
    Path(path).write_text(html, encoding="utf-8")
    logger.info("Dashboard saved: %s", path)
    return path
