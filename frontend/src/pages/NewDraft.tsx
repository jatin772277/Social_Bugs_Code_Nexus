import {useState} from 'react'
import {useNavigate,useParams} from 'react-router-dom'
import {useForm} from 'react-hook-form'
import api from '../lib/api'
import toast from 'react-hot-toast'
import {useAuthStore} from '../store/auth'
import {Shield,ArrowLeft,Send} from 'lucide-react'
interface DraftForm{title:string;content:string;channel:string;purpose:string}
export default function NewDraft(){
  const {workspaceId}=useParams<{workspaceId:string}>()
  const nav=useNavigate()
  const {user}=useAuthStore()
  const wsId=workspaceId||String(user?.workspace_id||1)
  const {register,handleSubmit,formState:{errors,isSubmitting}}=useForm<DraftForm>()
  const onSubmit=async(data:DraftForm)=>{
    try{
      const r=await api.post('/drafts',{...data,workspace_id:parseInt(wsId)})
      toast.success('Draft created')
      nav(`/draft/${r.data.id}`)
    }catch(e:any){toast.error(e.response?.data?.detail||'Failed')}
  }
  return(
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-4">
          <button onClick={()=>nav(-1)} className="btn-ghost p-2"><ArrowLeft className="w-4 h-4"/></button>
          <Shield className="w-6 h-6 text-brand-600"/>
          <span className="font-bold text-gray-900">New Draft</span>
        </div>
      </nav>
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="card">
          <h1 className="text-xl font-bold text-gray-900 mb-6">Create New Draft</h1>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div>
              <label className="label">Draft Title *</label>
              <input {...register('title',{required:'Title required'})} className="input" placeholder="e.g. Q1 Product Launch Press Release"/>
              {errors.title&&<p className="text-red-500 text-xs mt-1">{errors.title.message}</p>}
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Channel</label>
                <select {...register('channel')} className="input">
                  <option value="">Select channel…</option>
                  <option value="social_post">Social Post</option>
                  <option value="press_release">Press Release</option>
                  <option value="blog">Blog Article</option>
                  <option value="email">Email</option>
                  <option value="website_copy">Website Copy</option>
                  <option value="advertisement">Advertisement</option>
                  <option value="internal">Internal Communication</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="label">Purpose (one line)</label>
                <input {...register('purpose')} className="input" placeholder="e.g. Announce Series B funding"/>
              </div>
            </div>
            <div>
              <label className="label">Content *</label>
              <textarea {...register('content',{required:'Content required',minLength:{value:20,message:'Content too short'}})} rows={12} className="input resize-none font-mono text-sm" placeholder="Paste or type your draft content here…"/>
              {errors.content&&<p className="text-red-500 text-xs mt-1">{errors.content.message}</p>}
            </div>
            <div className="flex justify-end gap-3">
              <button type="button" onClick={()=>nav(-1)} className="btn-secondary">Cancel</button>
              <button type="submit" disabled={isSubmitting} className="btn-primary"><Send className="w-4 h-4"/>{isSubmitting?'Creating…':'Create Draft'}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

