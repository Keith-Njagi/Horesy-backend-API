from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from models import RoomTypeModel, RoomModel
from schemas.schemas import RoomType_Pydantic, RoomTypeIn_Pydantic, Room_Pydantic, RoomIn_Pydantic, Role_Pydantic
from utilities.auth import get_current_user_role

router = APIRouter(prefix='/api/rooms', tags=["rooms"])
# CRUD FOR ROOMS AND ROOM TYPES

@router.get('/')
async def get_rooms():
    return await Room_Pydantic.from_queryset(RoomModel.all())

@router.post('/')
async def post_room(room: RoomTypeIn_Pydantic, current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    if current_user_role.role != 'Admin':
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
async def update_room(id: int,room: RoomTypeIn_Pydantic, current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    if current_user_role.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomModel.filter(id=id).update(**room.dict())
    return await Room_Pydantic.from_tortoise_orm(obj)

@router.delete('/{id}')
async def delete_room(id:int, current_user_role:Role_Pydantic=Depends(get_current_user_role)) -> JSONResponse:
    if current_user_role.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    deleted = await RoomTypeModel.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room type {id} not found')
    return JSONResponse(status_code=status.HTTP_200_OK, content='Deleted room type {id}')



@router.get('/types')
async def get_room_types():
    return await RoomType_Pydantic.from_queryset(RoomTypeModel.all())

@router.post('/types')
async def post_room_type(room_type: RoomTypeIn_Pydantic, current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    if current_user_role.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomTypeModel.create(**room.dict(exclude_unset=True))
    return await RoomType_Pydantic.from_tortoise_orm(obj)

@router.get('/types/{id}')
async def get_single_room_type(id:int):
    room_type = await RoomTypeModel.get(id=id)
    if room_type:
        return await RoomType_Pydantic.from_tortoise_orm(room_type)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room type {id} does not exist')

@router.put('/types/{id}')
async def update_room_type(room_type: RoomTypeIn_Pydantic, current_user_role:Role_Pydantic=Depends(get_current_user_role)):
    if current_user_role.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await RoomTypeModel.filter(id=id).update(**room_type.dict())
    return await RoomType_Pydantic.from_tortoise_orm(obj)

@router.delete('/types/{id}')
async def delete_room_type(id:int, current_user_role:Role_Pydantic=Depends(get_current_user_role)) -> JSONResponse:
    if current_user_role.role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    deleted = await RoomTypeModel.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Room type {id} not found')
    return JSONResponse(status_code=status.HTTP_200_OK, content='Deleted room type {id}')

