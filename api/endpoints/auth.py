from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import HTTPNotFoundError

from models import UserModel, RoleModel, UserRoleModel
from schemas.schemas import  Password, User_Pydantic, UserIn_Pydantic, UserIn, Role_Pydantic, UserRole_Pydantic
from utilities.auth import encode_token
from utilities.user_roles_manager import UserPrivilege

router = APIRouter(prefix='/api/auth', tags=["auth"])

@router.post('/register', status_code=status.HTTP_201_CREATED,  response_model=User_Pydantic)
async def register(auth_detail: UserIn, role: Optional[str]=None):
    if await UserModel.filter(email=auth_detail.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
    if await UserModel.filter(phone=auth_detail.phone):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Phone number already exists')

    hashed_password = bcrypt.hash(auth_detail.password)
    obj = await UserModel.create(**auth_detail.dict(exclude_unset=True), password_hash=hashed_password)

    user = await User_Pydantic.from_tortoise_orm(obj)
    #  Ensure there are roles in Db or insert current roles to DB
    roles = await RoleModel.all()
    all_privileges = UserPrivilege.all_privileges
    if len(roles) == 0:
        for key, value in all_privileges.items():
            new_role = await RoleModel.create(role=value)
            
    # Add User roles
    UserPrivilege.generate_user_role(user_id = user.id)
    user_id = UserPrivilege.user_id
    usr_role = UserPrivilege.role
    
    if role in UserPrivilege.all_privileges.values():
        db_role = await RoleModel.get(role=role)
        new_user_role = await UserRoleModel.create(user_id=user_id, role_id=db_role.id)
    else:     
        new_user_role = await UserRoleModel.create(user_id=user_id, role_id=usr_role)

    return user

# Activation link to redirect to login page

@router.post('/token', status_code=status.HTTP_200_OK)
async def login(auth_form:  OAuth2PasswordRequestForm = Depends()):
    # See if user exists
    email = auth_form.username
    user = await UserModel.get(email=email)            

    if not user or not user.verify_password(password=auth_form.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    user_id = user.id
    user_role = await UserRoleModel.get(user_id=user_id)
    role_id = user_role.role_id
    role_item = await RoleModel.get(id=role_id)
    role = role_item.role

    token = await encode_token(user_id, role)
    
    return {'access_token': token, "token_type": "bearer"}
