from typing import List,Dict
from sqlalchemy.orm import Session
from app.models.workspace import GuidelineClause,TerminologyEntry,ApprovedFact,Guideline
from app.models.draft import Draft,Finding,FindingSeverity,FindingStatus
from app.services.rules_engine import check_banned_terms,verify_finding
from app.services.ai_review import run_ai_review,verify_ai_findings

def run_full_review(draft:Draft,db:Session)->List[Finding]:
    db.query(Finding).filter(Finding.draft_id==draft.id).delete()
    db.commit()
    workspace_id=draft.workspace_id
    terminology=db.query(TerminologyEntry).filter(TerminologyEntry.workspace_id==workspace_id).all()
    rule_findings=check_banned_terms(draft.content,terminology)
    clauses=db.query(GuidelineClause).join(Guideline).filter(Guideline.workspace_id==workspace_id).all()
    clause_dicts=[{"id":c.id,"clause_number":c.clause_number,"text":c.text,"category":c.category} for c in clauses]
    clause_map={c.id:c.text for c in clauses}
    ai_raw=run_ai_review(draft.content,clause_dicts)
    ai_verified=verify_ai_findings(ai_raw,draft.content,clause_map)
    all_findings=[]
    for rf in rule_findings:
        f=Finding(
            draft_id=draft.id,
            category=rf['category'],
            severity=FindingSeverity(rf['severity']),
            location_start=rf.get('location_start'),
            location_end=rf.get('location_end'),
            quoted_content=rf['quoted_content'],
            reason=rf['reason'],
            suggested_fix=rf.get('suggested_fix'),
            finding_source='rule',
            status=FindingStatus.open,
        )
        db.add(f)
        all_findings.append(f)
    for af in ai_verified:
        clause_id=af.get('clause_id')
        clause=clause_map.get(clause_id,'') if clause_id else ''
        severity_str=af.get('severity','minor')
        try:
            sev=FindingSeverity(severity_str)
        except Exception:
            sev=FindingSeverity.minor
        f=Finding(
            draft_id=draft.id,
            category=af.get('category','general'),
            severity=sev,
            location_start=af.get('location_start'),
            location_end=af.get('location_end'),
            quoted_content=af.get('quoted_content',''),
            reason=af.get('reason',''),
            cited_clause_id=clause_id,
            cited_clause_text=clause,
            suggested_fix=af.get('suggested_fix'),
            finding_source='ai',
            status=FindingStatus.open,
        )
        db.add(f)
        all_findings.append(f)
        if clause_id:
            cl=db.query(GuidelineClause).filter(GuidelineClause.id==clause_id).first()
            if cl:
                cl.violation_count=(cl.violation_count or 0)+1
    db.commit()
    for f in all_findings:
        db.refresh(f)
    return all_findings

def get_insights(workspace_id:int,db:Session)->dict:
    from sqlalchemy import func
    from app.models.draft import Draft,Finding
    drafts=db.query(Draft).filter(Draft.workspace_id==workspace_id).all()
    draft_ids=[d.id for d in drafts]
    if not draft_ids:
        return {"total_drafts":0,"total_findings":0,"by_category":{},"by_severity":{},"unclear_clauses":[]}
    findings=db.query(Finding).filter(Finding.draft_id.in_(draft_ids)).all()
    by_cat={}
    by_sev={}
    for f in findings:
        by_cat[f.category]=by_cat.get(f.category,0)+1
        by_sev[f.severity.value]=by_sev.get(f.severity.value,0)+1
    clauses=db.query(GuidelineClause).join(Guideline).filter(Guideline.workspace_id==workspace_id).order_by((GuidelineClause.dispute_count+GuidelineClause.dismissed_count).desc()).limit(5).all()
    unclear=[{"id":c.id,"clause_number":c.clause_number,"text":c.text,"dispute_count":c.dispute_count,"dismissed_count":c.dismissed_count,"violation_count":c.violation_count} for c in clauses]
    return {
        "total_drafts":len(drafts),
        "total_findings":len(findings),
        "by_category":by_cat,
        "by_severity":by_sev,
        "unclear_clauses":unclear,
    }

