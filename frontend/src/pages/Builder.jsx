import React, {useState} from 'react'
import { DndProvider, useDrag, useDrop } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

const ItemType = 'STEP'

function Step({name}){
  const [{isDragging}, drag] = useDrag(()=>({type:ItemType, item:{name}}),[name])
  return <div ref={drag} style={{padding:8,background:'#fff',borderRadius:6,boxShadow:'0 1px 3px rgba(0,0,0,0.1)',opacity:isDragging?0.5:1}}>{name}</div>
}

function Canvas({flow,setFlow}){
  const [, drop] = useDrop(()=>({accept:ItemType, drop:(item)=> setFlow([...flow, item.name])}),[flow])
  return <div ref={drop} style={{minHeight:300,background:'#f8fafc',padding:12,borderRadius:6}}>
    {flow.map((s,i)=> <div key={i} style={{padding:8,background:'#fff',marginTop:8,borderRadius:6}}>{i+1}. {s}</div>)}
  </div>
}

export default function Builder(){
  const steps=['Importar Nota','Validar XML','Classificar Tributação','Calcular Imposto','Gerar Relatório','Enviar para Contabilidade']
  const [flow,setFlow]=useState([])
  return (
    <DndProvider backend={HTML5Backend}>
      <div style={{display:'flex',height:'90vh'}}>
        <aside style={{width:280,padding:12,background:'#f1f5f9'}}>
          <h3>Ações</h3>
          {steps.map(s=> <div key={s} style={{marginTop:8}}><Step name={s} /></div>)}
        </aside>
        <main style={{flex:1,padding:20}}>
          <h2>Montagem de Fluxo</h2>
          <Canvas flow={flow} setFlow={setFlow} />
        </main>
      </div>
    </DndProvider>
  )
}
