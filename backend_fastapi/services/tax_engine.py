from backend_fastapi.dataclasses import dataclass
from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.dependencies import get_current_user
from backend_fastapi import database


@dataclass
class TaxInput:
    receita_bruta_12m: float
    folha_12m: float
    receita_mes: float
    atividade: str


@dataclass
class TaxResult:
    anexo: str
    fator_r: float
    aliquota_efetiva: float
    valor_das_estimado: float
    explicacao: str


class SimplesNacionalEngine:

    def calcular_fator_r(self, receita_12m: float, folha_12m: float) -> float:
        if receita_12m == 0:
            return 0
        return folha_12m / receita_12m

    def definir_anexo(self, fator_r: float) -> str:
        return "III" if fator_r >= 0.28 else "V"

    def obter_aliquota(self, anexo: str, receita_12m: float) -> float:
        if anexo == "III":
            if receita_12m <= 180000:
                return 0.06
            elif receita_12m <= 360000:
                return 0.112
            else:
                return 0.135

        if anexo == "V":
            if receita_12m <= 180000:
                return 0.155
            elif receita_12m <= 360000:
                return 0.18
            else:
                return 0.195

        raise ValueError("Anexo inválido")

    def calcular(self, data: TaxInput) -> TaxResult:
        fator_r = self.calcular_fator_r(
            data.receita_bruta_12m,
            data.folha_12m
        )

        anexo = self.definir_anexo(fator_r)
        aliquota = self.obter_aliquota(anexo, data.receita_bruta_12m)

        valor_das = data.receita_mes * aliquota

        explicacao = (
            f"Empresa enquadrada no Anexo {anexo} "
            f"pois o Fator R foi de {fator_r:.2%}. "
            f"Alíquota efetiva aplicada: {aliquota:.2%}."
        )

        return TaxResult(
            anexo=anexo,
            fator_r=round(fator_r, 4),
            aliquota_efetiva=aliquota,
            valor_das_estimado=round(valor_das, 2),
            explicacao=explicacao
        )
