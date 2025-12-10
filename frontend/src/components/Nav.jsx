import React from 'react'
import { Link } from 'react-router-dom'
export default function Nav(){
  return (
    <nav style={{background:'#0f172a',padding:12}}>
      <div style={{maxWidth:1200,margin:'0 auto',display:'flex',gap:12}}>
        <Link to='/' style={{color:'#fff',textDecoration:'none',fontWeight:700}}>GTH</Link>
        <Link to='/workspace' style={{color:'#9ca3af',textDecoration:'none'}}>Workspace</Link>
        <Link to='/builder' style={{color:'#9ca3af',textDecoration:'none'}}>Builder</Link>
      </div>
    </nav>
  )
}
