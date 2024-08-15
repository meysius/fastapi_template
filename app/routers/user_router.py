from fastapi import APIRouter
from app.domain.auth.schemas.user_schemas import UserCreate, UserOut
from app.domain.auth.auth_service import AuthServiceDep
from app.domain.auth.models.user import User

router = APIRouter()


@router.get("/users", response_model=list[UserOut])
async def list_users(auth_service: AuthServiceDep) -> list[User]:
    return await auth_service.list_users()


@router.post("/users", response_model=UserOut)
async def create_user(user_create: UserCreate, auth_service: AuthServiceDep) -> User:
    return await auth_service.create_user(user_create)
