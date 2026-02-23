import enum
import uuid
from datetime import datetime, date

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class InventoryType(str, enum.Enum):
    FEED = 'FEED'
    INPUT = 'INPUT'
    VACCINE = 'VACCINE'


class MovementType(str, enum.Enum):
    IN = 'IN'
    OUT = 'OUT'


class ScheduleType(str, enum.Enum):
    PAYROLL = 'PAYROLL'
    RESTOCK = 'RESTOCK'
    VACCINE_REMINDER = 'VACCINE_REMINDER'
    CUSTOM = 'CUSTOM'


class AlertSeverity(str, enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class AlertStatus(str, enum.Enum):
    OPEN = 'OPEN'
    RESOLVED = 'RESOLVED'


class TaskStatus(str, enum.Enum):
    OPEN = 'OPEN'
    DONE = 'DONE'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Farm(Base):
    __tablename__ = 'farms'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    timezone: Mapped[str] = mapped_column(String(60), default='America/Sao_Paulo')
    currency: Mapped[str] = mapped_column(String(8), default='BRL')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    module: Mapped[str] = mapped_column(String(50), nullable=False)
    can_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_write: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Membership(Base):
    __tablename__ = 'memberships'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roles.id'), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default='ACTIVE', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'farm_id', name='uq_membership_user_farm'),)


class ExpenseCategory(Base):
    __tablename__ = 'expense_categories'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_direct_cost: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Income(Base):
    __tablename__ = 'income'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    attachment_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('amount >= 0', name='ck_income_amount_nonneg'),
        Index('ix_income_farm_date', 'farm_id', 'date'),
        Index('ix_income_farm_created', 'farm_id', 'created_at'),
    )


class Expense(Base):
    __tablename__ = 'expense'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('expense_categories.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    vendor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_unplanned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('amount >= 0', name='ck_expense_amount_nonneg'),
        Index('ix_expense_farm_date', 'farm_id', 'date'),
        Index('ix_expense_farm_created', 'farm_id', 'created_at'),
    )


class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    type: Mapped[InventoryType] = mapped_column(Enum(InventoryType, name='inventory_type'), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    min_level: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    expires_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    __table_args__ = (CheckConstraint('min_level >= 0', name='ck_item_min_level_nonneg'),)


class InventoryMovement(Base):
    __tablename__ = 'inventory_movements'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('inventory_items.id'), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    qty: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    cost_total: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType, name='movement_type'), nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(60), nullable=True)
    reference_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('cost_total >= 0', name='ck_movement_cost_nonneg'),
        Index('ix_movements_farm_date', 'farm_id', 'date'),
    )


class Cattle(Base):
    __tablename__ = 'cattle'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    tag: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    __table_args__ = (UniqueConstraint('tag', 'farm_id', name='uq_cattle_tag_farm'),)


class Vaccination(Base):
    __tablename__ = 'vaccinations'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    cattle_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey('cattle.id'), nullable=True)
    batch_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    vaccine_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('inventory_items.id'), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    dose: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    next_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (CheckConstraint('cost >= 0', name='ck_vacc_cost_nonneg'),)


class Schedule(Base):
    __tablename__ = 'schedules'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    schedule_type: Mapped[ScheduleType] = mapped_column(Enum(ScheduleType, name='schedule_type'), nullable=False)
    rrule: Mapped[str] = mapped_column(String(255), nullable=False)
    next_run_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    payload_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    alert_type: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[AlertSeverity] = mapped_column(Enum(AlertSeverity, name='alert_severity'), nullable=False)
    status: Mapped[AlertStatus] = mapped_column(Enum(AlertStatus, name='alert_status'), nullable=False, default=AlertStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus, name='task_status'), nullable=False, default=TaskStatus.OPEN)
    auto_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    entity: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(80), nullable=False)
    payload_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ip: Mapped[str | None] = mapped_column(String(80), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)


class InviteToken(Base):
    __tablename__ = 'invite_tokens'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roles.id'), nullable=False)
    token: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class SnapshotMonthly(Base):
    __tablename__ = 'snapshot_monthly'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('farms.id'), nullable=False)
    month: Mapped[date] = mapped_column(Date, nullable=False)
    total_income: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    total_expense: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    direct_expense: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    gross_profit: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    net_profit: Mapped[float] = mapped_column(Numeric(14, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint('farm_id', 'month', name='uq_snapshot_farm_month'),)
