import {clsx,type ClassValue} from 'clsx'
import {twMerge} from 'tailwind-merge'
export function cn(...inputs:ClassValue[]){return twMerge(clsx(inputs))}
export function formatDate(d:string){return new Date(d).toLocaleDateString('en-IN',{day:'2-digit',month:'short',year:'numeric'})}
export function formatDateTime(d:string){return new Date(d).toLocaleString('en-IN',{day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'})}
export function statusColor(s:string){
  const map:Record<string,string>={
    draft:'bg-gray-100 text-gray-700',
    under_review:'bg-blue-100 text-blue-800',
    pending_approval:'bg-yellow-100 text-yellow-800',
    approved:'bg-green-100 text-green-800',
    rejected:'bg-red-100 text-red-800',
  }
  return map[s]||'bg-gray-100 text-gray-700'
}

