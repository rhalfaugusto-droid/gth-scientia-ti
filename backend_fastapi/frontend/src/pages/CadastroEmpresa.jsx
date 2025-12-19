import React, {useState} from 'react'
export default function CadastroEmpresa(){
  const [empresa,setEmpresa]=useState({nome:'',cnpj:'',areaAtuacao:''})
  const salvar=()=>{
    localStorage.setItem('empresa',JSON.stringify(empresa))
    alert('Dados salvos localmente')
  }
  return (
    <div className="container py-6">
      <div className="card max-w-2xl">
        <h2 className="text-xl font-semibold mb-3">Cadastro da Empresa</h2>
        <input placeholder="Nome" value={empresa.nome} onChange={e=>setEmpresa({...empresa,nome:e.target.value})} className="w-full border rounded px-3 py-2 mb-2"/>
        <input placeholder="CNPJ" value={empresa.cnpj} onChange={e=>setEmpresa({...empresa,cnpj:e.target.value})} className="w-full border rounded px-3 py-2 mb-2"/>
        <input placeholder="Área de atuação" value={empresa.areaAtuacao} onChange={e=>setEmpresa({...empresa,areaAtuacao:e.target.value})} className="w-full border rounded px-3 py-2 mb-2"/>
        <div className="flex gap-2">
          <button onClick={salvar} className="bg-sky-500 text-white px-4 py-2 rounded">Salvar</button>
          <button onClick={()=>window.location.href='/cadastro-tributario'} className="px-4 py-2 rounded border">Próximo</button>
        </div>
      </div>
    </div>
  )
}
