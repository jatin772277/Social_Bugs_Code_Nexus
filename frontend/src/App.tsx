import {BrowserRouter,Routes,Route,Navigate} from 'react-router-dom'
import {Toaster} from 'react-hot-toast'
import {useAuthStore} from './store/auth'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import WorkspacePage from './pages/WorkspacePage'
import NewDraft from './pages/NewDraft'
import DraftReview from './pages/DraftReview'
function ProtectedRoute({children}:{children:React.ReactNode}){
  const {token}=useAuthStore()
  if(!token) return <Navigate to="/login" replace/>
  return <>{children}</>
}
export default function App(){
  return(
    <BrowserRouter>
      <Toaster position="top-right" toastOptions={{duration:3500,style:{fontSize:'14px'}}}/>
      <Routes>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard/></ProtectedRoute>}/>
        <Route path="/workspace/:id" element={<ProtectedRoute><WorkspacePage/></ProtectedRoute>}/>
        <Route path="/workspace/:workspaceId/new-draft" element={<ProtectedRoute><NewDraft/></ProtectedRoute>}/>
        <Route path="/draft/:id" element={<ProtectedRoute><DraftReview/></ProtectedRoute>}/>
        <Route path="/" element={<Navigate to="/dashboard" replace/>}/>
        <Route path="*" element={<Navigate to="/dashboard" replace/>}/>
      </Routes>
    </BrowserRouter>
  )
}

