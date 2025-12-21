import { useEffect, useState } from "react";
import { getUsers } from "./services/users";

export default function App() {
  const [users, setUsers] = useState<any[]>([]);

  useEffect(() => {
    getUsers()
      .then(setUsers)
      .catch(err => console.error("Erro API:", err));
  }, []);

  return (
    <div style={{ fontFamily: "Arial", padding: 20 }}>
      <h1>Workspace - Plataforma Tributária (Prototype)</h1>

      <div style={{ display: "flex", gap: 20 }}>
        <div style={{ width: 220, border: "1px solid #ddd", padding: 10 }}>
          <h3>Modules</h3>
          <ul>
            <li>Documentos</li>
            <li>Apurações</li>
            <li>IA Assistente</li>
          </ul>
        </div>

        <div
          style={{
            flex: 1,
            minHeight: 300,
            border: "2px dashed #ccc",
            padding: 20,
          }}
        >
          <h3>Arraste módulos aqui</h3>
          <p>Este é um protótipo inicial do workspace.</p>

          <div style={{ marginTop: 20 }}>
            <input type="file" multiple />
          </div>

          <hr style={{ margin: "20px 0" }} />

          <h3>Usuários (Backend)</h3>
          <pre style={{ background: "#f5f5f5", padding: 10 }}>
            {JSON.stringify(users, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
