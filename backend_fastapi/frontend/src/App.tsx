
import React from 'react';
export default function App(){
  return (
    <div style={{fontFamily:'Arial', padding:20}}>
      <h1>Workspace - Plataforma Tributária (Prototype)</h1>
      <div style={{display:'flex', gap:20}}>
        <div style={{width:220, border:'1px solid #ddd', padding:10}}>
          <h3>Modules</h3>
          <ul>
            <li>Documentos</li>
            <li>Apurações</li>
            <li>IA Assistente</li>
          </ul>
        </div>
        <div style={{flex:1, minHeight:300, border:'2px dashed #ccc', padding:20}}>
          <h3>Arraste módulos aqui</h3>
          <p>Este é um protótipo inicial do workspace.</p>
          <div style={{marginTop:20}}>
            <input type="file" id="fileinput" multiple />
          </div>
        </div>
      </div>
    </div>
  );
}
