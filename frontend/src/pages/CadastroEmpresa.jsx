import { useState } from 'react'
export default function CadastroEmpresa(){
  const [empresa,setEmpresa]=useState({nome:'',cnpj:'',areaAtuacao:''})
  const next=()=>{
    localStorage.setItem('empresa',JSON.stringify(empresa))
    window.location.href='/cadastro-tributario'
  }
  return (
    <div className='container'>
      <h1>Cadastro da Empresa</h1>
      <input placeholder='Nome' value={empresa.nome} onChange={e=>setEmpresa({...empresa,nome:e.target.value})} style={{width:'100%',padding:10}}/>
      <input placeholder='CNPJ' value={empresa.cnpj} onChange={e=>setEmpresa({...empresa,cnpj:e.target.value})} style={{width:'100%',padding:10,marginTop:8}}/>
      <input placeholder='Área de atuação' value={empresa.areaAtuacao} onChange={e=>setEmpresa({...empresa,areaAtuacao:e.target.value})} style={{width:'100%',padding:10,marginTop:8}}/>
      <button onClick={next} style={{marginTop:12,padding:10,background:'#10b981',color:'#fff',border:0,borderRadius:6}}>Próximo</button>
    </div>
  )
}
