from typing import Optional

from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from models import UserModel, RoleModel, UserRoleModel, RoomTypeModel, RoomModel, BookingModel, PaymentModel


Tortoise.init_models(["models"], "models")
Tortoise._init_timezone(use_tz=True, timezone='Africa/Nairobi')

# class AuthDetail(BaseModel):
#     username: str
#     password: str

User_Pydantic = pydantic_model_creator(UserModel, name="User")
UserIn_Pydantic = pydantic_model_creator(UserModel, name="UserIn", exclude_readonly=True)

class UserIn(UserIn_Pydantic):
    password: str

class Password(BaseModel):
    password:str

Role_Pydantic = pydantic_model_creator(RoleModel, name="Role")
RoleIn_Pydantic = pydantic_model_creator(RoleModel, name="RoleIn", exclude_readonly=True)

RoomType_Pydantic = pydantic_model_creator(RoomTypeModel, name="RoomType")
RoomTypeIn_Pydantic = pydantic_model_creator(RoomTypeModel, name="RoomTypeIn", exclude_readonly=True)

Room_Pydantic = pydantic_model_creator(RoomModel, name="Room")
RoomIn_Pydantic = pydantic_model_creator(RoomModel, name="RoomIn", exclude_readonly=True)


UserRole_Pydantic = pydantic_model_creator(UserRoleModel, name="UserRole")
UserRoleIn_Pydantic = pydantic_model_creator(UserRoleModel, name="UserRoleIn", exclude_readonly=True)


Booking_Pydantic = pydantic_model_creator(BookingModel, name="Booking")
BookingIn_Pydantic = pydantic_model_creator(BookingModel, name="BookingIn", exclude_readonly=True)

Payment_Pydantic = pydantic_model_creator(PaymentModel, name="Payment")
PaymentIn_Pydantic = pydantic_model_creator(PaymentModel, name="PaymentIn", exclude_readonly=True)