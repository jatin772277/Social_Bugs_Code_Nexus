import re
from typing import List,Tuple
from sqlalchemy.orm import Session
from app.models.workspace import GuidelineClause,TerminologyEntry

CLAUSE_PATTERN=re.compile(r'(?m)^(\d+(?:\.\d+)*\.?\s+.{10,}?)(?=\n\d+(?:\.\d+)*\.?\s+|\Z)',re.DOTALL)
SECTION_PATTERN=re.compile(r'(?m)^([A-Z][A-Z\s]{3,})\n(.+?)(?=\n[A-Z][A-Z\s]{3,}\n|\Z)',re.DOTALL)

def split_into_clauses(text:str)->List[Tuple[str,str]]:
    clauses=[]
    matches=CLAUSE_PATTERN.findall(text)
    if matches and len(matches)>2:
        for idx,m in enumerate(matches,1):
            num_match=re.match(r'^(\d+(?:\.\d+)*\.?)',m.strip())
            num=num_match.group(1) if num_match else str(idx)
            body=re.sub(r'^'+re.escape(num)+r'\s*','',m.strip()).strip()
            if body:
                clauses.append((num,body))
    if not clauses:
        lines=[l.strip() for l in text.split('\n') if l.strip()]
        for idx,line in enumerate(lines,1):
            clauses.append((str(idx),line))
    return clauses

def infer_category(text:str)->str:
    t=text.lower()
    if any(w in t for w in ['tone','voice','formal','casual','friendly']):
        return 'tone'
    if any(w in t for w in ['term','word','phrase','call','refer','name','brand']):
        return 'terminology'
    if any(w in t for w in ['claim','fact','statistic','data','source','evidence']):
        return 'claims'
    if any(w in t for w in ['image','logo','colour','color','visual','icon','photo']):
        return 'visual'
    if any(w in t for w in ['message','value','promise','mission','story']):
        return 'messaging'
    if any(w in t for w in ['access','contrast','alt','screen reader','keyboard']):
        return 'accessibility'
    return 'general'

def check_banned_terms(content:str,terminology:List[TerminologyEntry])->List[dict]:
    findings=[]
    for entry in terminology:
        if entry.entry_type!='banned':
            continue
        idx=content.lower().find(entry.term.lower())
        if idx!=-1:
            end=idx+len(entry.term)
            findings.append({
                'category':'terminology',
                'severity':'major',
                'location_start':idx,
                'location_end':end,
                'quoted_content':content[idx:end],
                'reason':f'The term "{entry.term}" is banned.{(" Use: "+entry.preferred_alternative) if entry.preferred_alternative else ""}',
                'suggested_fix':entry.preferred_alternative or '',
                'finding_source':'rule',
                'rule_match_term':entry.term,
            })
    return findings

def verify_finding(finding:dict,content:str,clause_text:str)->bool:
    qc=finding.get('quoted_content','').strip().lower()
    if not qc or qc not in content.lower():
        return False
    if clause_text:
        qcl=finding.get('cited_clause_quote','').strip().lower()
        if qcl and qcl not in clause_text.lower():
            return False
    return True

