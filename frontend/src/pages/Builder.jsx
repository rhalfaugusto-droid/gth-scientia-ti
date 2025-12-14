import React, { useState } from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

const ItemType = "STEP";

/* ---------- STEP ---------- */
function Step({ name }) {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: ItemType,
    item: { name },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  }));

  return (
    <motion.div
      ref={drag}
      whileHover={{ scale: 1.02 }}
      className={`card cursor-move ${isDragging ? "opacity-50" : ""}`}
    >
      {name}
    </motion.div>
  );
}

/* ---------- CANVAS ---------- */
function Canvas({ flow, setFlow }) {
  const [, drop] = useDrop(() => ({
    accept: ItemType,
    drop: (item) => setFlow((prev) => [...prev, item.name]),
  }));

  return (
    <div
      ref={drop}
      className="p-4 bg-slate-50 rounded min-h-[300px] border border-dashed"
    >
      {flow.length === 0 && (
        <p className="text-slate-400">Arraste etapas para montar o fluxo</p>
      )}

      {flow.map((s, i) => (
        <div key={i} className="card mt-2">
          {i + 1}. {s}
        </div>
      ))}
    </div>
  );
}

/* ---------- BUILDER ---------- */
export default function Builder() {
  const steps = [
    "Importar Nota",
    "Validar XML",
    "Classificar Tributação",
    "Calcular Imposto",
    "Gerar Relatório",
    "Enviar para Contabilidade",
  ];

  const [flow, setFlow] = useState([]);
  const navigate = useNavigate();

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="container py-6">
        <div className="grid grid-cols-3 gap-6">
          {/* LATERAL */}
          <aside className="col-span-1">
            <h3 className="mb-3 font-semibold">Ações</h3>
            <div className="space-y-2">
              {steps.map((s) => (
                <Step key={s} name={s} />
              ))}
            </div>
          </aside>

          {/* ÁREA PRINCIPAL */}
          <main className="col-span-2">
            <h2 className="mb-3 font-semibold">Montagem de Fluxo</h2>

            <Canvas flow={flow} setFlow={setFlow} />

            {/* BOTÕES */}
            <div className="flex gap-3 mt-6">
              <button
                className="bg-cyan-600 hover:bg-cyan-700 text-white px-5 py-2 rounded-lg text-sm font-medium"
                onClick={() => {
                  if (flow.length === 0) {
                    alert("Monte ao menos uma etapa do fluxo.");
                    return;
                  }
                  navigate("/builder/workflow", { state: { flow } });
                }}
              >
                Concluir
              </button>

              <button
                className="bg-white border border-slate-300 hover:bg-slate-50 px-5 py-2 rounded-lg text-sm"
                onClick={() => setFlow([])}
              >
                Limpar
              </button>
            </div>
          </main>
        </div>
      </div>
    </DndProvider>
  );
}
