import sys
sys.path.insert(0,'.')
from app.core.database import engine,SessionLocal
from app.models import Base,User,Workspace,Guideline,GuidelineClause,TerminologyEntry,ApprovedFact
from app.core.security import hash_password
from app.services.rules_engine import split_into_clauses,infer_category

SAMPLE_GUIDELINES="""1. Tone and Voice
Our brand voice is confident, clear and human. We avoid jargon, excessive formality and corporate clichés.
1.1 Use active voice. Write "We launched" not "The launch was completed by us".
1.2 Write at a reading level accessible to a general audience. Avoid technical terms unless you define them.
1.3 Be direct. Say what you mean in the fewest words that remain clear.
2. Terminology and Language
2.1 Always refer to our product as "CodeNexus". Never "code nexus", "CN" or "the platform" in external communications.
2.2 Avoid superlatives we cannot prove: best, world-leading, unmatched, revolutionary. Use accurate comparative claims with a cited source instead.
2.3 Do not use the following banned terms: synergy, leverage (as a verb), ecosystem (unless referring to software integrations), scalable solution, thought leader.
2.4 Preferred spelling: organisation (not organization), colour (not color), programme (not program) for non-software contexts.
3. Promotional Claims
3.1 Any statistic or percentage claim must include a citation in the form [Source, Year].
3.2 Do not describe pricing as "affordable" or "cheap". Use specific pricing information instead.
3.3 Any claim about uptime, reliability or performance must reference a published SLA document.
4. Visual and Brand Assets
4.1 The primary brand colour is Deep Blue (#0369a1). Do not substitute it with other blue shades in brand materials.
4.2 The CodeNexus logo must appear in its approved form. Do not stretch, recolour or add effects to the logo.
4.3 All images published on official channels must have an alt text description for accessibility.
5. Accessibility
5.1 Text on a coloured background must meet WCAG AA contrast ratio of at least 4.5:1 for normal text.
5.2 Every link must have descriptive anchor text. Do not use "click here" or "read more" as link text.
5.3 Abbreviations must be expanded on first use. Example: "Search Engine Optimisation (SEO)".
"""

def seed():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    ws=Workspace(name="Demo Brand Workspace",description="Sample workspace pre-loaded with brand guidelines")
    db.add(ws)
    db.commit()
    db.refresh(ws)
    admin=User(email="admin@codenexus.demo",full_name="Admin User",hashed_password=hash_password("admin123"),role="admin",workspace_id=ws.id)
    manager=User(email="manager@codenexus.demo",full_name="Brand Manager",hashed_password=hash_password("manager123"),role="manager",workspace_id=ws.id)
    creator=User(email="creator@codenexus.demo",full_name="Content Creator",hashed_password=hash_password("creator123"),role="creator",workspace_id=ws.id)
    reviewer=User(email="reviewer@codenexus.demo",full_name="Legal Reviewer",hashed_password=hash_password("reviewer123"),role="reviewer",workspace_id=ws.id)
    for u in [admin,manager,creator,reviewer]:
        db.add(u)
    db.commit()
    g=Guideline(workspace_id=ws.id,title="CodeNexus Brand Style Guide v2",raw_text=SAMPLE_GUIDELINES)
    db.add(g)
    db.commit()
    db.refresh(g)
    clauses=split_into_clauses(SAMPLE_GUIDELINES)
    for num,text in clauses:
        c=GuidelineClause(guideline_id=g.id,clause_number=num,text=text,category=infer_category(text))
        db.add(c)
    banned_terms=["synergy","leverage","ecosystem","scalable solution","thought leader","click here","read more","best","world-leading","unmatched","revolutionary","affordable","cheap"]
    for term in banned_terms:
        db.add(TerminologyEntry(workspace_id=ws.id,term=term,entry_type="banned",reason="Banned per CodeNexus terminology guidelines section 2.3"))
    db.add(TerminologyEntry(workspace_id=ws.id,term="CodeNexus",entry_type="preferred",reason="Official product name — always capitalise exactly as shown"))
    db.add(ApprovedFact(workspace_id=ws.id,claim="CodeNexus is built by Social Bugs team at IIIT Nagpur",source="Internal company record 2026"))
    db.add(ApprovedFact(workspace_id=ws.id,claim="CodeNexus supports text, Word, PDF and image content review",source="Product spec sheet v2, 2026"))
    db.commit()
    db.close()
    print("Seed complete.")
    print("Demo accounts:")
    print("  admin@codenexus.demo / admin123")
    print("  manager@codenexus.demo / manager123")
    print("  creator@codenexus.demo / creator123")
    print("  reviewer@codenexus.demo / reviewer123")

if __name__=='__main__':
    seed()

