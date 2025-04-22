from db import UserDatabase
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import ValidationError
#from schemas import AddDeviceSchema, UpdateUserDataSchema, UpdateDeviceScanSchema, UpdateMoistLimitSchema, ForgotPasswordSchema, AddMoistHistorySchema, AddNotificationSchema, EditDeviceSchema, GetDevicesByUserIdSchema, GetMoistHistorySchema, GetNotificationSchema, NotificationIdSchema, SignupSchema, SignupQuerySchema, LoginQuerySchema, LoginSchema, SubscribeQuerySchema, SubscribeSchema, SuccessMessageSchema, UpdateNotificationStatusSchema, UserDeleteSchema, UserDetailSchema, UserListSchema, UserLoginSchema, UpdateFlagSchema, UserLogoutSchema, UserSignupSchema, ViewDeviceHistorySchema
from schemas import (
    AddDeviceSchema,
    UpdateUserDataSchema,
    UpdateDeviceScanSchema,
    UpdateMoistLimitSchema,
    ForgotPasswordSchema,
    AddMoistHistorySchema,
    AddNotificationSchema,
    EditDeviceSchema,
    GetDevicesByUserIdSchema,
    GetMoistHistorySchema,
    GetNotificationSchema,
    NotificationIdSchema,
    SignupSchema,
    SignupQuerySchema,
    LoginQuerySchema,
    LoginSchema,
    CreateMillerSchema,
    SubscribeQuerySchema,
    SubscribeSchema,
    SuccessMessageSchema,
    UpdateNotificationStatusSchema,
    UserDeleteSchema,
    UserDetailSchema,
    UserListSchema,
    UserLoginSchema,
    UpdateFlagSchema,
    UserLogoutSchema,
    UserSignupSchema,
    ViewDeviceHistorySchema
)

import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
#from blocklist import BLOCKLIST
from flask import request, render_template
import json
from flask import Flask, render_template, request, jsonify
# import torch
#from transformers import AutoModelForCausalLM, AutoTokenizer
import smtplib, ssl
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import razorpay
from datetime import datetime

blp = Blueprint("Users", __name__, description="Operations on users")
#tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
#model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
result_list = []


    
@blp.route("/add_user")
class UserSignup(MethodView):

    def __init__(self):
        self.db = UserDatabase()
    
    @blp.arguments(SignupSchema, location="json")
    def post(self, request_data):
        #request_data = request.get_json()
        #print(request_data)
        username = request_data['username']
        password = request_data['password']
        mobile = request_data['mobile']
        created_at = datetime.strptime(request_data['created_at'], '%d/%m/%Y %H:%M')
        last_login = datetime.strptime(request_data['last_login'], '%d/%m/%Y %H:%M')
        result = self.db.add_user(username,password,mobile,created_at,last_login)
        if result is None:
            abort(400, message="Username or password is incorrect")
        return result, 201


@blp.route("/user_login")
class UserLogin(MethodView):

    def __init__(self):
        self.db = UserDatabase()
    
    @blp.arguments(LoginSchema, location="json")
    def post(self, request_data):
        username = request_data['username']
        password = request_data['password']
        result = self.db.signin_user(username, password)
        if result is None:
            abort(404, message="Page Not Found")
        return result, 200
        
@blp.route("/update_flag")
class UserFlagUpdate(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UpdateFlagSchema, location="json")
    def post(self, request_data):
        print("Incoming update payload:", request_data)

        userid = request_data.pop("userid", None)
        if not userid:
            abort(400, message="User ID is required")

        result = self.db.update_user_profile(userid, request_data)

        if result:
            return result, 200
        else:
            abort(400, message="Failed to update user profile")


@blp.route("/update_user_data")
class UserFlagUpdate(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UpdateUserDataSchema, location="json")
    def post(self, request_data):
        print("Incoming update payload:", request_data)

        userid = request_data.pop("userid", None)
        if not userid:
            abort(400, message="User ID is required")

        result = self.db.update_user_data(userid, request_data)

        if result:
            return result, 200
        else:
            abort(400, message="Failed to update user profile")
    
@blp.route("/update_moist_limit")
class UserFlagUpdate(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UpdateMoistLimitSchema, location="json")
    def post(self, request_data):
        print("Incoming update payload:", request_data)

        userid = request_data.pop("userid", None)
        if not userid:
            abort(400, message="User ID is required")

        result = self.db.update_moist_limit(userid, request_data)

        if result:
            return result, 200
        else:
            abort(400, message="Failed to update user profile")

@blp.route("/update_device_scan")
class DeviceScanUpdate(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UpdateDeviceScanSchema, location="json")
    def post(self, request_data):
        try:
            print("Incoming update payload:", request_data)
            userid = request_data.get("userid")
            if not userid:
                abort(400, message="User ID is required")

            result = self.db.update_device_scan(userid, request_data)

            if result:
                return result, 200
            else:
                abort(400, message="Failed to update user profile")

        except ValidationError as e:
            print("Validation error:", e.messages)  # This prints any schema validation errors
            abort(400, message="Validation error: " + str(e.messages))
        except Exception as e:
            print("Error processing the request:", e)
            abort(500, message="Internal Server Error")
            
