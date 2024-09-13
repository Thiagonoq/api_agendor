from typing import Dict, Optional
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Header, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

import config
from utils import agendor


app = FastAPI(
    # dependencies=[Depends(get_token_header)],
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
    products: Optional[list] = None
    allowedUsers: Optional[list] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[dict] = None

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
    products: Optional[list] = None
    allowedUsers: Optional[list] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[dict] = None

class Deal(BaseModel):
    person_id: int
    person_name: str
    dealStatusText: Optional[str] = None
    description: Optional[str] = None
    endTime: Optional[str] = None
    products_entities: Optional[list] = None
    products: Optional[list] = None
    ranking: Optional[int] = None
    startTime: Optional[str] = None
    ownerUser: Optional[str] = None
    funnel: Optional[str] = None
    dealStage: Optional[str] = None
    value: Optional[int] = None
    allowedUsers: Optional[list] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[dict] = None

class DealUpdate(BaseModel):
    deal_id: int
    value: Optional[int] = None
    description: Optional[str] = None
    startTime: Optional[str] = None
    products_entities: Optional[list] = None
    products: Optional[list] = None
    ownerUser: Optional[int] = None
    allowedUsers: Optional[list] = None
    allowToAllUsers: Optional[bool] = None
    customFields: Optional[dict] = None

class DealStageUpdate(BaseModel):
    deal_id: int
    deal_stage: str

class DealStatusUpdate(BaseModel):
    deal_id: int
    deal_status_text: str

@contact_router.post("/create")
def create_contact(contact: Contact):
    contact_data = contact.model_dump(exclude_unset=True)
    return agendor.create_new_person(**contact_data)

@contact_router.get("/find/{phone}")
def find_contact(phone: str):
    person = agendor.list_person(phone)
    if not person:
        raise HTTPException(status_code=404, detail="Contact not found")
    return person

@contact_router.put("/person")
def update_contact(contact_update: ContactUpdate):
    update_data = contact_update.model_dump(exclude_unset=True)
    person_id = update_data.pop("person_id")
    return agendor.update_person(person_id, **update_data)

@deal_router.post("/create-deal")
def create_deal(deal: Deal):
    deal_data = deal.model_dump(exclude_unset=True)
    return agendor.create_new_deal(**deal_data)

@deal_router.get("/find-deal/{person_id}")
def find_deal(person_id: int):
    deal = agendor.list_deals(person_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

@deal_router.put("/deal")
def update_deal(deal_update: DealUpdate):
    update_data = deal_update.model_dump(exclude_unset=True)
    deal_id = update_data.pop("deal_id")
    return agendor.update_deal(deal_id, **update_data)

@deal_router.put("/stage")
def update_deal_stage(deal_stage_update: DealStageUpdate):
    return agendor.update_deal_stage(deal_stage_update.deal_id, deal_stage=deal_stage_update.deal_stage)

@deal_router.put("/status")
def update_deal_status(deal_status_update: DealStatusUpdate):
    return agendor.update_deal_status(deal_status_update.deal_id, deal_status_text=deal_status_update.deal_status_text)

api_router.include_router(contact_router)
api_router.include_router(deal_router)
app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)