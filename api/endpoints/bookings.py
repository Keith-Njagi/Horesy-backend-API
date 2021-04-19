from fastapi import APIRouter, Depends

from models import BookingModel, RoomModel
from schemas.schemas import Booking_Pydantic, BookingIn_Pydantic, User_Pydantic, Role_Pydantic, Room_Pydantic
from utilities.auth import get_current_user, get_current_user_role

router = APIRouter(prefix='/api/bookings', tags=["bookings"])
# CRUD FOR BOOKINGS

@router.get('/')
async def get_bookings(current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    if current_user_role.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    return await Booking_Pydantic.from_queryset(BookingModel.all())

@router.post('/')
async def post_booking(booking: BookingIn_Pydantic, current_user:User_Pydantic=Depends(get_current_user)):
    obj = await BookingModel.create(**booking.dict, user_id=current_user.id)
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

