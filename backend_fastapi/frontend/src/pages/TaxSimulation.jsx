import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

// URL base da API (ajustar conforme o ambiente de deploy)
const API_BASE_URL = 'http://localhost:8000'; 

export default function TaxSimulation() {
    const [file, setFile] = useState(null);
    const [simulationResult, setSimulationResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setSimulationResult(null);
        setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            setError("Por favor, selecione um arquivo XML de NFe.");
            return;
        }

        setLoading(true);
        setError(null);
        setSimulationResult(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Chamada para a nova rota de simulação
            const response = await axios.post(
                `${API_BASE_URL}/simulation/simulate_nfe`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        // Adicionar token de autenticação se necessário (depende da implementação do frontend)
                        // 'Authorization': `Bearer ${localStorage.getItem('token')}` 
                    }
                }
            );
            setSimulationResult(response.data);
        } catch (err) {
            console.error("Erro na simulação:", err.response ? err.response.data : err.message);
            setError(err.response?.data?.detail || "Erro ao processar a simulação. Verifique se o backend está rodando e se o XML é válido.");
        } finally {
            setLoading(false);
        }
    };

    const renderSimulationDetails = () => {
        if (!simulationResult) return null;

        const { nfe_data, simulation } = simulationResult;

        return (
            <motion.div 
                initial={{ opacity: 0, y: 20 }} 
                animate={{ opacity: 1, y: 0 }} 
                className="mt-6 p-6 bg-white rounded-lg shadow-lg"
            >
                <h3 className="text-xl font-bold mb-4 text-sky-700">Resultado da Simulação Tributária</h3>
                
                <div className="grid grid-cols-2 gap-4 mb-6 border-b pb-4">
                    <p><strong>Chave de Acesso:</strong> {nfe_data.chave_acesso}</p>
                    <p><strong>Data de Emissão:</strong> {new Date(nfe_data.data_emissao).toLocaleDateString()}</p>
                    <p><strong>Valor Total dos Produtos:</strong> R$ {nfe_data.valor_total_produtos.toFixed(2)}</p>
                    <p><strong>UF Emitente/Destinatário:</strong> {nfe_data.emitente_uf} / {nfe_data.destinatario_uf}</p>
                </div>

                <h4 className="text-lg font-semibold mb-3">Cálculo do IVA Dual (Simulado)</h4>
                <p className="text-2xl font-extrabold text-green-600 mb-4">
                    Imposto Total Simulado: R$ {simulation.total_tax.toFixed(2)}
                </p>

                <div className="space-y-2">
                    {Object.entries(simulation.breakdown).map(([tax, data]) => (
                        <div key={tax} className="flex justify-between border-b border-gray-100 pb-1">
                            <span className="font-medium">{tax} ({data.rate}):</span>
                            <span className="font-semibold">R$ {data.amount.toFixed(2)}</span>
                        </div>
                    ))}
                </div>

                <h4 className="text-sm font-semibold mt-4 pt-4 border-t">Evidências do Cálculo</h4>
                <pre className="bg-gray-50 p-3 text-xs rounded overflow-auto">
                    {JSON.stringify(simulation.evidence, null, 2)}
                </pre>

            </motion.div>
        );
    };

    return (
        <div className="container py-6">
            <motion.h1 
                initial={{ x: -20, opacity: 0 }} 
                animate={{ x: 0, opacity: 1 }} 
                className="text-2xl font-bold mb-6"
            >
                Simulação Tributária Híbrida (NFe)
            </motion.h1>

            <motion.div 
                initial={{ y: 10, opacity: 0 }} 
                animate={{ y: 0, opacity: 1 }} 
                className="card p-6 max-w-xl"
            >
                <h3 className="font-semibold mb-4">Upload de XML para Simulação</h3>
                <form onSubmit={handleSubmit}>
                    <input 
                        type="file" 
                        accept=".xml" 
                        onChange={handleFileChange} 
                        className="w-full border rounded p-2 mb-4"
                    />
                    <button 
                        type="submit" 
                        disabled={loading || !file}
                        className="w-full bg-sky-500 text-white px-4 py-2 rounded disabled:bg-gray-400 hover:bg-sky-600 transition"
                    >
                        {loading ? 'Simulando...' : 'Simular IVA Dual (CBS/IBS)'}
                    </button>
                </form>

                {error && (
                    <div className="mt-4 p-3 bg-red-100 text-red-700 rounded border border-red-300">
                        {error}
                    </div>
                )}
            </motion.div>

            {renderSimulationDetails()}
        </div>
    );
}
