import pytest
from httpx import AsyncClient
from app.main import app

SAMPLE_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe">
  <infNFe Id="NFe123" versao="4.00">
    <ide><cNF>123</cNF></ide>
    <emit><enderEmit><UF>SP</UF></enderEmit></emit>
    <det>
      <prod><cProd>1</cProd><xProd>Produto A</xProd><CFOP>5102</CFOP><vProd>100.00</vProd></prod>
    </det>
    <total><ICMSTot><vNF>100.00</vNF></ICMSTot></total>
  </infNFe>
</NFe>'''

@pytest.mark.asyncio
async def test_parse_validate():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        resp = await ac.post('/parse/xml', json={'xml': SAMPLE_XML})
        assert resp.status_code == 200
        data = resp.json()
        assert data['status'] == 'ok'
        parsed = data['parsed']
        assert parsed['totals']['vNF'] == '100.00' or float(parsed['totals']['vNF']) == 100.0
        # validate
        v = await ac.post('/validate/nfe', json={'xml': SAMPLE_XML})
        assert v.status_code == 200
        assert v.json()['status'] == 'ok'
