from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from src.domain.entities import ContactStatus


class OperatorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True
    max_load: int = Field(default=10, ge=1)


class OperatorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    max_load: Optional[int] = Field(None, ge=1)


class OperatorResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    max_load: int
    current_load: int

    class Config:
        from_attributes = True


class SourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True


class SourceResponse(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True


class OperatorSourceCreate(BaseModel):
    operator_id: int
    weight: int = Field(default=1, ge=1)


class OperatorSourceResponse(BaseModel):
    operator_id: int
    source_id: int
    weight: int

    class Config:
        from_attributes = True


class SourceDistributionResponse(BaseModel):
    source: SourceResponse
    operators: List[OperatorSourceResponse]


class LeadResponse(BaseModel):
    id: int
    external_id: str
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    external_lead_id: str = Field(..., description="external lead's id")
    source_id: int
    message: Optional[str] = None
    lead_name: Optional[str] = None


class ContactResponse(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: Optional[int]
    status: ContactStatus
    message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ContactDetailResponse(BaseModel):
    contact: ContactResponse
    lead: LeadResponse
    operator: Optional[OperatorResponse]


class LeadWithContactsResponse(BaseModel):
    lead: LeadResponse
    contacts: List[ContactResponse]
