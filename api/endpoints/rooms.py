from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from models import RoomTypeModel, RoomModel
from schemas.schemas import RoomType_Pydantic, RoomTypeIn_Pydantic, Room_Pydantic, RoomIn_Pydantic, Role_Pydantic
from utilities.auth import get_current_user_role
from typing import List

router = APIRouter(prefix='/api/rooms', tags=["rooms"])
# CRUD FOR ROOMS AND ROOM TYPES

@router.get('/',response_model=List[Room_Pydantic])
async def get_rooms():
    # return await Room_Pydantic.from_queryset(RoomModel.all())
    return await Room_Pydantic.from_queryset(RoomModel.filter(is_booked=False))

@router.post('/', response_model=Room_Pydantic)
async def post_room(room: RoomIn_Pydantic, current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomModel.create(**room.dict(exclude_unset=True))
    return await Room_Pydantic.from_tortoise_orm(obj)

@router.post('/')
async def post_room(room: RoomIn_Pydantic, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomModel.create(**room.dict(exclude_unset=True))
    return await Room_Pydantic.from_tortoise_orm(obj)

@router.get('/{id}')
async def get_single_room(id:int):
    room = await RoomModel.get(id=id)
    if room:
        return await Room_Pydantic.from_tortoise_orm(room)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room {id} does not exist')

@router.put('/{id}')
async def unbook_room(id: int, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomModel.filter(id=id).update(is_booked=False)
    return await Room_Pydantic.from_tortoise_orm(obj)

@router.delete('/{id}')
async def delete_room(id:int, current_user_role:str=Depends(get_current_user_role)) -> JSONResponse:
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    deleted = await RoomTypeModel.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room type {id} not found')
    return JSONResponse(status_code=status.HTTP_200_OK, content='Deleted room type {id}')




@router.get('/types/all')
async def get_types():
    # return "Hello"
    return await RoomType_Pydantic.from_queryset(RoomTypeModel.all())


@router.get('/types', response_model=List[RoomType_Pydantic])
async def get_room_types():
    return await RoomType_Pydantic.from_queryset(RoomTypeModel.all())
    # return await RoomType_Pydantic.from_tortoise_orm(RoomTypeModel.all())
    


@router.post('/types', response_model=RoomType_Pydantic)
async def post_room_type(room_type: RoomTypeIn_Pydantic, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorised to use this resource')

    obj = await RoomTypeModel.create(**room_type.dict(exclude_unset=True))
    return await RoomType_Pydantic.from_tortoise_orm(obj)

@router.get('/types/{id}')
async def get_single_room_type(id:int):
    room_type = await RoomTypeModel.get(id=id)
    if room_type:
        return await RoomType_Pydantic.from_tortoise_orm(room_type)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room type {id} does not exist')

@router.put('/types/{id}')
async def update_room_type(room_type: RoomTypeIn_Pydantic, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomTypeModel.filter(id=id).update(**room_type.dict())
    return await RoomType_Pydantic.from_tortoise_orm(obj)

@router.delete('/types/{id}')
async def delete_room_type(id:int, current_user_role:str=Depends(get_current_user_role)) -> JSONResponse:
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    deleted = await RoomTypeModel.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room type {id} not found')
    return JSONResponse(status_code=status.HTTP_200_OK, content='Deleted room type {id}')

