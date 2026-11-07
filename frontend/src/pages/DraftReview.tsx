import {useEffect,useState} from 'react'
import {useParams,useNavigate} from 'react-router-dom'
import api from '../lib/api'
import toast from 'react-hot-toast'
import {useAuthStore} from '../store/auth'
import {Shield,ArrowLeft,PlayCircle,CheckCircle,XCircle,AlertTriangle,MessageSquare,ThumbsDown,Info,Loader2,Send,Lock,Unlock} from 'lucide-react'
import type {Draft,Finding,Comment,Approval} from '../types'
import {formatDateTime,statusColor} from '../lib/utils'
import {cn} from '../lib/utils'

function FindingCard({f,onAction,canAct}:{f:Finding;onAction:(id:number,action:string,reason?:string)=>void;canAct:boolean}){
  const [disputing,setDisputing]=useState(false)
  const [reason,setReason]=useState('')
  const sevCls={critical:'badge-critical',major:'badge-major',minor:'badge-minor',info:'badge-info'}
  const statusCls={open:'badge-open',accepted:'badge-accepted',disputed:'badge-disputed',dismissed:'badge-dismissed'}
  return(
    <div className={cn('border rounded-xl p-4 mb-3 transition-colors',f.status==='accepted'?'border-green-200 bg-green-50':f.status==='dismissed'?'border-gray-200 bg-gray-50 opacity-60':f.status==='disputed'?'border-purple-200 bg-purple-50':'border-orange-200 bg-orange-50')}>
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex flex-wrap gap-2">
          <span className={sevCls[f.severity]}>{f.severity}</span>
          <span className="badge bg-gray-100 text-gray-700 capitalize">{f.category}</span>
          <span className={statusCls[f.status]}>{f.status}</span>
          <span className="badge bg-white text-gray-500 border border-gray-200">{f.finding_source==='rule'?'Rule':'AI'}</span>
        </div>
      </div>
      <div className="mb-2">
        <p className="text-sm font-medium text-gray-900 mb-1">Found in draft:</p>
        <blockquote className="text-sm text-gray-700 bg-white rounded-lg px-3 py-2 border-l-4 border-orange-400 italic">"{f.quoted_content}"</blockquote>
      </div>
      <p className="text-sm text-gray-700 mb-2"><span className="font-medium">Issue:</span> {f.reason}</p>
      {f.cited_clause_text&&(
        <div className="mb-2 p-2 bg-blue-50 rounded-lg border border-blue-100">
          <p className="text-xs text-blue-600 font-medium mb-1">Cited guideline clause</p>
          <p className="text-xs text-blue-800">"{f.cited_clause_text}"</p>
        </div>
      )}
      {f.suggested_fix&&(
        <div className="mb-3 p-2 bg-white rounded-lg border border-green-200">
          <p className="text-xs text-green-700 font-medium mb-1">Suggested fix</p>
          <p className="text-sm text-gray-800">"{f.suggested_fix}"</p>
        </div>
      )}
      {f.dispute_reason&&<p className="text-xs text-purple-700 mb-2"><span className="font-medium">Dispute reason:</span> {f.dispute_reason}</p>}
      {canAct&&f.status==='open'&&(
        <div className="flex gap-2 mt-2">
          <button onClick={()=>onAction(f.id,'accept')} className="btn-primary text-xs py-1 px-3 bg-green-600 hover:bg-green-700"><CheckCircle className="w-3 h-3"/>Accept</button>
          <button onClick={()=>setDisputing(!disputing)} className="btn-secondary text-xs py-1 px-3 text-purple-700 border-purple-300"><AlertTriangle className="w-3 h-3"/>Dispute</button>
          <button onClick={()=>onAction(f.id,'dismiss')} className="btn-ghost text-xs py-1 px-3 text-gray-500"><XCircle className="w-3 h-3"/>Dismiss</button>
        </div>
      )}
      {disputing&&f.status==='open'&&(
        <div className="mt-3">
          <textarea value={reason} onChange={e=>setReason(e.target.value)} rows={2} className="input text-sm resize-none" placeholder="Why do you disagree with this finding?"/>
          <div className="flex gap-2 mt-2">
            <button onClick={()=>{onAction(f.id,'dispute',reason);setDisputing(false)}} className="btn-primary text-xs py-1 px-3 bg-purple-600 hover:bg-purple-700">Submit Dispute</button>
            <button onClick={()=>setDisputing(false)} className="btn-ghost text-xs py-1 px-2">Cancel</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default function DraftReview(){
  const {id}=useParams<{id:string}>()
  const nav=useNavigate()
  const {user}=useAuthStore()
  const [draft,setDraft]=useState<Draft|null>(null)
  const [reviewing,setReviewing]=useState(false)
  const [comment,setComment]=useState('')
  const [approveNote,setApproveNote]=useState('')
  const [showApprove,setShowApprove]=useState(false)
  const [loading,setLoading]=useState(true)
  useEffect(()=>{
    if(!id) return
    api.get(`/drafts/${id}`).then(r=>setDraft(r.data)).finally(()=>setLoading(false))
  },[id])
  const runReview=async()=>{
    if(!id) return
    setReviewing(true)
    try{
      const r=await api.post(`/drafts/${id}/review`)
      toast.success(`Review complete — ${r.data.length} finding(s)`)
      const dr=await api.get(`/drafts/${id}`)
      setDraft(dr.data)
    }catch(e:any){
      toast.error(e.response?.data?.detail||'Review failed')
    }finally{setReviewing(false)}
  }
  const actOnFinding=async(fid:number,action:string,dispute_reason?:string)=>{
    try{
      const r=await api.patch(`/drafts/${id}/findings/${fid}`,{action,dispute_reason})
      setDraft(prev=>prev?{...prev,findings:prev.findings?.map(f=>f.id===fid?r.data:f)}:prev)
      toast.success(`Finding ${action}ed`)
    }catch(e:any){toast.error('Failed')}
  }
  const addComment=async()=>{
    if(!comment.trim()) return
    try{
      const r=await api.post(`/drafts/${id}/comments`,{text:comment})
      setDraft(prev=>prev?{...prev,comments:[...(prev.comments||[]),r.data]}:prev)
      setComment('')
    }catch(e:any){toast.error('Failed')}
  }
  const approve=async(decision:string)=>{
    try{
      await api.post(`/drafts/${id}/approve`,{decision,note:approveNote||null})
      toast.success(`Draft ${decision}`)
      setShowApprove(false)
      const dr=await api.get(`/drafts/${id}`)
      setDraft(dr.data)
    }catch(e:any){toast.error(e.response?.data?.detail||'Failed')}
  }
  if(loading) return <div className="min-h-screen flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-brand-600"/></div>
  if(!draft) return <div className="min-h-screen flex items-center justify-center text-gray-400">Draft not found</div>
  const canAct=user?.id===draft.creator_id||user?.role==='admin'
  const canApprove=user?.role==='manager'||user?.role==='reviewer'||user?.role==='admin'
  const findings=draft.findings||[]
  const open=findings.filter(f=>f.status==='open')
  const accepted=findings.filter(f=>f.status==='accepted')
  const disputed=findings.filter(f=>f.status==='disputed')
  const dismissed=findings.filter(f=>f.status==='dismissed')
  return(
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button onClick={()=>nav(-1)} className="btn-ghost p-2"><ArrowLeft className="w-4 h-4"/></button>
            <Shield className="w-6 h-6 text-brand-600"/>
            <span className="font-medium text-gray-900 truncate max-w-xs">{draft.title}</span>
            <span className={`text-xs px-2 py-1 rounded-full font-medium ${statusColor(draft.status)}`}>{draft.status.replace('_',' ')}</span>
          </div>
          <div className="flex items-center gap-3">
            {canApprove&&draft.status==='pending_approval'&&!showApprove&&(
              <button onClick={()=>setShowApprove(true)} className="btn-primary"><Lock className="w-4 h-4"/>Review Approval</button>
            )}
            <button onClick={runReview} disabled={reviewing} className="btn-primary">
              {reviewing?<><Loader2 className="w-4 h-4 animate-spin"/>Reviewing…</>:<><PlayCircle className="w-4 h-4"/>Run Review</>}
            </button>
          </div>
        </div>
      </nav>
      {showApprove&&(
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md">
            <h3 className="font-bold text-gray-900 text-lg mb-4">Approval Decision</h3>
            <textarea value={approveNote} onChange={e=>setApproveNote(e.target.value)} rows={3} className="input resize-none mb-4" placeholder="Note or feedback for the creator (optional)"/>
            <div className="flex gap-3">
              <button onClick={()=>approve('approved')} className="btn-primary flex-1 justify-center bg-green-600 hover:bg-green-700"><CheckCircle className="w-4 h-4"/>Approve</button>
              <button onClick={()=>approve('rejected')} className="btn-danger flex-1 justify-center"><XCircle className="w-4 h-4"/>Reject</button>
              <button onClick={()=>setShowApprove(false)} className="btn-secondary">Cancel</button>
            </div>
          </div>
        </div>
      )}
      <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 xl:grid-cols-5 gap-8">
        <div className="xl:col-span-2">
          <div className="card mb-4">
            <h2 className="font-semibold text-gray-900 mb-1">Draft Content</h2>
            {draft.channel&&<p className="text-xs text-gray-400 mb-3">Channel: {draft.channel.replace('_',' ')}</p>}
            {draft.purpose&&<p className="text-xs text-brand-600 mb-3">Purpose: {draft.purpose}</p>}
            <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-800 whitespace-pre-wrap leading-relaxed max-h-[60vh] overflow-y-auto">{draft.content}</div>
          </div>
          <div className="card">
            <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2"><MessageSquare className="w-4 h-4"/>Comments ({(draft.comments||[]).length})</h2>
            <div className="space-y-3 mb-4 max-h-48 overflow-y-auto">
              {(draft.comments||[]).map(c=>(
                <div key={c.id} className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-400 mb-1">User #{c.author_id} · {formatDateTime(c.created_at)}</p>
                  <p className="text-sm text-gray-800">{c.text}</p>
                </div>
              ))}
              {(draft.comments||[]).length===0&&<p className="text-sm text-gray-400">No comments yet</p>}
            </div>
            <div className="flex gap-2">
              <input value={comment} onChange={e=>setComment(e.target.value)} onKeyDown={e=>e.key==='Enter'&&addComment()} className="input text-sm flex-1" placeholder="Add a comment…"/>
              <button onClick={addComment} className="btn-primary px-3"><Send className="w-4 h-4"/></button>
            </div>
          </div>
          {(draft.approvals||[]).length>0&&(
            <div className="card mt-4">
              <h2 className="font-semibold text-gray-900 mb-3">Approvals</h2>
              {(draft.approvals||[]).map(a=>(
                <div key={a.id} className={cn('p-3 rounded-lg mb-2',a.decision==='approved'?'bg-green-50 border border-green-200':'bg-red-50 border border-red-200')}>
                  <div className="flex items-center gap-2 mb-1">
                    {a.decision==='approved'?<CheckCircle className="w-4 h-4 text-green-600"/>:<XCircle className="w-4 h-4 text-red-600"/>}
                    <span className={cn('text-sm font-medium',a.decision==='approved'?'text-green-800':'text-red-800')}>{a.decision}</span>
                    <span className="text-xs text-gray-400 ml-auto">{formatDateTime(a.created_at)}</span>
                  </div>
                  {a.note&&<p className="text-xs text-gray-600">{a.note}</p>}
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="xl:col-span-3">
          <div className="mb-4 flex items-center gap-4">
            <h2 className="font-semibold text-gray-900">Findings</h2>
            <div className="flex gap-2 text-xs">
              {open.length>0&&<span className="badge bg-orange-100 text-orange-800">{open.length} open</span>}
              {accepted.length>0&&<span className="badge-accepted">{accepted.length} accepted</span>}
              {disputed.length>0&&<span className="badge-disputed">{disputed.length} disputed</span>}
              {dismissed.length>0&&<span className="badge-dismissed">{dismissed.length} dismissed</span>}
              {findings.length===0&&<span className="text-gray-400">Run a review to see findings</span>}
            </div>
          </div>
          {findings.length===0&&(
            <div className="card text-center py-16 text-gray-400">
              <PlayCircle className="w-10 h-10 mx-auto mb-3 text-gray-300"/>
              <p className="font-medium">No findings yet</p>
              <p className="text-sm mt-1">Click "Run Review" to check this draft against your brand guidelines</p>
            </div>
          )}
          {findings.map(f=>(
            <FindingCard key={f.id} f={f} onAction={actOnFinding} canAct={canAct}/>
          ))}
        </div>
      </div>
    </div>
  )
}

