import React, { useState } from 'react';

export default function LoginPanel({ onLogin }: { onLogin: (token:string)=>void }){
  const [user, setUser] = useState('admin');
  const [pw, setPw] = useState('admin123');
  const login = async ()=>{
    try{
      const res = await fetch((import.meta.env.VITE_API_BASE||'http://localhost:8000') + '/token', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({username:user,password:pw}) });
      if(!res.ok){ alert('Login failed'); return; }
      const data = await res.json();
      localStorage.setItem('gth_token', data.access_token);
      onLogin(data.access_token);
    }catch(e){ console.error(e); alert('Erro no login'); }
  };
  return (
    <div className="p-4 border rounded">
      <div className="mb-2"><label className="text-xs">Usuário</label><input className="w-full border p-1" value={user} onChange={e=>setUser(e.target.value)} /></div>
      <div className="mb-2"><label className="text-xs">Senha</label><input type="password" className="w-full border p-1" value={pw} onChange={e=>setPw(e.target.value)} /></div>
      <div className="flex space-x-2"><button className="px-3 py-1 bg-blue-600 text-white rounded" onClick={login}>Entrar</button></div>
    </div>
  )
}
