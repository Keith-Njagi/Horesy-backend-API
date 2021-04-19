import os
import logging
from typing import List
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.logger import logger

from api.endpoints import oauth2_scheme
from models import UserModel, UserRoleModel, RoleModel
from schemas.schemas import User_Pydantic, UserRole_Pydantic, Role_Pydantic
from configs.base_config import settings

# openssl rand -hex 32 ->to generate random SECRET_KEY
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Encode token
async def encode_token(id:str, role:str):
        is_admin:bool = False
        if role == 'Admin':
            is_admin = True

        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat':datetime.utcnow(),
            'sub':{ 
                'id':id,
                'role':role,
                'claims':{
                    'is_admin':is_admin
                }
            }
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Decode token
async def decode_token( token:str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            print(f'============================== \\n Auth Error: {e} \\n ==============================')
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

# Use ID provided by decode_token to get Current User from DB
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = await decode_token(token)
    user = await UserModel.get(id=payload.get('id'))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User_Pydantic = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_user_role(token: str = Depends(oauth2_scheme)):
    payload = await decode_token(token)
    # role = payload.get('role')
    user_role =  await UserRoleModel.get(user_id=payload.get('id'))
    role_item = await RoleModel.get(id=user_role.role_id)
    role = role_item.role
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return role

async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    return token

class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User_Pydantic = Depends(get_current_active_user), role: str = Depends(get_current_user_role)):
        if role not in self.allowed_roles:
            logger.debug(f"User with role {role} not in {self.allowed_roles}")
            # print(f"User with role {role} not in {self.allowed_roles}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorised to use this resource")

