from backend_fastapi.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_simulacao_simples_sucesso():
    payload = {
        "faturamento_mensal": 10000,
        "anexo": "I",
        "uf": "SP"
    }

    response = client.post("/simulation/simples", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["regime"] == "Simples Nacional"
    assert data["anexo"] == "I"
    assert data["faturamento_mensal"] == 10000
    assert data["aliquota_estimada"] == 0.06
    assert data["das_estimado"] == 600.0


def test_simulacao_simples_faturamento_invalido():
    payload = {
        "faturamento_mensal": 0,
        "anexo": "I",
        "uf": "SP"
    }

    response = client.post("/simulation/simples", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Faturamento inválido"


def test_simulacao_simples_contrato_resposta():
    payload = {
        "faturamento_mensal": 35000,
        "anexo": "III",
        "uf": "SP"
    }

    response = client.post("/simulation/simples", json=payload)

    assert response.status_code == 200

    data = response.json()

    # Campos obrigatórios do contrato
    assert "regime" in data
    assert "anexo" in data
    assert "uf" in data
    assert "faturamento_mensal" in data
    assert "aliquota_estimada" in data
    assert "das_estimado" in data
    assert "observacao" in data

    # Tipos esperados
    assert isinstance(data["regime"], str)
    assert isinstance(data["anexo"], str)
    assert isinstance(data["uf"], str)
    assert isinstance(data["faturamento_mensal"], (int, float))
    assert isinstance(data["aliquota_estimada"], float)
    assert isinstance(data["das_estimado"], float)
    assert isinstance(data["observacao"], str)
