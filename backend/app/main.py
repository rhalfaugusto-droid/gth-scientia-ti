from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Any
from . import db
from .auth import authenticate_user, create_access_token, get_current_user, get_password_hash, require_admin
import xmltodict

app = FastAPI(title='GTH - Full Deploy API')

class FlowPayload(BaseModel):
    nodes: Any
    edges: Any

class XmlPayload(BaseModel):
    xml: str

class TokenRequest(BaseModel):
    username: str
    password: str

class CreateUser(BaseModel):
    username: str
    password: str
    tenant_name: str = 'default'
    is_admin: bool = False

@app.on_event('startup')
async def startup():
    await db.database.connect()
    db.metadata.create_all(db.engine)
    # seed default tenant and admin user
    t = await db.database.fetch_one(db.tenants.select().where(db.tenants.c.name=='default'))
    if not t:
        await db.database.execute(db.tenants.insert().values(name='default'))
        t = await db.database.fetch_one(db.tenants.select().where(db.tenants.c.name=='default'))
    u = await db.database.fetch_one(db.users.select().where(db.users.c.username=='admin'))
    if not u:
        pw = get_password_hash('admin123')
        await db.database.execute(db.users.insert().values(username='admin', password_hash=pw, tenant_id=t['id'], is_admin=True))

@app.on_event('shutdown')
async def shutdown():
    await db.database.disconnect()

@app.post('/token')
async def token(req: TokenRequest):
    user = await authenticate_user(req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = create_access_token({'sub': user['username'], 'tenant_id': user['tenant_id']})
    return {'access_token': access, 'token_type': 'bearer'}

@app.post('/admin/create-user')
async def admin_create_user(req: CreateUser, admin_user = Depends(require_admin)):
    t = await db.database.fetch_one(db.tenants.select().where(db.tenants.c.name==req.tenant_name))
    if not t:
        await db.database.execute(db.tenants.insert().values(name=req.tenant_name))
        t = await db.database.fetch_one(db.tenants.select().where(db.tenants.c.name==req.tenant_name))
    pw_hash = get_password_hash(req.password)
    await db.database.execute(db.users.insert().values(username=req.username, password_hash=pw_hash, tenant_id=t['id'], is_admin=req.is_admin))
    return {'status':'created'}

@app.post('/flow/save')
async def save_flow(payload: FlowPayload, current_user: Any = Depends(get_current_user)):
    tenant_id = current_user['tenant_id']
    name = payload.nodes[0].get('data',{}).get('label','Fluxo sem nome') if payload.nodes else 'Fluxo'
    rec = {'tenant_id': tenant_id, 'name': name, 'data': {'nodes': payload.nodes, 'edges': payload.edges}}
    await db.database.execute(db.flows.insert().values(**rec))
    return {'status':'saved'}

@app.get('/flows')
async def list_flows(current_user: Any = Depends(get_current_user)):
    tenant_id = current_user['tenant_id']
    rows = await db.database.fetch_all(db.flows.select().where(db.flows.c.tenant_id==tenant_id))
    return [{'id': r['id'], 'name': r['name']} for r in rows]

@app.get('/flow/{flow_id}')
async def get_flow(flow_id: int, current_user: Any = Depends(get_current_user)):
    tenant_id = current_user['tenant_id']
    row = await db.database.fetch_one(db.flows.select().where((db.flows.c.tenant_id==tenant_id) & (db.flows.c.id==flow_id)))
    if not row:
        raise HTTPException(status_code=404, detail='Not found')
    return row['data']

@app.post('/flow/run')
async def run_flow(payload: FlowPayload, current_user: Any = Depends(get_current_user)):
    result = []
    for node in payload.nodes:
        label = node.get('data', {}).get('label', 'nó')
        props = node.get('data', {}).get('props', {})
        if 'import' in label.lower():
            parsed = props.get('xml_parsed') or {}
            result.append({'node': label, 'output': {'parsed': parsed}})
        elif 'calc' in label.lower() or 'calc_trib' in label.lower():
            result.append({'node': label, 'output': {'icms_old': 1800, 'icms_new': 1500}})
        elif 'email' in label.lower():
            result.append({'node': label, 'output': {'sent': True}})
        else:
            result.append({'node': label, 'output': {'ok': True}})
    return {'status': 'ran', 'result': result}

@app.post('/parse/xml')
async def parse_xml(payload: XmlPayload, current_user: Any = Depends(get_current_user)):
    xml_text = payload.xml
    try:
        obj = xmltodict.parse(xml_text, force_list=('det', 'prod'))
        infNFe = None
        if 'nfeProc' in obj:
            infNFe = obj['nfeProc'].get('NFe', {}).get('infNFe')
        elif 'NFe' in obj:
            nfe = obj.get('NFe')
            if isinstance(nfe, dict) and 'infNFe' in nfe:
                infNFe = nfe['infNFe']
        if not infNFe:
            for v in obj.values():
                if isinstance(v, dict) and 'infNFe' in v:
                    infNFe = v['infNFe']
                    break
        parsed = {'chave': None, 'totals': {}, 'items': []}
        if infNFe:
            chave = infNFe.get('@Id') or infNFe.get('@Id')
            if chave and chave.startswith('NFe'):
                chave = chave[3:]
            parsed['chave'] = chave
            total = infNFe.get('total', {}) if isinstance(infNFe.get('total', {}), dict) else {}
            icmstot = total.get('ICMSTot') or total.get('ICMSTot', {})
            vNF = icmstot.get('vNF') if isinstance(icmstot, dict) else None
            parsed['totals']['vNF'] = vNF
            emit = infNFe.get('emit', {})
            ender = emit.get('enderEmit', {}) if isinstance(emit, dict) else {}
            parsed['emit_state'] = ender.get('UF') or None
            dets = infNFe.get('det') or []
            for det in dets:
                prod = det.get('prod') or {}
                cProd = prod.get('cProd') or ''
                xProd = prod.get('xProd') or ''
                CFOP = prod.get('CFOP') or ''
                vProd = prod.get('vProd') or ''
                parsed['items'].append({'cProd': cProd, 'xProd': xProd, 'CFOP': CFOP, 'vProd': vProd})
        return {'status':'ok', 'parsed': parsed}
    except Exception as e:
        return {'status':'error', 'error': str(e)}

@app.post('/validate/nfe')
async def validate_endpoint(payload: XmlPayload, current_user: Any = Depends(get_current_user)):
    parsed_resp = await parse_xml(payload, current_user=current_user)
    if parsed_resp.get('status') != 'ok':
        raise HTTPException(status_code=400, detail='Invalid XML')
    parsed = parsed_resp.get('parsed')
    from .validate import validate_nfe
    result = validate_nfe(parsed)
    return {'status':'ok', 'validation': result}
