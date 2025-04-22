from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

    
class SuccessMessageSchema(Schema):
    message = fields.Str(dump_only=True)

class HomepageSchema(Schema):
    locate = fields.Str(required=True)


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

class UpdateUserDataSchema(Schema):
    userid = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    mobile = fields.Str(required=True)

class UpdateMoistLimitSchema(Schema):
    userid = fields.Str(required=True)
    limit = fields.Str(required=True)
    
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
    millerid = fields.Str(required=True)
    millername = fields.Str(required=True)
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

class UpdateDeviceScanSchema(Schema):
    userid = fields.Str(required=True)
    deviceid = fields.Str(required=True)
    flag = fields.Boolean(required=True)
    
class GetDevicesByUserIdSchema(Schema):
    userid = fields.Str(required=True)

class EditDeviceSchema(Schema):
    userid = fields.Str(required=True)
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

    
class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    login_time = fields.DateTime(required=True)

class UserDetailSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    login_time = fields.DateTime(required=True)

class ForgotPasswordSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
class UserDeleteSchema(Schema):
    user_id = fields.Str(required=True)
    
class UserSignupSchema(Schema):
    email = fields.Str(required=True)
    
class CreateMillerSchema(Schema):
    millerid = fields.Str(required=True)
    millername = fields.Str(reqquired=True)
    userid = fields.Str(required=True)

class GetMillerSchema(Schema):
    millerid = fields.Str(required=True)
    userid = fields.Str(required=True)
