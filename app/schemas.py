from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.models import InventoryType, MovementType, ScheduleType, AlertSeverity, AlertStatus


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class FarmCreate(BaseModel):
    name: str
    timezone: str = 'America/Sao_Paulo'
    currency: str = 'BRL'


class FarmOut(BaseModel):
    id: UUID
    name: str
    timezone: str
    currency: str

    class Config:
        from_attributes = True


class IncomeCreate(BaseModel):
    date: date
    description: str
    amount: Decimal = Field(ge=0)
    source: str
    attachment_url: str | None = None


class ExpenseCreate(BaseModel):
    date: date
    category_id: UUID
    description: str
    amount: Decimal = Field(ge=0)
    vendor: str | None = None
    is_unplanned: bool = False


class InventoryItemCreate(BaseModel):
    name: str
    type: InventoryType
    unit: str
    min_level: Decimal = Field(ge=0)
    expires_at: date | None = None


class InventoryMovementCreate(BaseModel):
    item_id: UUID
    date: date
    qty: Decimal
    cost_total: Decimal = Field(ge=0)
    movement_type: MovementType
    reference_type: str | None = None
    reference_id: str | None = None


class CattleCreate(BaseModel):
    tag: str
    birth_date: date | None = None
    notes: str | None = None


class VaccinationCreate(BaseModel):
    cattle_id: UUID | None = None
    batch_id: str | None = None
    vaccine_item_id: UUID
    date: date
    dose: str
    cost: Decimal = Field(ge=0)
    next_due_date: date | None = None


class ScheduleCreate(BaseModel):
    name: str
    schedule_type: ScheduleType
    rrule: str
    next_run_at: datetime
    payload_json: dict | None = None


class AlertOut(BaseModel):
    id: UUID
    title: str
    message: str
    severity: AlertSeverity
    status: AlertStatus

    class Config:
        from_attributes = True
