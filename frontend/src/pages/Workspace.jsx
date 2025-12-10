import React, {useState} from 'react'
const widgets=['Resumo Tributário','Documentos Pendentes','Notas Importadas','Créditos / Débitos','Alertas da IA Fiscal']
export default function Workspace(){
  const [area,setArea]=useState([])
  const add=(w)=>{ if(!area.includes(w)) setArea([...area,w]) }
  return (
    <div style={{display:'flex',height:'90vh'}}>
      <aside style={{width:260,background:'#f1f5f9',padding:12}}>
        <h3>Módulos</h3>
        {widgets.map(w=> <button key={w} onClick={()=>add(w)} style={{display:'block',width:'100%',marginTop:8,padding:8}}>{w}</button>)}
      </aside>
      <main style={{flex:1,padding:20}}>
        <h2>Área de Trabalho</h2>
        {area.length===0 && <div>Selecione módulos ao lado.</div>}
        <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:12,marginTop:12}}>
          {area.map(a=> <div key={a} style={{background:'#fff',padding:12,borderRadius:8,boxShadow:'0 2px 6px rgba(0,0,0,0.06)'}}>{a}</div>)}
        </div>
      </main>
    </div>
  )
}
