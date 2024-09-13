from typing import Dict, Optional, List
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Header, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

import config
from utils.agendor import AgendorAPI  # Certifique-se de que o caminho está correto

app = FastAPI(
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        422: {"description": "Internal server error"},
        405: {"description": "Not found"},
    },
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

def get_token_header(token: str = Header("", alias="VideoAI-Authorization")):
    if token != config.SERVICE_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid token")

    return token

api_router = APIRouter(prefix='/api/agendor', tags=['agendor'], dependencies=[Depends(get_token_header)])
contact_router = APIRouter(prefix='/contact', tags=['contact'])
deal_router = APIRouter(prefix='/deal', tags=['deal'])

agendor_api = AgendorAPI()

class Contact(BaseModel):
    name: str
    phone: str
    responsible: str
    cpf: Optional[str] = None
    organization: Optional[int] = None
    role: Optional[str] = None
    ranking: Optional[int] = None
    description: Optional[str] = None
    birthday: Optional[str] = None
    email: Optional[str] = None
    work: Optional[str] = None
    mobile: Optional[str] = None
    fax: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    instagram: Optional[str] = None
    linked_in: Optional[str] = None
    skype: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[int] = None
    additional_info: Optional[str] = None
    city: Optional[int] = None
    leadOrigin: Optional[int] = None
    category: Optional[int] = None
    products: Optional[List[int]] = None
    allowedUsers: Optional[List[int]] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[Dict[str, any]] = None

class ContactUpdate(BaseModel):
    person_id: int
    name: Optional[str] = None
    cpf: Optional[str] = None
    organization: Optional[int] = None
    role: Optional[str] = None
    ranking: Optional[int] = None
    description: Optional[str] = None
    birthday: Optional[str] = None
    ownerUser: Optional[int] = None
    email: Optional[str] = None
    work: Optional[str] = None
    mobile: Optional[str] = None
    fax: Optional[str] = None
    whatsapp: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    instagram: Optional[str] = None
    linked_in: Optional[str] = None
    skype: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[int] = None
    additional_info: Optional[str] = None
    city: Optional[int] = None
    leadOrigin: Optional[int] = None
    category: Optional[int] = None
    products: Optional[List[int]] = None
    allowedUsers: Optional[List[int]] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[Dict[str, any]] = None

class Deal(BaseModel):
    entity_type: str = Field("people", const=True)
    entity_id: int
    title: str
    dealStatusText: Optional[str] = None
    description: Optional[str] = None
    endTime: Optional[str] = None
    products_entities: Optional[List[Dict[str, any]]] = None
    products: Optional[List[str]] = None
    ranking: Optional[int] = None
    startTime: Optional[str] = None
    ownerUser: Optional[int] = None
    funnel_id: Optional[int] = None
    dealStage: Optional[int] = None
    value: Optional[float] = None
    allowedUsers: Optional[List[int]] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[Dict[str, any]] = None

class DealUpdate(BaseModel):
    deal_id: int
    value: Optional[float] = None
    description: Optional[str] = None
    startTime: Optional[str] = None
    products_entities: Optional[List[Dict[str, any]]] = None
    products: Optional[List[str]] = None
    ownerUser: Optional[int] = None
    allowedUsers: Optional[List[int]] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[Dict[str, any]] = None

class DealStageUpdate(BaseModel):
    deal_id: int
    deal_stage: int  # Deve ser um inteiro

class DealStatusUpdate(BaseModel):
    deal_id: int
    deal_status_text: str

@contact_router.post("/create")
def create_contact(contact: Contact):
    try:
        # Obter o ID do responsável a partir do nome
        responsible_id = agendor_api.get_responsible_id(contact.responsible)
        if not responsible_id:
            raise HTTPException(status_code=404, detail="Responsible not found")

        contact_data = contact.dict(exclude_unset=True)
        contact_data.pop("responsible")  # Remover o campo 'responsible' que não é usado diretamente

        # Chamar o método da API
        new_person = agendor_api.create_new_person(
            name=contact.name,
            phone=contact.phone,
            responsible_id=responsible_id,
            **contact_data
        )
        return new_person
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@contact_router.get("/find/{phone}")
def find_contact(phone: str):
    try:
        # Usando o método list_person com filtro
        persons = agendor_api.list_person(per_page=100, phone=phone)
        if not persons:
            raise HTTPException(status_code=404, detail="Contact not found")
        return persons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@contact_router.put("/update")
def update_contact(contact_update: ContactUpdate):
    try:
        update_data = contact_update.dict(exclude_unset=True)
        person_id = update_data.pop("person_id")

        updated_person = agendor_api.update_person(person_id, **update_data)
        return updated_person
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@deal_router.post("/create-deal")
def create_deal(deal: Deal):
    try:
        deal_data = deal.dict(exclude_unset=True)
        new_deal = agendor_api.create_new_deal(**deal_data)
        return new_deal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@deal_router.get("/find-deal/{entity_type}/{entity_id}")
def find_deal(entity_type: str, entity_id: int):
    try:
        if entity_type not in ["people", "organizations"]:
            raise HTTPException(status_code=400, detail="Invalid entity_type. Must be 'people' or 'organizations'")
        deals = agendor_api.list_deals(entity_type=entity_type, entity_id=entity_id)
        if not deals:
            raise HTTPException(status_code=404, detail="Deals not found")
        return deals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@deal_router.put("/update")
def update_deal(deal_update: DealUpdate):
    try:
        update_data = deal_update.dict(exclude_unset=True)
        deal_id = update_data.pop("deal_id")

        updated_deal = agendor_api.update_deal(deal_id, **update_data)
        return updated_deal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@deal_router.put("/stage")
def update_deal_stage(deal_stage_update: DealStageUpdate):
    try:
        updated_deal = agendor_api.update_deal_stage(
            deal_id=deal_stage_update.deal_id,
            deal_stage=deal_stage_update.deal_stage
        )
        return updated_deal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@deal_router.put("/status")
def update_deal_status(deal_status_update: DealStatusUpdate):
    try:
        updated_deal = agendor_api.update_deal_status(
            deal_id=deal_status_update.deal_id,
            deal_status_text=deal_status_update.deal_status_text
        )
        return updated_deal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

api_router.include_router(contact_router)
api_router.include_router(deal_router)
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)