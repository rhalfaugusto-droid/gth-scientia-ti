import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Nav(){
  const navigate = useNavigate()
  const logout = ()=>{
    localStorage.removeItem('token')
    localStorage.removeItem('backend')
    navigate('/')
  }
  return (
    <motion.nav initial={{y:-20,opacity:0}} animate={{y:0,opacity:1}} transition={{duration:0.4}} className="bg-gradient-to-r from-slate-800 to-slate-900 text-white">
      <div className="container flex items-center justify-between py-3">
        <div className="flex items-center gap-4">
          <Link to="/" className="text-xl font-bold">GTH</Link>
          <Link to="/workspace" className="text-sm text-slate-200">Workspace</Link>
          <Link to="/builder" className="text-sm text-slate-200">Builder</Link>
          <Link to="/simulation" className="text-sm text-slate-200">Simulação</Link>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={()=>navigate('/cadastro-empresa')} className="text-sm">Novo Cliente</button>
          <button onClick={logout} className="bg-sky-500 px-3 py-1 rounded text-white text-sm">Logout</button>
        </div>
      </div>
    </motion.nav>
  )
}
