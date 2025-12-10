import { useState } from 'react'
import axios from 'axios'
export default function Login(){
  const [email,setEmail]=useState('')
  const [senha,setSenha]=useState('')
  const [erro,setErro]=useState('')
  const handleLogin=async()=>{
    try{
      const res=await axios.post('/auth/login',{email, password: senha})
      localStorage.setItem('token', res.data.access_token || 'demo')
      window.location.href='/workspace'
    }catch(e){
      setErro('Credenciais inválidas')
    }
  }
  return (
    <div style={{display:'flex',height:'80vh',alignItems:'center',justifyContent:'center'}}>
      <div style={{width:360,background:'#fff',padding:20,borderRadius:8,boxShadow:'0 2px 10px rgba(0,0,0,0.08)'}}>
        <h2>Entrar</h2>
        {erro && <div style={{color:'red'}}>{erro}</div>}
        <input placeholder='E-mail' value={email} onChange={e=>setEmail(e.target.value)} style={{width:'100%',padding:8,marginTop:8}}/>
        <input placeholder='Senha' type='password' value={senha} onChange={e=>setSenha(e.target.value)} style={{width:'100%',padding:8,marginTop:8}}/>
        <button onClick={handleLogin} style={{width:'100%',marginTop:12,padding:10,background:'#0ea5e9',color:'#fff',border:0,borderRadius:6}}>Entrar</button>
      </div>
    </div>
  )
}
