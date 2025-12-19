import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

/**
 * Autenticação local (fallback)
 * Edite esses usuários aqui para adicionar / mudar e-mails e senhas.
 */
const LOCAL_USERS = [
  { email: "admin@gth.com", password: "123456", name: "Administrador", role: "admin" },
  { email: "teste@gth.com", password: "teste", name: "Usuário Teste", role: "user" }
];

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // verifica na lista local
  const checkLocal = (email, password) => {
    return LOCAL_USERS.find((u) => u.email === email && u.password === password) || null;
  };

  const handleLogin = async () => {
    setError("");

    // 1) Primeiro tenta autenticar localmente (offline)
    const localUser = checkLocal(email.trim(), password);
    if (localUser) {
      localStorage.setItem("token", "local-token");
      localStorage.setItem("user", JSON.stringify({ email: localUser.email, name: localUser.name, role: localUser.role }));
      localStorage.setItem("backend", "local");
      return navigate("/workspace");
    }

    // 2) Se não for local, tenta Node backend (porta 4000)
    try {
      const nodeRes = await axios.post("http://localhost:4000/auth/login", { email, password }, { timeout: 3000 });
      if (nodeRes?.data?.token) {
        localStorage.setItem("token", nodeRes.data.token);
        localStorage.setItem("backend", "node");
        return navigate("/workspace");
      }
    } catch (e) {
      // ignora - tentaremos python a seguir
    }

    // 3) Tenta Python backend (porta 8000)
    try {
      const pyRes = await axios.post("http://localhost:8000/auth/login", { email, password }, { timeout: 3000 });
      if (pyRes?.data?.access_token) {
        localStorage.setItem("token", pyRes.data.access_token);
        localStorage.setItem("backend", "python");
        return navigate("/workspace");
      }
    } catch (e) {
      // ignora
    }

    setError("Credenciais inválidas — verifique e-mail/senha ou use 'Entrar sem backend (teste)'.");
  };

  // botão rápido para entrar sem autenticação (modo teste)
  const quick = () => {
    localStorage.setItem("token", "dev");
    localStorage.setItem("backend", "none");
    navigate("/workspace");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100">
      <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="card w-full max-w-md">
        <h2 className="text-2xl font-semibold mb-4">Entrar — GTH</h2>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <input placeholder="E-mail" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full border rounded px-3 py-2 mb-2" />
        <input placeholder="Senha" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full border rounded px-3 py-2 mb-4" />
        <button onClick={handleLogin} className="w-full bg-sky-500 text-white py-2 rounded">Entrar</button>
        <button onClick={quick} className="w-full mt-2 border rounded py-2">Entrar sem backend (teste)</button>

        <div style={{ marginTop: 12, fontSize: 13, color: "#6b7280" }}>
          Usuários locais disponíveis:
          <ul>
            <li>admin@gth.com / 123456 (admin)</li>
            <li>teste@gth.com / teste (usuário)</li>
          </ul>
        </div>
      </motion.div>
    </div>
  );
}
