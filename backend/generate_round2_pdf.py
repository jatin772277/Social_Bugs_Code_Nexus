import pymupdf
import sys

def build_pdf(out_path):
    doc=pymupdf.open()
    pages=[
        """Round 2 Build Report — Pre-Publication Brand Governance Platform
Team Name: Social Bugs | Hackathon: CodeNexus India 2026
Team Members: Jatin Baghel (Lead), Dushyant, Vishal Thombre, Ricky Mukherjee

1. Executive Summary of Round 2 Delivery
In Round 1, we proposed an evidence-grounded review desk sitting directly between content creation and public distribution. In Round 2, we have built and verified the complete core workflow end-to-end.

A content creator uploads or drafts text in their designated workspace, where rule-based engines and Google Gemini AI check the text against the organization's own approved guidelines, banned terms, and approved facts.

Every finding is evidence-locked: it isolates the exact offending quote in the text and matches it to a specific guideline clause or terminology policy. Creators can accept, dispute (with written justification), or dismiss findings. Brand managers and reviewers track these revisions and issue formal approval or rejection with notes before any content is cleared for publishing.

2. Key Features Shipped & Verified
- Multi-Role Authentication & Access Control: JWT-secured role model with distinct permissions for Content Creators, Brand Managers, Authorised Reviewers, and Workspace Admins.
- Workspace & Guideline Management: Automated clause segmentation from unstructured style guidelines into identifiable clauses with category tagging (tone, terminology, claims, visual, messaging, accessibility).
- Real-Time Terminology & Fact Engine: Strict rule-based checking for banned terminology, preferred wording substitutions, and approved factual claim citations.
- Grounded AI Review & Verification: Multi-clause grounding using Gemini with zero-hallucination verification dropping ungrounded flags.
- Human-In-The-Loop Interactive Desk: Split review interface where creators can accept suggested fixes, log structured disputes, or dismiss flags.
- Governance & Approval Queue: Comment discussions on drafts, structured approval/rejection decisions with auditor notes, and locked approved states.
- Analytics & Clarity Signals: Aggregated dashboard reporting recurring violations, severity distributions, and frequently disputed clauses.""",
        """3. Technology Stack & Implementation Details
- Frontend: React 18, TypeScript, Vite, Tailwind CSS, Lucide icons, React Router, Zustand for lightweight authenticated state management, and Axios.
- Backend: Python 3.11 with FastAPI, SQLAlchemy 2.0 ORM, and Pydantic v2 data models.
- AI Engine: Google Gemini API (gemini-3.8-flash) via google-genai SDK with low temperature and structured JSON mode.
- Security: Cryptographic bcrypt hashing for credentials and signed HS256 JWT tokens with role-based route guards.
- Database Architecture: Relational database architecture compatible with PostgreSQL and SQLite for portability.
- Deployment: Containerized multi-service Docker Compose setup with Nginx reverse proxy and healthchecks.

4. Technical Challenges Solved
- Eliminating Hallucinations via Verification: A common pitfall in automated LLM brand checks is false positives or fabricated citations. We implemented an evidence verification barrier: candidate AI findings are checked against the source guideline clause and raw submitted text before display.
- Deterministic Pre-Filtering: Fixed rule checks (banned phrases, exact keywords) run prior to any LLM prompt, guaranteeing immediate detection of policy violations at zero AI token cost.
- Clause Splitting Logic: Automatic regex segmentation converts arbitrary guideline documentation into individually referenceable clauses with dispute tracking counters.""",
        """5. What Changed From Round 1 Proposal
In Round 1, we planned to implement multi-modal image checking and Word/PDF layout parsing in the same initial phase. During implementation, we realized that an evidence verification mechanism and rock-solid human-in-the-loop review workflow were paramount to user trust.

We intentionally narrowed Round 2 to ship a battle-tested text review desk, guideline clause extraction, and approval queue, while cleanly scoping document formatting, PDF/Word binary parsing, and image color-contrast/alt-text rules into Round 3.

6. What Does Not Work Yet (Known Limitations)
- File Format Inputs: Native binary upload of PDF and DOCX files is currently parsed via plain text extraction rather than layout-preserved visual coordinates.
- Advanced Visual Media Auditing: Automatic extraction of color palettes from raster image uploads and WCAG pixel-level contrast analysis is scheduled for Round 3.
- External AI Masking: Automatic redaction of sensitive internal project codewords prior to model dispatch is architected but currently bypassed in local mode.

7. Commitments for Round 3
We commit to delivering the following three major improvements in Round 3:

1. Native Word, PDF & Image File Support: Direct parsing of DOCX, PDF, and image uploads with position-aware text highlights, image palette extraction, and WCAG AA contrast ratio validation.
2. Complete Role-Based Revision History with Side-by-Side Diff: Full versioning snapshots tracking every creator edit, showing reviewers an exact visual side-by-side diff against prior iterations.
3. Guideline Clarity Insights with AI Rewrite Engine: Active aggregation of disputed and dismissed clauses to detect ambiguous brand guidelines, automatically generating proposed rule rewrites for workspace administrators."""
    ]
    for content in pages:
        page=doc.new_page(width=595,height=842)
        rect=pymupdf.Rect(50,50,545,792)
        page.insert_textbox(rect,content,fontsize=10,fontname="helv")
    doc.save(out_path)
    doc.close()
    print("PDF generated:",out_path)

if __name__=="__main__":
    out="d:\\My Projects\\CodeNexus\\CodeNexus_Round2_SocialBugs.pdf"
    if len(sys.argv)>1:
        out=sys.argv[1]
    build_pdf(out)
