from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.entities import ContactStatus


class OperatorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True
    max_load: int = Field(default=10, ge=1)


class OperatorUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None
    max_load: int | None = Field(None, ge=1)


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
    operators: list[OperatorSourceResponse]


class LeadResponse(BaseModel):
    id: int
    external_id: str
    name: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    external_lead_id: str = Field(..., description="external lead's id")
    source_id: int
    message: str | None = None
    lead_name: str | None = None


class ContactResponse(BaseModel):
    id: int
    lead_id: int
    source_id: int
    operator_id: int | None
    status: ContactStatus
    message: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ContactDetailResponse(BaseModel):
    contact: ContactResponse
    lead: LeadResponse
    operator: OperatorResponse | None


class LeadWithContactsResponse(BaseModel):
    lead: LeadResponse
    contacts: list[ContactResponse]
