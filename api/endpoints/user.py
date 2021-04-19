import os

import requests
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse
from starlette.requests import Request

from . import conf
from models import UserModel, ActivationTokenModel
from schemas.auth import  User_Pydantic, UserIn_Pydantic
from utilities.auth import RoleChecker, get_current_user, get_current_user_token

router = APIRouter(prefix='/api/usr', tags=["user"])


@router.put('/update/', status_code=status.HTTP_200_OK,)
async def update_user(user: UserIn_Pydantic, current_user: User_Pydantic = Depends(get_current_user)) -> JSONResponse:
    obj = await UserModel.filter(id=current_user.id).update(full_name=user.full_name, email=user.email, phone=user.phone)
    return JSONResponse(status_code=status.HTTP_200_OK, content='User Updated')

@router.put('/disable/account', status_code=status.HTTP_200_OK)
async def deactivate_account(current_user:User_Pydantic = Depends(get_current_user)) -> JSONResponse:
    await UserModel.filter(id=current_user.id).update(disabled=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content='Disabled account')

@router.post('/activate/account', status_code=status.HTTP_200_OK)
async def activate_account(current_user:User_Pydantic = Depends(get_current_user)) -> JSONResponse:
    await UserModel.filter(id=current_user.id).update(disabled=False)
    return JSONResponse(status_code=status.HTTP_200_OK, content='User account activated')
