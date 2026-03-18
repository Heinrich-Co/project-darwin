# Project Darwin — Claude Cowork Instructions
 
## What This System Does
Project Darwin generates marketing content (briefs, blogs, social posts, design prompts, LinkedIn posts) using 8 AI skills. All generated content is saved in the Google Drive staging folder for review before publishing to Notion.
 
---
 
## Staging File Location (Google Drive)
 
All content files are stored in the shared company Google Drive folder:
 
**Folder path:** `Heinrich Co / Project Darwin / Staging`
 
When asked to show pending content, use the **Google Drive MCP** to read all JSON files from this folder where `"status": "pending_review"`.
 
**Do NOT wait for manual file uploads. Always read directly from Google Drive.**
 
---
 
## Notion Database IDs (Project Darwin Workspace)
 
When pushing approved content to Notion, use these exact database IDs:
 
- **Content Briefs** → Database ID: `326f9b0d23a880bf8e28ee4f9c1895a7`
- **Blog Posts** → Database ID: `326f9b0d23a880c781a7fbe1a53252a0`
- **Social Posts** → Database ID: `326f9b0d23a880a3a415c48f08993279`
- **Leads** → Database ID: `326f9b0d23a8804d87f7efa29e3a3378`
- **Analytics Reports** → Database ID: `326f9b0d23a8802582bbcea69847ae92`
 
All databases live under the **"Project Darwin"** page in the company Notion workspace.
 
---
 
## How to Review Content
 
### Show Pending Items
When asked to show pending content:
1. Use Google Drive MCP to read all `.json` files in `Heinrich Co / Project Darwin / Staging`
2. Filter for items where `"status": "pending_review"`
3. Present each item clearly with:
   - Type (brief / blog / social / designs / linkedin)
   - Keyword
   - Created date
   - A clean, readable summary of the content (NOT raw JSON)
 
### Show a Specific Item
When asked to review a specific item, read the full JSON file and present in readable format:
- For **briefs**: Show the keyword, 3 angles, blog structure, CTAs
- For **blogs**: Show the title, introduction, section headings, word count, conclusion
- For **social posts**: Show each post with platform, type, copy text, hashtags
- For **designs**: Show each design prompt with dimensions and use case
- For **linkedin posts**: Show the pillar, copy text, posting day, engagement playbook
 
### Approve Content
When told to approve:
1. Update the JSON file's `"status"` field to `"approved"` in Google Drive
2. Push the content to Notion using the Notion MCP:
   - **Briefs** → Create in "Content Briefs" database → ID: `326f9b0d23a880bf8e28ee4f9c1895a7`
   - **Blogs** → Create in "Blog Posts" database with full content in page body → ID: `326f9b0d23a880c781a7fbe1a53252a0`
   - **Social** → Create one entry per post in "Social Posts" database → ID: `326f9b0d23a880a3a415c48f08993279`
   - **LinkedIn** → Create in "Social Posts" database as LinkedIn type → ID: `326f9b0d23a880a3a415c48f08993279`
 
### Refine Content
When feedback is given (e.g., "make it more direct"):
1. Rewrite the content following the feedback
2. Maintain Heinrich Co. brand voice: corporate, direct, precise, executive
3. Show the updated version for approval before pushing to Notion
 
### Weekly Summary
When asked for a summary, read all files from the Drive staging folder and count by status:
- **pending_review**: Items waiting for review
- **approved**: Items approved and pushed to Notion
- **needs_revision**: Items sent back for changes
 
---
 
## Notion Database Structure
 
### Content Briefs
Columns: Name, Brief ID, Keyword, Status, Angles, Created
 
### Blog Posts
Columns: Name, Slug, Word Count, Status, Reading Time, Created
Page body: Full blog content with headings and sections
 
### Social Posts
Columns: Name, Platform (linkedin/instagram/youtube), Type (static/carousel/reel), Keyword, Copy, Status, Created
 
### Leads
Columns: Name, Company, Score, Stage, Source, Actions, Qualified
 
### Analytics Reports
Columns: Name, Period, Pages Monitored, Total Views, Total Signals, Hot Leads, Date
 
---
 
## Brand Voice Rules
- Tone: Corporate, Direct, Precise, Executive
- Never use: Amazing, Awesome, Revolutionary, Game-changing
- Never use: Salesy language, motivational clichés, excessive jargon
- Always: Be objective, factual, strategic, data-driven
- Target: C-suite executives, $10M+ revenue companies
