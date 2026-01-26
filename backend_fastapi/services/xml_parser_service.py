from lxml import etree
from typing import Dict, Any, Optional


def parse_nfe_xml(xml_content: str) -> Optional[Dict[str, Any]]:
    """
    Analisa o conteúdo XML de uma Nota Fiscal Eletrônica (NFe) e extrai dados relevantes.

    Args:
        xml_content: String contendo o XML da NFe.

    Returns:
        Um dicionário com os dados extraídos ou None em caso de erro.
    """
    try:
        # 1. Parsing do XML
        root = etree.fromstring(xml_content.encode("utf-8"))

        # 2. Namespace da NFe
        ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}

        # 3. Identificação
        ide_node = root.find(".//nfe:ide", namespaces=ns)
        emit_node = root.find(".//nfe:emit", namespaces=ns)
        dest_node = root.find(".//nfe:dest", namespaces=ns)

        if ide_node is None or emit_node is None or dest_node is None:
            return None

        # 4. Totais
        vICMS = root.find(".//nfe:ICMSTot/nfe:vICMS", namespaces=ns)
        vPIS = root.find(".//nfe:ICMSTot/nfe:vPIS", namespaces=ns)
        vCOFINS = root.find(".//nfe:ICMSTot/nfe:vCOFINS", namespaces=ns)
        vProd = root.find(".//nfe:ICMSTot/nfe:vProd", namespaces=ns)
        vNF = root.find(".//nfe:ICMSTot/nfe:vNF", namespaces=ns)

        # 5. Itens
        items = []
        for det_node in root.findall(".//nfe:det", namespaces=ns):
            prod_node = det_node.find("nfe:prod", namespaces=ns)
            imposto_node = det_node.find("nfe:imposto", namespaces=ns)

            item_data = {
                "cProd": prod_node.find("nfe:cProd", namespaces=ns).text if prod_node is not None else None,
                "xProd": prod_node.find("nfe:xProd", namespaces=ns).text if prod_node is not None else None,
                "qCom": float(prod_node.find("nfe:qCom", namespaces=ns).text)
                if prod_node is not None and prod_node.find("nfe:qCom", namespaces=ns) is not None else 0.0,
                "vUnCom": float(prod_node.find("nfe:vUnCom", namespaces=ns).text)
                if prod_node is not None and prod_node.find("nfe:vUnCom", namespaces=ns) is not None else 0.0,
                "vProd": float(prod_node.find("nfe:vProd", namespaces=ns).text)
                if prod_node is not None and prod_node.find("nfe:vProd", namespaces=ns) is not None else 0.0,
                "NCM": prod_node.find("nfe:NCM", namespaces=ns).text if prod_node is not None else None,
                "CST_ICMS": imposto_node.find(".//nfe:ICMS/*/nfe:CST", namespaces=ns).text
                if imposto_node is not None else None,
                "vICMS": float(imposto_node.find(".//nfe:ICMS/*/nfe:vICMS", namespaces=ns).text)
                if imposto_node is not None and imposto_node.find(".//nfe:ICMS/*/nfe:vICMS", namespaces=ns) is not None else 0.0,
            }

            items.append(item_data)

        inf_nfe = root.find(".//nfe:infNFe", namespaces=ns)

        extracted_data = {
            "nfe_id": inf_nfe.get("Id"),
            "chave_acesso": inf_nfe.get("Id")[3:],
            "data_emissao": ide_node.find("nfe:dhEmi", namespaces=ns).text
            if ide_node.find("nfe:dhEmi", namespaces=ns) is not None
            else ide_node.find("nfe:dEmi", namespaces=ns).text,
            "emitente": {
                "CNPJ": emit_node.find("nfe:CNPJ", namespaces=ns).text,
                "xNome": emit_node.find("nfe:xNome", namespaces=ns).text,
                "UF": emit_node.find(".//nfe:enderEmit/nfe:UF", namespaces=ns).text,
            },
            "destinatario": {
                "CNPJ": dest_node.find("nfe:CNPJ", namespaces=ns).text
                if dest_node.find("nfe:CNPJ", namespaces=ns) is not None
                else dest_node.find("nfe:CPF", namespaces=ns).text,
                "xNome": dest_node.find("nfe:xNome", namespaces=ns).text,
                "UF": dest_node.find(".//nfe:enderDest/nfe:UF", namespaces=ns).text,
            },
            "totais": {
                "vICMS": float(vICMS.text) if vICMS is not None else 0.0,
                "vPIS": float(vPIS.text) if vPIS is not None else 0.0,
                "vCOFINS": float(vCOFINS.text) if vCOFINS is not None else 0.0,
                "vProd": float(vProd.text) if vProd is not None else 0.0,
                "vNF": float(vNF.text) if vNF is not None else 0.0,
            },
            "itens": items,
        }

        return extracted_data

    except etree.XMLSyntaxError as e:
        print(f"Erro de sintaxe XML: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar XML: {e}")
        return None
