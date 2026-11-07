import json
import re
from typing import List,Optional
from google import genai
from google.genai import types
from app.core.config import get_settings

settings=get_settings()

def get_client()->genai.Client:
    return genai.Client(api_key=settings.gemini_api_key)

REVIEW_SYSTEM="""You are a strict brand compliance reviewer. You receive content and relevant brand guideline clauses.
You must identify only clear, definite violations where you can quote BOTH the exact text from the content AND the exact text from the clause.
Return JSON only. No markdown fences. No explanations outside JSON."""

REVIEW_PROMPT_TEMPLATE="""
Content to review:
\"\"\"
{content}
\"\"\"

Relevant brand guideline clauses:
{clauses}

For each violation you find, return an object with these exact keys:
- clause_id: the integer id of the clause (from the list above)
- clause_number: the clause number string
- quoted_content: exact substring from the content that violates the clause (copy it verbatim)
- cited_clause_quote: exact substring from the clause text that makes this a violation (copy it verbatim)
- category: one of [tone, terminology, claims, visual, messaging, accessibility, general]
- severity: one of [critical, major, minor, info]
- reason: one plain-language sentence explaining the violation
- suggested_fix: a corrected version of only the quoted_content, keeping the creator's intent

Return: {{"findings": [...]}}
If there are no violations, return: {{"findings": []}}
"""

def format_clauses_for_prompt(clauses:list)->str:
    lines=[]
    for c in clauses:
        lines.append(f'[id:{c["id"]}] Clause {c["clause_number"]}: {c["text"]}')
    return '\n'.join(lines)

def chunk_content(content:str,max_chars:int=3000)->List[str]:
    if len(content)<=max_chars:
        return [content]
    chunks=[]
    start=0
    while start<len(content):
        end=min(start+max_chars,len(content))
        last_period=content.rfind('.',start,end)
        if last_period>start+max_chars//2:
            end=last_period+1
        chunks.append(content[start:end])
        start=end
    return chunks

def run_ai_review(content:str,clauses:list)->List[dict]:
    if not settings.gemini_api_key or not clauses:
        return []
    client=get_client()
    all_findings=[]
    chunks=chunk_content(content)
    clauses_text=format_clauses_for_prompt(clauses)
    for chunk in chunks:
        prompt=REVIEW_PROMPT_TEMPLATE.format(content=chunk,clauses=clauses_text)
        try:
            response=client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=REVIEW_SYSTEM,
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            raw=response.text.strip()
            raw=re.sub(r'^```(?:json)?\s*','',raw)
            raw=re.sub(r'\s*```$','',raw)
            data=json.loads(raw)
            findings=data.get('findings',[])
            if isinstance(findings,list):
                all_findings.extend(findings)
        except Exception:
            pass
    return all_findings

def verify_ai_findings(findings:list,content:str,clause_map:dict)->List[dict]:
    verified=[]
    for f in findings:
        qc=f.get('quoted_content','').strip()
        if not qc:
            continue
        if qc.lower() not in content.lower():
            continue
        clause_id=f.get('clause_id')
        if clause_id and clause_id in clause_map:
            clause_text=clause_map[clause_id]
            qcl=f.get('cited_clause_quote','').strip()
            if qcl and qcl.lower() not in clause_text.lower():
                continue
        idx=content.lower().find(qc.lower())
        f['location_start']=idx
        f['location_end']=idx+len(qc) if idx!=-1 else None
        verified.append(f)
    return verified

