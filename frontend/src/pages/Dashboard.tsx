import {useEffect,useState} from 'react'
import {useNavigate} from 'react-router-dom'
import {useAuthStore} from '../store/auth'
import api from '../lib/api'
import toast from 'react-hot-toast'
import {Shield,Plus,Building2,FileText,BarChart3,LogOut,ChevronRight} from 'lucide-react'
import type {Workspace,Draft} from '../types'
import {formatDate,statusColor} from '../lib/utils'
export default function Dashboard(){
  const {user,logout}=useAuthStore()
  const nav=useNavigate()
  const [workspaces,setWorkspaces]=useState<Workspace[]>([])
  const [drafts,setDrafts]=useState<Draft[]>([])
  const [creating,setCreating]=useState(false)
  const [wsName,setWsName]=useState('')
  const [loading,setLoading]=useState(true)
  useEffect(()=>{
    Promise.all([
      api.get('/workspaces').then(r=>setWorkspaces(r.data)),
      user?.workspace_id?api.get(`/drafts?workspace_id=${user.workspace_id}`).then(r=>setDrafts(r.data)):Promise.resolve()
    ]).catch(()=>{}).finally(()=>setLoading(false))
  },[user])
  const createWorkspace=async()=>{
    if(!wsName.trim()) return
    try{
      const r=await api.post('/workspaces',{name:wsName})
      setWorkspaces(p=>[...p,r.data])
      setWsName('')
      setCreating(false)
      toast.success('Workspace created')
    }catch(e:any){toast.error(e.response?.data?.detail||'Failed')}
  }
  if(loading) return <div className="min-h-screen flex items-center justify-center"><div className="animate-spin w-8 h-8 border-4 border-brand-600 border-t-transparent rounded-full"/></div>
  return(
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield className="w-7 h-7 text-brand-600"/>
            <span className="font-bold text-xl text-gray-900">CodeNexus</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">{user?.full_name} <span className="ml-1 text-xs text-brand-600 capitalize">({user?.role})</span></span>
            <button onClick={()=>{logout();nav('/login')}} className="btn-ghost text-sm"><LogOut className="w-4 h-4"/>Sign out</button>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Manage your brand governance workspaces and drafts</p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-gray-900 flex items-center gap-2"><Building2 className="w-4 h-4"/>Workspaces</h2>
                <button onClick={()=>setCreating(!creating)} className="btn-primary text-xs py-1 px-2"><Plus className="w-3 h-3"/>New</button>
              </div>
              {creating&&(
                <div className="mb-4 flex gap-2">
                  <input value={wsName} onChange={e=>setWsName(e.target.value)} className="input text-sm" placeholder="Workspace name"/>
                  <button onClick={createWorkspace} className="btn-primary text-xs px-3">Create</button>
                </div>
              )}
              <div className="space-y-2">
                {workspaces.length===0&&<p className="text-sm text-gray-400">No workspaces yet</p>}
                {workspaces.map(ws=>(
                  <button key={ws.id} onClick={()=>nav(`/workspace/${ws.id}`)} className="w-full text-left p-3 rounded-lg hover:bg-gray-50 border border-gray-100 flex items-center justify-between group transition-colors">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{ws.name}</p>
                      <p className="text-xs text-gray-400">{formatDate(ws.created_at)}</p>
                    </div>
                    <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-brand-500 transition-colors"/>
                  </button>
                ))}
              </div>
            </div>
          </div>
          <div className="lg:col-span-2">
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-gray-900 flex items-center gap-2"><FileText className="w-4 h-4"/>Recent Drafts</h2>
                {user?.workspace_id&&<button onClick={()=>nav(`/workspace/${user.workspace_id}/new-draft`)} className="btn-primary text-xs py-1 px-2"><Plus className="w-3 h-3"/>New Draft</button>}
              </div>
              {drafts.length===0?<p className="text-sm text-gray-400">No drafts yet. Select a workspace to create one.</p>:(
                <div className="space-y-3">
                  {drafts.slice(0,8).map(d=>(
                    <button key={d.id} onClick={()=>nav(`/draft/${d.id}`)} className="w-full text-left p-3 rounded-lg hover:bg-gray-50 border border-gray-100 flex items-center justify-between group transition-colors">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">{d.title}</p>
                        <div className="flex items-center gap-2 mt-1">
                          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColor(d.status)}`}>{d.status.replace('_',' ')}</span>
                          {d.channel&&<span className="text-xs text-gray-400">{d.channel}</span>}
                          <span className="text-xs text-gray-400">{formatDate(d.created_at)}</span>
                        </div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-brand-500 ml-2 transition-colors"/>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

