// frontend/src/components/Toolbox.jsx
import React from "react";
import { ChevronRightIcon, DocumentTextIcon, Cog6ToothIcon, CalculatorIcon, InboxIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline';

export default function Toolbox({ steps }) {
  return (
    <div className="p-2">
      <h3 className="mb-3 font-semibold">Ações</h3>
      <div className="flex flex-col gap-2">
        {steps.map((s) => (
          <div key={s.key} className="flex items-center gap-2 p-2 bg-white rounded-lg shadow-sm cursor-grab tool-button">
            <Icon name={s.icon} />
            <div className="text-sm font-medium">{s.label}</div>
            <ChevronRightIcon className="w-4 h-4 ml-auto text-slate-400" />
          </div>
        ))}
      </div>
    </div>
  );
}

function Icon({ name }) {
  const props = { className: "w-6 h-6 text-slate-600" };
  switch (name) {
    case "import": return <InboxIcon {...props} />;
    case "validate": return <DocumentTextIcon {...props} />;
    case "classify": return <Cog6ToothIcon {...props} />;
    case "calc": return <CalculatorIcon {...props} />;
    case "report": return <DocumentTextIcon {...props} />;
    case "send": return <PaperAirplaneIcon {...props} />;
    default: return <DocumentTextIcon {...props} />;
  }
}
