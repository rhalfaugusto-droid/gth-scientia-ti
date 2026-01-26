from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from backend_fastapi.services.xml_parser_service import parse_nfe_xml
from backend_fastapi.services.tax_service import calculate_tax
from backend_fastapi.dependencies import get_current_user
from backend_fastapi import database, crud

router = APIRouter()

class WorkflowIn(BaseModel):
    name: str
    data: dict

class WorkflowOut(BaseModel):
    id: int
    name: str
    owner_email: Optional[str]
    data: dict

    class Config:
        orm_mode = True

@router.post("/", response_model=WorkflowOut)
def create_workflow(payload: WorkflowIn, db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    owner = current.email
    wf = crud.create_workflow(db, payload.name, owner, payload.data)
    return wf

@router.get("/", response_model=list[WorkflowOut])
def list_workflows(db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    owner = current.email
    return crud.get_workflows_by_owner(db, owner)

@router.get("/{wf_id}", response_model=WorkflowOut)
def get_workflow(wf_id: int, db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    wf = crud.get_workflow(db, wf_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if wf.owner_email != current.email:
        raise HTTPException(status_code=403, detail="Forbidden")
    return wf

@router.put("/{wf_id}", response_model=WorkflowOut)
def update_workflow(wf_id: int, payload: WorkflowIn, db: Session = Depends(database.get_db), current = Depends(get_current_user)):
    wf = crud.get_workflow(db, wf_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if wf.owner_email != current.email:
        raise HTTPException(status_code=403, detail="Forbidden")
    updated = crud.update_workflow(db, wf_id, payload.data, payload.name)
    return updated
