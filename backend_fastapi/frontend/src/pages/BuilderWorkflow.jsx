// frontend/src/pages/BuilderWorkflow.jsx
import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function BuilderWorkflow() {
  const location = useLocation();
  const navigate = useNavigate();
  const initialFlow = (location.state && location.state.flow) || JSON.parse(localStorage.getItem("gth_flow") || "[]");

  const [flow, setFlow] = useState(initialFlow);
  const [activeTab, setActiveTab] = useState(0);
  const [formData, setFormData] = useState({}); // store per-step data
  const [name, setName] = useState("");

  useEffect(() => {
    // persist in localStorage so reloads won't lose data
    localStorage.setItem("gth_flow", JSON.stringify(flow));
  }, [flow]);

  async function handleSaveWorkflow() {
    try {
      const payload = { name: name || `workflow-${Date.now()}`, data: { nodes: flow, meta: formData } };
      const res = await api.post("/workflows/", payload);
      alert("Workflow salvo com id: " + res.data.id);
      navigate("/workspace");
    } catch (err) {
      console.error(err);
      alert("Erro ao salvar workflow");
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-white overflow-auto">
      <div className="p-4 border-b flex items-center gap-4">
        <button className="px-2 py-1" onClick={() => navigate(-1)}>Voltar</button>
        <input value={name} onChange={(e)=>setName(e.target.value)} placeholder="Nome do workflow" className="p-2 border rounded" />
        <div className="ml-auto flex gap-2">
          <button onClick={handleSaveWorkflow} className="bg-green-600 text-white px-3 py-1 rounded">Salvar</button>
        </div>
      </div>

      <div className="p-4">
        <div className="flex gap-2 border-b mb-4">
          {flow.map((s, idx) => (
            <div key={idx} onClick={()=>setActiveTab(idx)} className={`px-3 py-1 cursor-pointer ${activeTab===idx ? "border-b-2 border-slate-800":""}`}>
              {idx+1}. {s}
            </div>
          ))}
        </div>

        <div>
          {flow.length===0 && <div className="p-6 text-slate-500">Nenhuma etapa no fluxo</div>}
          {flow[activeTab] && (
            <StepEditor stepName={flow[activeTab]} formData={formData} setFormData={setFormData} index={activeTab} />
          )}
        </div>
      </div>
    </div>
  );
}

function StepEditor({ stepName, formData, setFormData, index }) {
  const key = `step_${index}`;
  const state = formData[key] || { notes: "", params: {} };

  return (
    <div className="p-4 bg-slate-50 rounded">
      <h3 className="font-semibold mb-2">{stepName}</h3>

      <label className="block text-sm text-slate-600 mb-1">Observações</label>
      <textarea className="w-full p-2 border rounded mb-3" placeholder="Anotações" defaultValue={state.notes} onChange={(e)=>{
        setFormData(prev => ({ ...prev, [key]: { ...(prev[key]||{}), notes: e.target.value } }));
      }} />

      <label className="block text-sm text-slate-600 mb-1">Parâmetros (JSON)</label>
      <textarea className="w-full p-2 border rounded mb-3" placeholder='{"param":123}' defaultValue={JSON.stringify(state.params)} onChange={(e)=>{
        try {
          const parsed = JSON.parse(e.target.value || "{}");
          setFormData(prev => ({ ...prev, [key]: { ...(prev[key]||{}), params: parsed } }));
        } catch (err) {
          // ignore parse error for now
        }
      }} />
    </div>
  );
}
