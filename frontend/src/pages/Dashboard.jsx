import React from 'react'
import { motion } from 'framer-motion'
export default function Dashboard(){
  const cards = [
    {title:'Resumo Tributário', value:'OK'},
    {title:'Notas Pendentes', value:12},
    {title:'Créditos Disponíveis', value:'R$ 12.345,67'},
    {title:'Alertas', value:2}
  ]
  return (
    <div className="container py-6">
      <motion.h1 initial={{x:-20,opacity:0}} animate={{x:0,opacity:1}} className="text-2xl font-bold mb-4">Área de Trabalho</motion.h1>
      <div className="grid grid-cols-4 gap-4 mb-6">
        {cards.map((c,i)=>(
          <motion.div key={i} initial={{y:10,opacity:0}} animate={{y:0,opacity:1}} className="card">
            <div className="text-sm text-slate-500">{c.title}</div>
            <div className="text-2xl font-semibold">{c.value}</div>
          </motion.div>
        ))}
      </div>
      <div className="card p-6">
        <h3 className="font-semibold mb-2">Últimas Notas</h3>
        <div className="text-sm text-slate-600">Nenhuma nota importada.</div>
      </div>
    </div>
  )
}
