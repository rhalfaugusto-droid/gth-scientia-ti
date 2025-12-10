import { useState } from 'react'
export default function CadastroTributario(){
  const [regime,setRegime]=useState('')
  const concluir=()=>{ localStorage.setItem('regimeTributario',regime); window.location.href='/workspace' }
  return (
    <div className='container'>
      <h1>Selecione o Regime Tributário</h1>
      <select value={regime} onChange={e=>setRegime(e.target.value)} style={{width:'100%',padding:10}}>
        <option value=''>Selecione...</option>
        <option value='simples'>Simples Nacional</option>
        <option value='presumido'>Lucro Presumido</option>
        <option value='real'>Lucro Real</option>
        <option value='hibrido'>Período Híbrido 2026-2033</option>
      </select>
      <button onClick={concluir} style={{marginTop:12,padding:10,background:'#0ea5e9',color:'#fff',border:0,borderRadius:6}}>Concluir</button>
    </div>
  )
}
