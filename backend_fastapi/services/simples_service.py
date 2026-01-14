from typing import Dict


def simular_simples_nacional(
    faturamento_mensal: float,
    anexo: str,
    uf: str,
) -> Dict:
    """
    Simula cálculo básico do Simples Nacional.
    """

    if faturamento_mensal <= 0:
        raise ValueError("Faturamento inválido")

    # Alíquotas simplificadas por anexo (exemplo didático)
    aliquotas = {
        "I": 0.06,
        "II": 0.112,
        "III": 0.135,
        "IV": 0.165,
        "V": 0.155,
    }

    anexo = anexo.upper()

    if anexo not in aliquotas:
        raise ValueError("Anexo inválido")

    aliquota = aliquotas[anexo]
    das_estimado = faturamento_mensal * aliquota

    return {
        "regime": "Simples Nacional",
        "anexo": anexo,
        "uf": uf,
        "faturamento_mensal": faturamento_mensal,
        "aliquota_estimada": aliquota,
        "das_estimado": round(das_estimado, 2),
        "observacao": "Simulação simplificada sem considerar faixa progressiva",
    }
