import requests
from fastapi import APIRouter, Depends, HTTPException, status

from passlib.hash import bcrypt
from models import BookingModel, RoomModel, UserModel
from schemas.schemas import Booking_Pydantic, BookingIn_Pydantic, User_Pydantic, Role_Pydantic, Room_Pydantic, Booking
from utilities.auth import get_current_user, get_current_user_role

router = APIRouter(prefix='/api/bookings', tags=["bookings"])
# CRUD FOR BOOKINGS

@router.get('/')
async def get_bookings(current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    return await Booking_Pydantic.from_queryset(BookingModel.all())

@router.post('/')
async def post_booking(booking: Booking):
    user_email = booking.email
    usr_by_email = await UserModel.filter(email=user_email)
    
    user_id = 0
    if len(usr_by_email) == 0:
        auth_detail = {
            "full_name": booking.full_name,
            "email": user_email,
            "phone": booking.phone
        }
        hashed_password = bcrypt.hash(booking.phone)
        new_usr = await UserModel.create(**auth_detail, password_hash=hashed_password)
        user_id = new_usr.id
    
    if len(usr_by_email) != 0:
        user_id = usr_by_email[0].id

    booking_by_date_from = await BookingModel.filter(date_from=booking.date_from)
    if len(booking_by_date_from):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The chosen day has been booked')

    obj = await BookingModel.create(room_id=booking.room_id, user_id=user_id, date_from=booking.date_from, date_to=booking.date_to)
    await RoomModel.filter(id=booking.room_id).update(is_booked=True)
    return await Booking_Pydantic.from_tortoise_orm(obj)

@router.get('/{id}')
async def get_single_booking(id:int):
    booking = await BookingModel.get(id=id)
    if booking:
        return await Booking_Pydantic.from_tortoise_orm(booking)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Booking {id} does not exist')


@router.put('/{id}')
async def update_booking(id: int,booking: BookingIn_Pydantic, current_user:User_Pydantic=Depends(get_current_user)):
    obj = await BookingModel.filter(id=id).update(**booking.dict())
    return await Booking_Pydantic.from_tortoise_orm(obj)


@router.delete('/{id}')
async def delete_booking(id:int, current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    deleted = await BookingModel.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Booking {id} not found')
    return JSONResponse(status_code=status.HTTP_200_OK, content='Deleted booking {id}')

@router.get('/calendar')
async def get_calendar_bookings(current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    return await Booking_Pydantic.from_queryset(BookingModel.all())