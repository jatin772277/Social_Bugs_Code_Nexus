import {useEffect,useState} from 'react'
import {useParams,useNavigate,Link} from 'react-router-dom'
import api from '../lib/api'
import toast from 'react-hot-toast'
import {Shield,ArrowLeft,Plus,Trash2,BookOpen,AlertTriangle,CheckCircle,BarChart3,FileText} from 'lucide-react'
import type {Workspace,Guideline,TerminologyEntry,ApprovedFact,Draft,Insights} from '../types'
import {formatDate,statusColor} from '../lib/utils'
import {useAuthStore} from '../store/auth'
type Tab='guidelines'|'terminology'|'facts'|'drafts'|'insights'
export default function WorkspacePage(){
  const {id}=useParams<{id:string}>()
  const nav=useNavigate()
  const {user}=useAuthStore()
  const [ws,setWs]=useState<Workspace|null>(null)
  const [tab,setTab]=useState<Tab>('drafts')
  const [guidelines,setGuidelines]=useState<Guideline[]>([])
  const [terms,setTerms]=useState<TerminologyEntry[]>([])
  const [facts,setFacts]=useState<ApprovedFact[]>([])
  const [drafts,setDrafts]=useState<Draft[]>([])
  const [insights,setInsights]=useState<Insights|null>(null)
  const [glText,setGlText]=useState('')
  const [glTitle,setGlTitle]=useState('')
  const [termTerm,setTermTerm]=useState('')
  const [termType,setTermType]=useState('banned')
  const [termAlt,setTermAlt]=useState('')
  const [factClaim,setFactClaim]=useState('')
  const [factSrc,setFactSrc]=useState('')
  useEffect(()=>{
    if(!id) return
    api.get(`/workspaces/${id}`).then(r=>setWs(r.data))
    api.get(`/workspaces/${id}/guidelines`).then(r=>setGuidelines(r.data))
    api.get(`/workspaces/${id}/terminology`).then(r=>setTerms(r.data))
    api.get(`/workspaces/${id}/facts`).then(r=>setFacts(r.data))
    api.get(`/drafts?workspace_id=${id}`).then(r=>setDrafts(r.data))
    api.get(`/insights/${id}`).then(r=>setInsights(r.data))
  },[id])
  const addGuideline=async()=>{
    if(!glTitle.trim()||!glText.trim()) return
    try{
      const fd=new FormData()
      fd.append('title',glTitle)
      fd.append('text_content',glText)
      const r=await api.post(`/workspaces/${id}/guidelines`,fd)
      setGuidelines(p=>[...p,r.data])
      setGlTitle('')
      setGlText('')
      toast.success(`Guideline imported — ${r.data.clauses.length} clauses extracted`)
    }catch(e:any){toast.error(e.response?.data?.detail||'Failed')}
  }
  const deleteGuideline=async(gid:number)=>{
    await api.delete(`/workspaces/${id}/guidelines/${gid}`)
    setGuidelines(p=>p.filter(g=>g.id!==gid))
    toast.success('Guideline removed')
  }
  const addTerm=async()=>{
    if(!termTerm.trim()) return
    try{
      const r=await api.post(`/workspaces/${id}/terminology`,{term:termTerm,entry_type:termType,preferred_alternative:termAlt||null})
      setTerms(p=>[...p,r.data])
      setTermTerm('')
      setTermAlt('')
      toast.success('Term added')
    }catch(e:any){toast.error(e.response?.data?.detail||'Failed')}
  }
  const addFact=async()=>{
    if(!factClaim.trim()) return
    try{
      const r=await api.post(`/workspaces/${id}/facts`,{claim:factClaim,source:factSrc||null})
      setFacts(p=>[...p,r.data])
      setFactClaim('')
      setFactSrc('')
      toast.success('Fact added')
    }catch(e:any){toast.error(e.response?.data?.detail||'Failed')}
  }
  const tabs:Array<{key:Tab;label:string;icon:any}>=[
    {key:'drafts',label:'Drafts',icon:FileText},
    {key:'guidelines',label:'Guidelines',icon:BookOpen},
    {key:'terminology',label:'Terminology',icon:AlertTriangle},
    {key:'facts',label:'Approved Facts',icon:CheckCircle},
    {key:'insights',label:'Insights',icon:BarChart3},
  ]
  return(
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <button onClick={()=>nav('/dashboard')} className="btn-ghost p-2"><ArrowLeft className="w-4 h-4"/></button>
          <Shield className="w-6 h-6 text-brand-600"/>
          <span className="font-bold text-gray-900">CodeNexus</span>
          <span className="text-gray-400">/</span>
          <span className="font-medium text-gray-700">{ws?.name||'…'}</span>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{ws?.name}</h1>
            {ws?.description&&<p className="text-gray-500 mt-1">{ws.description}</p>}
          </div>
          <button onClick={()=>nav(`/workspace/${id}/new-draft`)} className="btn-primary"><Plus className="w-4 h-4"/>New Draft</button>
        </div>
        <div className="flex gap-1 mb-6 border-b border-gray-200">
          {tabs.map(t=>(
            <button key={t.key} onClick={()=>setTab(t.key)} className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${tab===t.key?'border-brand-600 text-brand-600':'border-transparent text-gray-500 hover:text-gray-700'}`}>
              <t.icon className="w-4 h-4"/>{t.label}
            </button>
          ))}
        </div>
        {tab==='drafts'&&(
          <div className="space-y-3">
            {drafts.length===0&&<div className="card text-center text-gray-400 py-12">No drafts yet — create one to get started</div>}
            {drafts.map(d=>(
              <button key={d.id} onClick={()=>nav(`/draft/${d.id}`)} className="card w-full text-left flex items-center justify-between hover:border-brand-300 transition-colors p-4">
                <div>
                  <p className="font-medium text-gray-900">{d.title}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(d.status)}`}>{d.status.replace('_',' ')}</span>
                    {d.channel&&<span className="text-xs text-gray-400">{d.channel}</span>}
                    <span className="text-xs text-gray-400">{formatDate(d.created_at)}</span>
                  </div>
                </div>
                <span className="text-brand-600 text-sm font-medium">View →</span>
              </button>
            ))}
          </div>
        )}
        {tab==='guidelines'&&(
          <div>
            <div className="card mb-6">
              <h3 className="font-medium text-gray-900 mb-4">Import Guidelines</h3>
              <div className="space-y-3">
                <input value={glTitle} onChange={e=>setGlTitle(e.target.value)} className="input" placeholder="Guideline title e.g. Brand Voice Guide v2"/>
                <textarea value={glText} onChange={e=>setGlText(e.target.value)} rows={6} className="input resize-none" placeholder="Paste your brand guidelines text here…"/>
                <button onClick={addGuideline} className="btn-primary"><Plus className="w-4 h-4"/>Import & Split Clauses</button>
              </div>
            </div>
            <div className="space-y-4">
              {guidelines.map(g=>(
                <div key={g.id} className="card">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h4 className="font-medium text-gray-900">{g.title}</h4>
                      <p className="text-xs text-gray-400 mt-0.5">{g.clauses.length} clauses extracted · {formatDate(g.created_at)}</p>
                    </div>
                    <button onClick={()=>deleteGuideline(g.id)} className="btn-ghost text-red-500 p-1"><Trash2 className="w-4 h-4"/></button>
                  </div>
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {g.clauses.map(c=>(
                      <div key={c.id} className="flex gap-3 p-2 rounded-lg bg-gray-50">
                        <span className="text-xs font-mono text-brand-600 shrink-0 pt-0.5">{c.clause_number}</span>
                        <p className="text-xs text-gray-700">{c.text}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        {tab==='terminology'&&(
          <div>
            <div className="card mb-6">
              <h3 className="font-medium text-gray-900 mb-4">Add Terminology Rule</h3>
              <div className="grid grid-cols-2 gap-3 mb-3">
                <input value={termTerm} onChange={e=>setTermTerm(e.target.value)} className="input" placeholder="Term e.g. synergy"/>
                <select value={termType} onChange={e=>setTermType(e.target.value)} className="input">
                  <option value="banned">Banned</option>
                  <option value="preferred">Preferred</option>
                </select>
              </div>
              <input value={termAlt} onChange={e=>setTermAlt(e.target.value)} className="input mb-3" placeholder="Preferred alternative (optional)"/>
              <button onClick={addTerm} className="btn-primary"><Plus className="w-4 h-4"/>Add Term</button>
            </div>
            <div className="card">
              <h3 className="font-medium text-gray-900 mb-4">Terminology Rules ({terms.length})</h3>
              <div className="space-y-2">
                {terms.map(t=>(
                  <div key={t.id} className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                    <div>
                      <span className="font-medium text-gray-900 text-sm">"{t.term}"</span>
                      <span className={`ml-2 text-xs px-2 py-0.5 rounded-full font-medium ${t.entry_type==='banned'?'bg-red-100 text-red-700':'bg-green-100 text-green-700'}`}>{t.entry_type}</span>
                      {t.preferred_alternative&&<span className="ml-2 text-xs text-gray-500">→ "{t.preferred_alternative}"</span>}
                    </div>
                  </div>
                ))}
                {terms.length===0&&<p className="text-sm text-gray-400">No terminology rules yet</p>}
              </div>
            </div>
          </div>
        )}
        {tab==='facts'&&(
          <div>
            <div className="card mb-6">
              <h3 className="font-medium text-gray-900 mb-4">Add Approved Fact</h3>
              <textarea value={factClaim} onChange={e=>setFactClaim(e.target.value)} rows={3} className="input resize-none mb-3" placeholder="Approved factual claim e.g. Our uptime guarantee is 99.9%"/>
              <input value={factSrc} onChange={e=>setFactSrc(e.target.value)} className="input mb-3" placeholder="Source URL or reference (optional)"/>
              <button onClick={addFact} className="btn-primary"><Plus className="w-4 h-4"/>Add Fact</button>
            </div>
            <div className="card">
              <h3 className="font-medium text-gray-900 mb-4">Approved Facts ({facts.length})</h3>
              <div className="space-y-3">
                {facts.map(f=>(
                  <div key={f.id} className="p-3 rounded-lg bg-gray-50">
                    <p className="text-sm text-gray-900">{f.claim}</p>
                    {f.source&&<p className="text-xs text-brand-600 mt-1">{f.source}</p>}
                  </div>
                ))}
                {facts.length===0&&<p className="text-sm text-gray-400">No approved facts yet</p>}
              </div>
            </div>
          </div>
        )}
        {tab==='insights'&&insights&&(
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Overview</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-4 bg-brand-50 rounded-xl">
                  <p className="text-3xl font-bold text-brand-600">{insights.total_drafts}</p>
                  <p className="text-sm text-gray-600 mt-1">Total Drafts</p>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-xl">
                  <p className="text-3xl font-bold text-orange-600">{insights.total_findings}</p>
                  <p className="text-sm text-gray-600 mt-1">Total Findings</p>
                </div>
              </div>
            </div>
            <div className="card">
              <h3 className="font-semibold text-gray-900 mb-4">Findings by Category</h3>
              <div className="space-y-2">
                {Object.entries(insights.by_category).sort((a,b)=>b[1]-a[1]).map(([cat,cnt])=>(
                  <div key={cat} className="flex items-center gap-3">
                    <span className="text-sm text-gray-600 w-24 capitalize">{cat}</span>
                    <div className="flex-1 bg-gray-100 rounded-full h-2">
                      <div className="bg-brand-500 rounded-full h-2" style={{width:`${Math.min(100,(cnt/Math.max(...Object.values(insights.by_category)))*100)}%`}}/>
                    </div>
                    <span className="text-sm font-medium text-gray-900 w-6 text-right">{cnt}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="card md:col-span-2">
              <h3 className="font-semibold text-gray-900 mb-4">Unclear / Frequently Disputed Clauses</h3>
              {insights.unclear_clauses.length===0?<p className="text-sm text-gray-400">No data yet</p>:(
                <div className="space-y-3">
                  {insights.unclear_clauses.map(c=>(
                    <div key={c.id} className="p-3 rounded-lg border border-orange-100 bg-orange-50">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-mono text-orange-700">Clause {c.clause_number}</span>
                        <div className="flex gap-3 text-xs text-gray-500">
                          <span>{c.dispute_count} disputed</span>
                          <span>{c.dismissed_count} dismissed</span>
                          <span>{c.violation_count} violations</span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-700">{c.text}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

