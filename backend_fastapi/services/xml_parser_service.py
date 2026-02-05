from lxml import etree
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def _safe_text(node):
    return node.text if node is not None and node.text else None


def _safe_float(node):
    try:
        return float(node.text) if node is not None and node.text else 0.0
    except ValueError:
        return 0.0


def parse_nfe_xml(xml_content: str) -> Optional[Dict[str, Any]]:
    """
    Parser seguro de NFe XML.
    Resistente a:
    - campos ausentes
    - XML inválido
    - valores vazios
    """

    try:
        # parser seguro contra XXE
        parser = etree.XMLParser(resolve_entities=False)
        root = etree.fromstring(xml_content.encode("utf-8"), parser)

        ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

        ide_node = root.find(".//nfe:ide", namespaces=ns)
        emit_node = root.find(".//nfe:emit", namespaces=ns)
        dest_node = root.find(".//nfe:dest", namespaces=ns)

        if not all([ide_node, emit_node, dest_node]):
            return None

        # -----------------
        # Totais
        # -----------------
        vICMS = root.find(".//nfe:ICMSTot/nfe:vICMS", namespaces=ns)
        vPIS = root.find(".//nfe:ICMSTot/nfe:vPIS", namespaces=ns)
        vCOFINS = root.find(".//nfe:ICMSTot/nfe:vCOFINS", namespaces=ns)
        vProd = root.find(".//nfe:ICMSTot/nfe:vProd", namespaces=ns)
        vNF = root.find(".//nfe:ICMSTot/nfe:vNF", namespaces=ns)

        # -----------------
        # Itens
        # -----------------
        items = []

        for det_node in root.findall(".//nfe:det", namespaces=ns):
            prod_node = det_node.find("nfe:prod", namespaces=ns)
            imposto_node = det_node.find("nfe:imposto", namespaces=ns)

            item_data = {
                "cProd": _safe_text(prod_node.find("nfe:cProd", namespaces=ns)) if prod_node is not None else None,
                "xProd": _safe_text(prod_node.find("nfe:xProd", namespaces=ns)) if prod_node is not None else None,
                "qCom": _safe_float(prod_node.find("nfe:qCom", namespaces=ns)) if prod_node is not None else 0.0,
                "vUnCom": _safe_float(prod_node.find("nfe:vUnCom", namespaces=ns)) if prod_node is not None else 0.0,
                "vProd": _safe_float(prod_node.find("nfe:vProd", namespaces=ns)) if prod_node is not None else 0.0,
                "NCM": _safe_text(prod_node.find("nfe:NCM", namespaces=ns)) if prod_node is not None else None,
                "CST_ICMS": _safe_text(
                    imposto_node.find(".//nfe:ICMS/*/nfe:CST", namespaces=ns)
                ) if imposto_node is not None else None,
                "vICMS": _safe_float(
                    imposto_node.find(".//nfe:ICMS/*/nfe:vICMS", namespaces=ns)
                ) if imposto_node is not None else 0.0,
            }

            items.append(item_data)

        inf_nfe = root.find(".//nfe:infNFe", namespaces=ns)

        return {
            "nfe_id": inf_nfe.get("Id") if inf_nfe is not None else None,
            "chave_acesso": inf_nfe.get("Id")[3:] if inf_nfe is not None else None,
            "data_emissao": _safe_text(
                ide_node.find("nfe:dhEmi", namespaces=ns)
                or ide_node.find("nfe:dEmi", namespaces=ns)
            ),
            "emitente": {
                "CNPJ": _safe_text(emit_node.find("nfe:CNPJ", namespaces=ns)),
                "xNome": _safe_text(emit_node.find("nfe:xNome", namespaces=ns)),
                "UF": _safe_text(emit_node.find(".//nfe:enderEmit/nfe:UF", namespaces=ns)),
            },
            "destinatario": {
                "CNPJ": _safe_text(
                    dest_node.find("nfe:CNPJ", namespaces=ns)
                    or dest_node.find("nfe:CPF", namespaces=ns)
                ),
                "xNome": _safe_text(dest_node.find("nfe:xNome", namespaces=ns)),
                "UF": _safe_text(dest_node.find(".//nfe:enderDest/nfe:UF", namespaces=ns)),
            },
            "totais": {
                "vICMS": _safe_float(vICMS),
                "vPIS": _safe_float(vPIS),
                "vCOFINS": _safe_float(vCOFINS),
                "vProd": _safe_float(vProd),
                "vNF": _safe_float(vNF),
            },
            "itens": items,
        }

    except Exception:
        logger.exception("Erro ao processar XML da NFe")
        return None
