from uuid import UUID, uuid4
from app.domain.orm_base import OrmBase
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class User(OrmBase):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String())
