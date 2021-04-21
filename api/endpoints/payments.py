from fastapi import APIRouter, Depends

from models import PaymentModel
from schemas.schemas import Payment_Pydantic, PaymentIn_Pydantic, User_Pydantic, Role_Pydantic
from utilities.auth import get_current_user, get_current_user_role

router = APIRouter(prefix='/api/payments', tags=["payments"])
# CRUD FOR BOOKINGS

@router.get('/')
async def get_payments(current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    return await Payment_Pydantic.from_queryset(PaymentModel.all())


@router.post('/')
async def post_payment(payment: PaymentIn_Pydantic, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await PaymentModel.create(**payment.dict)
    return await Payment_Pydantic.from_tortoise_orm(obj)


@router.get('/{id}')
async def get_single_payment(id:int, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    payment = await PaymentModel.get(id=id)
    if payment:
        return await Payment_Pydantic.from_tortoise_orm(payment)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Booking {id} does not exist')


@router.put('/{id}')
async def update_payment(payment: PaymentIn_Pydantic, current_user_role:str=Depends(get_current_user_role)):
    if current_user_role != 'Admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'You are not authorised to use this resource')
    obj = await PaymentModel.filter(id=id).update(**payment.dict())
    return await Payment_Pydantic.from_tortoise_orm(obj)
