from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime


# class SocietySchema(Schema):
#     name = fields.Str(required=True)
#     price = fields.Int(required=True)

# class SocietyGetSchema(Schema):
#     id = fields.Str(dump_only=True)
#     name = fields.Str(dump_only=True)
#     price = fields.Int(dump_only=True)

class RestaurantDetailSchema(Schema):
    rst_id = fields.Str(required=True)
    
class SuccessMessageSchema(Schema):
    message = fields.Str(dump_only=True)

class HomepageSchema(Schema):
    locate = fields.Str(required=True)

# class SocietyQuerySchema(Schema):
#     id = fields.Str(required=True)

# class SocietyOptionalQuerySchema(Schema):
#     id = fields.Str(required=False)


class SignupSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    mobile = fields.Str(required=True)
    created_at = fields.Str(required=True)
    last_login = fields.Str(required=True)
    @validates('created_at')
    def validate_created_at(self, value):
        try:
            datetime.strptime(value, '%d/%m/%Y %H:%M')
        except ValueError:
            raise ValidationError("Invalid date format for created_at. Use 'DD/MM/YYYY HH:MM'.")

    @validates('last_login')
    def validate_last_login(self, value):
        try:
            datetime.strptime(value, '%d/%m/%Y %H:%M')
        except ValueError:
            raise ValidationError("Invalid date format for last_login. Use 'DD/MM/YYYY HH:MM'.")
            
class UpdateFlagSchema(Schema):
    userid = fields.String(required=True)
    qms = fields.Boolean(required=True)
    bms = fields.Boolean(required=True)
    aga = fields.Boolean(required=True)
    pushnotification = fields.Boolean(required=True)

class UserLogoutSchema(Schema):
    user_id = fields.Str(required=True)
    logout_time = fields.DateTime(required=True)
    track_id = fields.Str(required=True)
    track_time = fields.Str(required=True)

class SignupQuerySchema(Schema):
    token = fields.Int(required=True)

class SubscribeSchema(Schema):
    emailid = fields.Str(required=True)
    
class SubscribeQuerySchema(Schema):
    message = fields.Str(required=True)

class UserListSchema(Schema):
    result = fields.List(fields.String(), required=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class LoginQuerySchema(Schema):
    id = fields.Str(required=True)
    mobile = fields.Str(required=True)
    emailid = fields.Str(required=True)
    password = fields.Str(required=True)

class AddMoistHistorySchema(Schema):
    userid = fields.Str(required=True)
    id = fields.Str(required=True)
    moistdate = fields.Str(required=True)
    commodity = fields.Str(required=True)
    lot = fields.Str(required=True)
    stack = fields.Str(required=True)
    moisture = fields.Float(required=True)
    temperature = fields.Float(required=True)
    humidity = fields.Float(required=True)
    depo = fields.Str(required=True)
    deviceId = fields.Str(required=True)
    
    @validates('moistdate')
    def validate_moistdate(self, value):
        try:
            datetime.strptime(value, '%d/%m/%Y %H:%M')
        except ValueError:
            raise ValidationError("Invalid date format for created_at. Use 'DD/MM/YYYY HH:MM'.")

class GetMoistHistorySchema(Schema):
    userid = fields.Str(required=True)


class AddDeviceSchema(Schema):
    userid = fields.Str(required=True)
    deviceid = fields.Str(required=True)
    devicename = fields.Str(required=True)
    macaddress = fields.Str(required=True)
    charuuid = fields.Str(required=True)
    status = fields.Boolean(required=True)

class GetDevicesByUserIdSchema(Schema):
    userid = fields.Str(required=True)

class EditDeviceSchema(Schema):
    deviceid = fields.Str(required=True)
    devicename = fields.Str(required=False)
    macaddress = fields.Str(required=False)
    charuuid = fields.Str(required=False)

class ViewDeviceHistorySchema(Schema):
    deviceid = fields.Str(required=True)

    
class AddNotificationSchema(Schema):
    id = fields.Str(required=True)
    userid = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    notif_date = fields.Str(required=True)
    notif_type = fields.Str(required=True)
    status = fields.Boolean(required=True)
    @validates('notif_date')
    def validate_notif_date(self, value):
        try:
            datetime.strptime(value, '%d/%m/%Y %H:%M')
        except ValueError:
            raise ValidationError("Invalid date format for created_at. Use 'DD/MM/YYYY HH:MM'.")


class GetNotificationSchema(Schema):
    userid = fields.Str(required=True)

class NotificationIdSchema(Schema):
    notification_id = fields.Str(required=True)

class UpdateNotificationStatusSchema(Schema):
    notification_id = fields.Str(required=True)
    status = fields.Boolean(required=True)

class CreateShopSchema(Schema):
    username = fields.Str(required=True)
    mobile = fields.Str(required=True)
    email = fields.Str(required=True)
    passcode = fields.Str(required=True)
    pan = fields.Str(required=True)
    rst_name = fields.Str(required=True)
    house = fields.Str(required=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    pin = fields.Str(required=True)
    rating = fields.Str(required=True)
    keyfood = fields.Str(required=True)

class GetHomepage(Schema):
    data = fields.List(fields.String(), required=True)
    
class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    login_time = fields.DateTime(required=True)

class UserDetailSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    login_time = fields.DateTime(required=True)

class ForgotPasswordSchema(Schema):
    userid = fields.Str(required=True)
    password = fields.Str(required=True)
    
class UserDeleteSchema(Schema):
    user_id = fields.Str(required=True)
    
class UserSignupSchema(Schema):
    email = fields.Str(required=True)
    
class VisitorLoginQuerySchema(Schema):
    username = fields.Str(required=True)
    passcode = fields.Str(required=True)

class AddFavouriteSchema(Schema):
    parentid = fields.Str(required=True)
    user_id = fields.Str(required=True)

class GetFavouriteSchema(Schema):
    user_id = fields.Str(required=True)


class PlanStatusQuerySchema(Schema):
    user_id = fields.Str(required=True)

class RemoveFavouriteSchema(Schema):
    user_id = fields.Str(required=True)
    parentid = fields.Str(required=True)
    
class AddAudioSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    rating = fields.Str(required=True)
    author = fields.Str(required=True)
    link = fields.Str(required=True)
    length = fields.Str(required=True)
    totalpart = fields.Str(required=True)
    image_url = fields.Str(required=True)
    keywords = fields.Str(required=True)
    drive_link = fields.Str(required=True)
    language = fields.Str(required=True)

class GetCartSchema(Schema):
    cst_id = fields.Str(required=True)
    
class PlaceOrderSchema(Schema):
    user_id = fields.Str(required=True)
    payment_date = fields.DateTime(required=True)
    pay_id = fields.Str(required=True)
    
    
class GuestQuerySchema(Schema):
    query = fields.Str(required=True)
    
