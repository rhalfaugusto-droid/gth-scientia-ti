import React, {useState} from 'react'
export default function CadastroTributario(){
  const [regime,setRegime]=useState('')
  const concluir=()=>{ localStorage.setItem('regimeTributario',regime); alert('Regime salvo'); window.location.href='/workspace' }
  return (
    <div className="container py-6">
      <div className="card max-w-2xl">
        <h2 className="text-xl font-semibold mb-3">Selecione o Regime Tributário</h2>
        <select value={regime} onChange={e=>setRegime(e.target.value)} className="w-full border rounded px-3 py-2 mb-3">
          <option value=''>Selecione...</option>
          <option value='simples'>Simples Nacional</option>
          <option value='presumido'>Lucro Presumido</option>
          <option value='real'>Lucro Real</option>
          <option value='hibrido'>Período Híbrido 2026-2033</option>
        </select>
        <div className="flex gap-2">
          <button onClick={concluir} className="bg-sky-500 text-white px-4 py-2 rounded">Concluir</button>
        </div>
      </div>
    </div>
  )
}