@blp.route("/update_password")
class PasswordUpdate(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(ForgotPasswordSchema, location="json")
    def post(self, request_data):
        print("Incoming update payload:", request_data)

        username = request_data.get("username")
        password = request_data.get("password")
        if not username:
            abort(400, message="User ID is required")

        result = self.db.update_user_password(username, password)

        if result:
            return {"message": "Password updated successfully"}, 200
        else:
            abort(400, message="Failed to update user profile")
    
@blp.route("/add_moisture")
class MoistureData(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(AddMoistHistorySchema, location="json")
    def post(self, request_data):
        id = request_data['id']
        userid = request_data['userid']
        date = request_data['moistdate']
        commodity = request_data['commodity']
        lot = request_data['lot']
        stack = request_data['stack']
        moisture = request_data['moisture']
        temperature = request_data['temperature']
        humidity = request_data['humidity']
        depo = request_data['depo']
        deviceId = request_data['deviceId']

        result = self.db.add_moist_history(id, userid, date, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId)

        if not result:
            abort(400, message="Failed to add moist history")

        return {"message": "Moisture history added successfully"}, 201

@blp.route("/add_moist")
class MoistData(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(GetMoistHistorySchema, location="query")
    def post(self, request_data):
        userid = request_data['userid']
        records = self.db.get_moist_history_by_userid(userid)

        if not records:
            abort(404, message="No moisture history found for this user")

        return records, 200

@blp.route("/device")
class DeviceAPI(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    # Add new device
    @blp.arguments(AddDeviceSchema, location="json")
    def post(self, request_data):
        userid = request_data['userid']
        deviceid = request_data['deviceid']
        devicename = request_data['devicename']
        macaddress = request_data['macaddress']
        charuuid = request_data['charuuid']
        status = request_data['status']

        result = self.db.add_device(userid, deviceid, devicename, macaddress, charuuid, status)

        if not result:
            abort(400, message="Failed to add device")

        return {"message": "Device added successfully"}, 201

    # Get all devices by user id
    @blp.arguments(GetDevicesByUserIdSchema, location="query")
    def get(self, request_data):
        userid = request_data['userid']
        devices = self.db.get_devices_by_userid(userid)

        if not devices:
            abort(404, message="No devices found for this user")

        return {"devices": devices}, 200

    # Edit device details
    @blp.arguments(EditDeviceSchema, location="json")
    def put(self, request_data):
        userid = request_data['userid']
        deviceid = request_data['deviceid']
        devicename = request_data['devicename']
        macaddress = request_data['macaddress']
        charuuid = request_data['charuuid']

        result = self.db.edit_device(userid, deviceid, devicename, macaddress, charuuid)

        if not result:
            abort(400, message="Failed to update device")

        return {"message": "Device updated successfully"}, 200

    # View moisture history by device id
    @blp.arguments(ViewDeviceHistorySchema, location="query")
    def patch(self, request_data):
        deviceid = request_data['deviceid']
        history = self.db.get_device_history(deviceid)

        if not history:
            abort(404, message="No moisture history found for this device")

        return {"device_history": history}, 200


@blp.route("/notification")
class NotificationView(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(AddNotificationSchema, location="json")
    def post(self, request_data):
        result = self.db.add_notification(**request_data)
        if not result:
            abort(400, message="Failed to add notification")
        return {"message": "Notification added successfully"}, 201

    @blp.arguments(GetNotificationSchema, location="query")
    def get(self, request_data):
        userid = request_data['userid']
        notifications = self.db.get_notifications_by_userid(userid)
        if not notifications:
            abort(404, message="No notifications found")
        return notifications, 200

    @blp.arguments(NotificationIdSchema, location="query")
    def delete(self, request_data):
        notification_id = request_data['notification_id']
        result = self.db.delete_notification_by_id(notification_id)
        if not result:
            abort(404, message="Notification not found")
        return {"message": "Notification deleted"}, 200

    @blp.arguments(UpdateNotificationStatusSchema, location="json")
    def patch(self, request_data):
        notification_id = request_data['notification_id']
        status = request_data['status']
        result = self.db.mark_notification_as_read(notification_id, status)
        if not result:
            abort(400, message="Failed to update notification status")
        return {"message": "Notification status updated"}, 200

@blp.route("/create_miller")
class CreateMillerView(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(CreateMillerSchema, location="json")
    def post(self, request_data):
        result = self.db.add_miller(request_data)
        if not result:
            abort(400, message="Failed to add miller")
        return {"message": "Miller added successfully"}, 201


