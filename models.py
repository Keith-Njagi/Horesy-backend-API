from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class UserModel(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=30, null=False,)
    email = fields.CharField(max_length=80, unique=True,null=False,)
    phone = fields.CharField(max_length=12, unique=True, null=False,)
    password_hash = fields.CharField(max_length=255, null=False)
    disabled = fields.BooleanField(null=False, default=True)
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz = True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz = True)

    user_roles: fields.ReverseRelation["UserRoleModel"]
    bookings: fields.ReverseRelation["BookingModel"]


    class Meta:
        table="users"
        ordering = ["id"]

    class PydanticMeta:
        exclude = ["password_hash", "disabled"]

    # def __str__(self):
    #     return self.full_name

    @classmethod
    async def get_user(id:int):
        return cls.get(id=id)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

class RoleModel(Model):
    id = fields.IntField(pk=True)
    role = fields.CharField(max_length=30, null=False,)
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz = True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz = True)

    user_roles: fields.ReverseRelation["UserRoleModel"]

    class Meta:
        table="roles"

    def __str__(self):
        return self.role

class UserRoleModel(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField("models.UserModel", related_name="user_roles", on_delete='CASCADE')
    role: fields.ForeignKeyRelation[RoleModel] = fields.ForeignKeyField("models.RoleModel", related_name="user_roles", on_delete='CASCADE')
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz = True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz = True)

    class Meta:
        table="user_roles"

class RoomTypeModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, null=False,)
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz=True)

    rooms: fields.ReverseRelation["RoomModel"]

    class Meta:
        table="room_types"
        ordering = ["id"]

    # def __str__(self):
    #     return self.name

class RoomModel(Model):
    id = fields.IntField(pk=True)
    room_type: fields.ForeignKeyRelation[RoomTypeModel] = fields.ForeignKeyField("models.RoomTypeModel", related_name="rooms", on_delete='CASCADE')
    image = fields.CharField(max_length=255, null=False,)
    description = fields.TextField(null=False)
    price = fields.IntField(null=False)
    is_booked = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz = True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz = True)

    bookings: fields.ReverseRelation["BookingModel"]

    class Meta:
        table="rooms"
        ordering = ["id"]

    def __str__(self):
        return self.description

class BookingModel(Model):
    id = fields.IntField(pk=True)
    room: fields.ForeignKeyRelation[RoomModel] = fields.ForeignKeyField("models.RoomModel", related_name="bookings", on_delete='CASCADE')
    user: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField("models.UserModel", related_name="bookings", on_delete='CASCADE')
    date_from = fields.DatetimeField(null=False, use_tz = True)
    date_to = fields.DatetimeField(null=True, use_tz = True)
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz = True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz = True)

    payments: fields.ReverseRelation["PaymentModel"]

    class Meta:
        table="bookings"
        ordering = ["id"]

class PaymentModel(Model):
    id = fields.IntField(pk=True)
    booking: fields.ForeignKeyRelation[BookingModel] = fields.ForeignKeyField("models.BookingModel", related_name="payments", on_delete='CASCADE')
    amount = fields.IntField(null=False)
    paid_via = fields.CharField(max_length=30,null=True)
    created_at = fields.DatetimeField(null=False, auto_now_add=True, use_tz = True)
    updated_at = fields.DatetimeField(null=True, auto_now=True, use_tz = True)

    class Meta:
        table="payments"
        ordering = ["id"]

    def __str__(self):
        return self.amount

