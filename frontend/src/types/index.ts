export type UserRole='creator'|'manager'|'reviewer'|'admin'
export interface User{id:number;email:string;full_name:string;role:UserRole;workspace_id:number|null;is_active:boolean;created_at:string}
export interface Workspace{id:number;name:string;description:string|null;created_at:string}
export interface GuidelineClause{id:number;clause_number:string;text:string;category:string|null;dispute_count:number;dismissed_count:number;violation_count:number}
export interface Guideline{id:number;title:string;source_filename:string|null;created_at:string;clauses:GuidelineClause[]}
export interface TerminologyEntry{id:number;term:string;entry_type:string;preferred_alternative:string|null;reason:string|null}
export interface ApprovedFact{id:number;claim:string;source:string|null;expires_at:string|null;created_at:string}
export type DraftStatus='draft'|'under_review'|'pending_approval'|'approved'|'rejected'
export type FindingSeverity='critical'|'major'|'minor'|'info'
export type FindingStatus='open'|'accepted'|'disputed'|'dismissed'
export interface Finding{id:number;draft_id:number;category:string;severity:FindingSeverity;location_start:number|null;location_end:number|null;quoted_content:string;reason:string;cited_clause_id:number|null;cited_clause_text:string|null;suggested_fix:string|null;status:FindingStatus;dispute_reason:string|null;finding_source:string;created_at:string}
export interface Comment{id:number;draft_id:number;author_id:number;text:string;created_at:string}
export interface Approval{id:number;draft_id:number;approver_id:number;decision:string;note:string|null;created_at:string}
export interface Draft{id:number;title:string;content:string;channel:string|null;purpose:string|null;status:DraftStatus;creator_id:number;workspace_id:number;created_at:string;updated_at:string|null;findings?:Finding[];comments?:Comment[];approvals?:Approval[]}
export interface Insights{total_drafts:number;total_findings:number;by_category:Record<string,number>;by_severity:Record<string,number>;unclear_clauses:Array<{id:number;clause_number:string;text:string;dispute_count:number;dismissed_count:number;violation_count:number}>}

