from fastapi import Depends
from typing import Annotated
from app.domain.auth.models.user import User
from app.domain.auth.schemas.user_schemas import UserCreate
from app.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class AuthService:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def list_users(self) -> list[User]:
        async with self.session.begin_nested():
            users = await self.session.scalars(select(User))
            return list(users.all())

    async def create_user(self, user_create: UserCreate) -> User:
        user = User(
            email=user_create.email, password_hash=f"hash of: {user_create.password}"
        )
        async with self.session.begin_nested():
            self.session.add(user)
            return user


AuthServiceDep = Annotated[AuthService, Depends(AuthService)]
