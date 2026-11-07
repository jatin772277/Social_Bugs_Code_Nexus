import {useForm} from 'react-hook-form'
import {useNavigate,Link} from 'react-router-dom'
import {useAuthStore} from '../store/auth'
import api from '../lib/api'
import toast from 'react-hot-toast'
import {Shield} from 'lucide-react'
interface RegisterForm{full_name:string;email:string;password:string;role:string}
export default function Register(){
  const {register,handleSubmit,formState:{errors,isSubmitting}}=useForm<RegisterForm>({defaultValues:{role:'creator'}})
  const {setAuth}=useAuthStore()
  const nav=useNavigate()
  const onSubmit=async(data:RegisterForm)=>{
    try{
      await api.post('/auth/register',data)
      const lr=await api.post('/auth/login',{email:data.email,password:data.password})
      setAuth(lr.data.user,lr.data.access_token)
      toast.success('Account created!')
      nav('/dashboard')
    }catch(e:any){
      toast.error(e.response?.data?.detail||'Registration failed')
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
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Create your account</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="label">Full Name</label>
              <input {...register('full_name',{required:'Name is required'})} className="input" placeholder="Jane Smith"/>
              {errors.full_name&&<p className="text-red-500 text-xs mt-1">{errors.full_name.message}</p>}
            </div>
            <div>
              <label className="label">Email</label>
              <input {...register('email',{required:'Email is required'})} type="email" className="input" placeholder="you@company.com"/>
              {errors.email&&<p className="text-red-500 text-xs mt-1">{errors.email.message}</p>}
            </div>
            <div>
              <label className="label">Password</label>
              <input {...register('password',{required:'Password required',minLength:{value:6,message:'Min 6 chars'}})} type="password" className="input" placeholder="••••••••"/>
              {errors.password&&<p className="text-red-500 text-xs mt-1">{errors.password.message}</p>}
            </div>
            <div>
              <label className="label">Role</label>
              <select {...register('role')} className="input">
                <option value="creator">Content Creator</option>
                <option value="manager">Brand Manager</option>
                <option value="reviewer">Authorised Reviewer</option>
                <option value="admin">Workspace Admin</option>
              </select>
            </div>
            <button type="submit" disabled={isSubmitting} className="btn-primary w-full justify-center py-2.5">
              {isSubmitting?'Creating…':'Create Account'}
            </button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-6">
            Have an account?{' '}
            <Link to="/login" className="text-brand-600 font-medium hover:underline">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}

