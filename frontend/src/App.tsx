import React, { useEffect, useState } from 'react';
import LoginPanel from './components/LoginPanel';
import axios from 'axios';

export default function App(){
  const [token, setToken] = useState<string | null>(localStorage.getItem('gth_token'));
  const [flows, setFlows] = useState<any[]>([]);

  useEffect(()=>{
    if(!token) return;
    (async ()=>{
      try{
        const res = await axios.get((import.meta.env.VITE_API_BASE||'http://localhost:8000') + '/flows', { headers: { Authorization: 'Bearer '+token } });
        setFlows(res.data);
      }catch(e){ console.error(e); }
    })();
  }, [token]);

  if(!token) return <div className="h-screen flex items-center justify-center"><LoginPanel onLogin={(t)=> setToken(t)} /></div>

  return (
    <div className="h-screen p-4">
      <h1 className="text-xl font-bold mb-4">GTH - Fluxos</h1>
      <div className="mb-4">Usuário logado. Token salvo no localStorage.</div>
      <div>
        <h2 className="font-semibold">Fluxos salvos</h2>
        <ul className="mt-2">
          {flows.map(f=> <li key={f.id}>{f.name}</li>)}
        </ul>
      </div>
    </div>
  )
}
