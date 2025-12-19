from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, companies, rules, engine, admin, xml_parser, tax_simulation

app = FastAPI(title='GTH FastAPI Backend POC')

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(users.router, prefix='/users', tags=['users'])
app.include_router(companies.router, prefix='/companies', tags=['companies'])
app.include_router(rules.router, prefix='/rules', tags=['rules'])
app.include_router(engine.router, prefix='/engine', tags=['engine'])
app.include_router(admin.router, prefix='/admin', tags=['admin'])
app.include_router(xml_parser.router, prefix='/parser', tags=['parser'])
app.include_router(tax_simulation.router, prefix='/simulation', tags=['simulation'])

@app.get('/')
def root():
    return {'msg':'GTH FastAPI Backend POC'}

from routers import workflows
app.include_router(workflows.router, prefix='/workflows', tags=['workflows'])

