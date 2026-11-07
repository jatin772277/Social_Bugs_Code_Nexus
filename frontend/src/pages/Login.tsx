import {useState} from 'react'
import {useForm} from 'react-hook-form'
import {useNavigate,Link} from 'react-router-dom'
import {useAuthStore} from '../store/auth'
import api from '../lib/api'
import toast from 'react-hot-toast'
import {Shield,Eye,EyeOff} from 'lucide-react'
interface LoginForm{email:string;password:string}
export default function Login(){
  const [show,setShow]=useState(false)
  const {register,handleSubmit,formState:{errors,isSubmitting}}=useForm<LoginForm>()
  const {setAuth}=useAuthStore()
  const nav=useNavigate()
  const onSubmit=async(data:LoginForm)=>{
    try{
      const r=await api.post('/auth/login',data)
      setAuth(r.data.user,r.data.access_token)
      toast.success(`Welcome, ${r.data.user.full_name}`)
      nav('/dashboard')
    }catch(e:any){
      toast.error(e.response?.data?.detail||'Login failed')
    }
  }
  return(
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-brand-900 to-brand-700 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-white rounded-2xl shadow-lg mb-4">
            <Shield className="w-8 h-8 text-brand-600"/>
          </div>
          <h1 className="text-3xl font-bold text-white">CodeNexus</h1>
          <p className="text-brand-200 mt-1">Brand Governance Platform</p>
        </div>
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Sign in to your account</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="label">Email</label>
              <input {...register('email',{required:'Email is required'})} type="email" className="input" placeholder="you@company.com"/>
              {errors.email&&<p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
            </div>
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <input {...register('password',{required:'Password is required'})} type={show?'text':'password'} className="input pr-10" placeholder="••••••••"/>
                <button type="button" onClick={()=>setShow(!show)} className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600">
                  {show?<EyeOff className="w-4 h-4"/>:<Eye className="w-4 h-4"/>}
                </button>
              </div>
              {errors.password&&<p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
            </div>
            <button type="submit" disabled={isSubmitting} className="btn-primary w-full justify-center py-2.5">
              {isSubmitting?'Signing in…':'Sign in'}
            </button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-6">
            No account?{' '}
            <Link to="/register" className="text-brand-600 font-medium hover:underline">Register here</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

