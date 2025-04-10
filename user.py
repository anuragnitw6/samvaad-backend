from db import UserDatabase
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AddAudioSchema, AddDeviceSchema, AddFavouriteSchema, AddMoistHistorySchema, AddNotificationSchema, CreateShopSchema, EditDeviceSchema, GetCartSchema, GetDevicesByUserIdSchema, GetFavouriteSchema, GetHomepage, GetMoistHistorySchema, GetNotificationSchema, GuestQuerySchema, HomepageSchema, NotificationIdSchema, PlaceOrderSchema, PlanStatusQuerySchema, RemoveFavouriteSchema, RestaurantDetailSchema, SignupSchema, SignupQuerySchema, LoginQuerySchema, LoginSchema, SubscribeQuerySchema, SubscribeSchema, SuccessMessageSchema, UpdateNotificationStatusSchema, UpdateProfileSchema, UserDeleteSchema, UserDetailSchema, UserListSchema, UserLoginSchema, UserLogoutSchema, UserSignupSchema, ViewDeviceHistorySchema, VisitorLoginQuerySchema
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


# @blp.route("/guest")
# class UserLogin(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()
    
#     # @blp.response(200, OwnerLoginSucessSchema)
#     @blp.arguments(GuestQuerySchema, location="query")
#     def get(self, request_data):
#         query = request_data['query']
#         result = self.db.guest_search(query)
        
#         if result is None:
#             abort(404, message="User doesn't exist")
#         return result, 200
    

# @blp.route("/homepage")
# class UserLogin(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()
    
#     # @blp.response(200, GetHomepage)
#     @blp.arguments(HomepageSchema, location="query")
#     def get(self, request_data):
#         query = request_data['locate']
#         result = self.db.home_page(query)
#         if result is None:
#             abort(404, message="Page Not Found")
#         return result, 200
    
@blp.route("/add_user")
class UserLogin(MethodView):

    def __init__(self):
        self.db = UserDatabase()
    
    @blp.response(200)
    @blp.arguments(LoginSchema, location="json")
    def get(self, request_data):
        username = request_data['username']
        password = request_data['password']
        result = self.db.signin_user(username, password)
        if result is None:
            abort(404, message="Page Not Found")
        return result, 200
    
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
        
@blp.route("/update_user")
class UserProfileUpdate(MethodView):
    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(UpdateProfileSchema, location="json")
    def put(self, request_data):
        print("Incoming update payload:", request_data)

        userid = request_data.pop("userid", None)

        if not userid:
            abort(400, message="User ID is required")

        if not request_data:
            abort(400, message="No fields provided to update")

        result = self.db.update_user_profile(userid, request_data)

        if result:
            return {"message": "User profile updated successfully"}, 200
        else:
            abort(400, message="Failed to update user profile")

    
@blp.route("/add_moist")
class MoistData(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    @blp.arguments(AddMoistHistorySchema, location="query")
    def get(self, request_data):
        userid = request_data['userid']
        date = request_data['date']
        time = request_data['time']
        commodity = request_data['commodity']
        lot = request_data['lot']
        stack = request_data['stack']
        moisture = request_data['moisture']
        temperature = request_data['temperature']
        humidity = request_data['humidity']
        depo = request_data['depo']
        deviceId = request_data['deviceId']

        result = self.db.add_moist_history(userid, date, time, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId)

        if not result:
            abort(400, message="Failed to add moist history")

        return {"message": "Moisture history added successfully"}, 201

    @blp.arguments(GetMoistHistorySchema, location="query")
    def post(self, request_data):
        userid = request_data['userid']
        records = self.db.get_moist_history_by_userid(userid)

        if not records:
            abort(404, message="No moisture history found for this user")

        return {"moisture_history": records}, 200

@blp.route("/device")
class DeviceAPI(MethodView):

    def __init__(self):
        self.db = UserDatabase()

    # Add new device
    @blp.arguments(AddDeviceSchema, location="query")
    def post(self, request_data):
        userid = request_data['userid']
        deviceid = request_data['deviceid']
        devicename = request_data['devicename']
        macaddress = request_data['macaddress']
        charuuid = request_data['charuuid']
        status = request_data['status']

        result = self.db.add_user_device(userid, deviceid, devicename, macaddress, charuuid, status)

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
    @blp.arguments(EditDeviceSchema, location="query")
    def put(self, request_data):
        deviceid = request_data['deviceid']
        devicename = request_data.get('devicename')
        macaddress = request_data.get('macaddress')
        charuuid = request_data.get('charuuid')
        status = request_data.get('status')

        result = self.db.update_device(deviceid, devicename, macaddress, charuuid, status)

        if not result:
            abort(400, message="Failed to update device")

        return {"message": "Device updated successfully"}, 200

    # View moisture history by device id
    @blp.arguments(ViewDeviceHistorySchema, location="query")
    def patch(self, request_data):
        deviceid = request_data['deviceid']
        history = self.db.get_moist_history_by_deviceid(deviceid)

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
        notifications = self.db.get_all_notifications(userid)
        if not notifications:
            abort(404, message="No notifications found")
        return {"notifications": notifications}, 200

    @blp.arguments(NotificationIdSchema, location="query")
    def delete(self, request_data):
        notification_id = request_data['notification_id']
        result = self.db.delete_notification(notification_id)
        if not result:
            abort(404, message="Notification not found")
        return {"message": "Notification deleted"}, 200

    @blp.arguments(UpdateNotificationStatusSchema, location="json")
    def patch(self, request_data):
        notification_id = request_data['notification_id']
        status = request_data['status']
        result = self.db.update_notification_status(notification_id, status)
        if not result:
            abort(400, message="Failed to update notification status")
        return {"message": "Notification status updated"}, 200

    # @blp.response(200, GetHomepage)
    # @blp.arguments(RemoveFavouriteSchema, location="query")
    # def delete(self, request_data):
    #     user_id = request_data['user_id']
    #     parent_id = request_data['parent_id']
    #     result = self.db.remove_favourite(user_id,parent_id)
    #     if result is None:
    #         abort(404, message="Page Not Found")
    #     return 200
    
# @blp.route("/plan")
# class UserLogin(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()
    
#     # @blp.response(200, OwnerLoginSucessSchema)
#     @blp.arguments(PlanStatusQuerySchema, location="query")
#     def get(self, request_data):
#         user_id = request_data['user_id']
#         result = self.db.plan_status(user_id)
#         if result is None:
#             abort(404, message="User doesn't exist")
#         return result, 200
    
#     @blp.arguments(UserSignupSchema)
#     def post(self, request_data):
#         #request_data = request.get_json()
#         #print(request_data)
#         email = request_data['email']
#         # verifyOtp(email)
#         result = self.db.verify_email(email)
#         if result is None:
#             abort(400, message="Please Try Again...")
#         return result,201

# @blp.route("/user-detail")
# class UserLogin(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()
    
#     # @blp.response(200, OwnerLoginSucessSchema)
#     @blp.arguments(UserLoginSchema, location="query")
#     def get(self, request_data):
#         email = request_data['email']
#         login_time =request_data['login_time']
#         result = self.db.visitor_login(email,login_time) 
#         if result is None:
#             abort(404, message="User doesn't exist")
#         return result, 200
    
#     @blp.arguments(UserDetailSchema)
#     def post(self, request_data):
#         #request_data = request.get_json()
#         #print(request_data)
#         name = request_data['name']
#         email = request_data['email']
#         login_time = request_data['login_time']
#         otp = self.db.verify_email(email)
#         user_id = uuid.uuid4().hex
#         result = self.db.save_user(name,user_id,email,login_time)
#         if result is False:
#             abort(400, message="user already exist")
#         return {"user_id":user_id,"name":name,"email":email,"otp":otp}, 201

#     @blp.arguments(UserDeleteSchema)
#     def delete(self, request_data):
#         #request_data = request.get_json()
#         #print(request_data)
#         user_id = request_data['user_id']
#         result = self.db.delete_user(user_id)
#         if result is None:
#             abort(400, message="Please Try Again...")
#         return {"message":"User removed successfully"}, 201

# @blp.route("/logout")
# class UserLogout(MethodView):
   
   
#     def __init__(self):
#         self.db = UserDatabase()
    
#     # @jwt_required()
#     @blp.arguments(UserLogoutSchema)
#     def post(self,request_data):
#         user_id = request_data['user_id']
#         logout_time = request_data['logout_time']
#         track_id = request_data['track_id']
#         track_time = request_data['track_time']
#         result = self.db.user_logout(user_id,logout_time,track_id,track_time)
#         return {'message': "Successfully logged out."}

# @blp.route("/items")
# class User(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()

#     @blp.arguments(RestaurantDetailSchema,location="query")
#     # @blp.response(200, SuccessMessageSchema)
#     def get(self, request_data):
#         # check if already exists
#         rst_id = request_data["rst_id"]
#         result = self.db.get_restaurant_details(rst_id)
#         if result is not None:
#             return result, 200
#         return {"message": "Page Not Found"}, 404

#     @blp.arguments(AddItemSchema)
#     # @blp.response(200, SuccessMessageSchema)
#     def post(self, request_data):
#         # check if already exists
#         name = request_data["name"]
#         quantity = request_data["quantity"]
#         price = request_data["price"]
#         rest_id = request_data["rest_id"]
#         category = request_data["category"]
#         item_id = uuid.uuid4().hex
#         if self.db.add_new_item(item_id,name, quantity, price, rest_id,category):
#             return {"message": "Item added succesfully"}, 201
#         return {"message": "Please Try Again"}, 501

#     # @blp.response(200, SuccessMessageSchema)
#     @blp.arguments(SignupQuerySchema, location="query")
#     def delete(self, args):
#         id = args.get('id')
#         if self.db.delete_user(id):
#             return {'message': 'User deleted'}   
#         abort(404, message="Given user id doesn't exist.")

# @blp.route("/create-shop")
# class User(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()

#     # @blp.response(200, OwnerLoginSucessSchema)
#     @blp.arguments(OwnerLoginQuerySchema, location="query")
#     def get(self, request_data):
#         username = request_data['username']
#         password = request_data['passcode']
#         result = self.db.shop_owner_login(username, password)
#         # user = {
#         #     "id":result[0],
#         #     "mobile":result[1],
#         #     "password":result[2],
#         #     "emailid":result[3]
#         # }
#         # user['id'], user['mobile'], user['password'], user['email'] = result 
#         if result is None:
#             abort(404, message="User doesn't exist")
#         return {"message": "Login succesfully","data":result}, 200
        
#     @blp.arguments(CreateShopSchema)
#     # @blp.response(200, SuccessMessageSchema)
#     def post(self, request_data):
#         # check if already exists
        
#         uid = uuid.uuid4().hex
#         rid = uuid.uuid4().hex
#         username = request_data["username"]
#         email = request_data["email"]
#         mobile = request_data["mobile"]
#         passcode = request_data["passcode"]
#         pan = request_data["pan"]
#         rst_name = request_data["rst_name"]
#         # password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
#         house = request_data["house"]
#         street = request_data["street"]
#         city = request_data["city"]
#         state = request_data["state"]
#         pin = request_data["pin"]
#         keyfood = request_data["keyfood"]
#         rating = request_data["rating"]
#         #print(password)
#         # password = request_data["password"]
#         # if self.db.verify_signup(mobile, password, emailid):
#         #     return abort(403, message="User already exists")
#         if self.db.create_shop(uid, username, email, mobile,passcode,pan,rid,rst_name,house,street,city,state,pin,keyfood,rating):
#             return {"message": "User added succesfully"}, 201

    # @blp.response(200, SuccessMessageSchema)
    # @blp.arguments(SignupQuerySchema, location="query")
    # def delete(self, args):
    #     id = args.get('id')
    #     if self.db.delete_user(id):
    #         return {'message': 'User deleted'}   
    #     abort(404, message="Given user id doesn't exist.")

# @blp.route("/add-cart")
# class User(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()

#     # @blp.response(200, OwnerLoginSucessSchema)
#     @blp.arguments(GetCartSchema, location="query")
#     def get(self, request_data):
#         cst_id = request_data['cst_id']
#         result = self.db.get_cart(cst_id)
#         if result is None:
#             abort(404, message="User doesn't exist")
#         return {"message": "Cart Items fetch succesfully"}, 200
        
#     @blp.arguments(AddAudioSchema)
#     # @blp.response(200, SuccessMessageSchema)
#     def post(self, request_data):
#         # check if already exists
        
#         title = request_data["title"]
#         description = request_data["description"]
#         rating = request_data["rating"]
#         author = request_data["author"]
#         link = request_data["link"]
#         length = request_data["length"]
#         totalpart = request_data["totalpart"]
#         image_url = request_data["image_url"]
#         keywords = request_data["keywords"]
#         drive_link = request_data["drive_link"]
#         language = request_data["language"]
#         audio_id = uuid.uuid4().hex
#         if self.db.add_audio(audio_id,title,description,rating,author,link,length,totalpart,image_url,keywords,drive_link,language):
#             return {"message": "Audio file added succesfully"}, 201
#         return {"message": "Please Try Again"}, 501
#     # @blp.response(200, SuccessMessageSchema)
#     @blp.arguments(SignupQuerySchema, location="query")
#     def delete(self, args):
#         id = args.get('id')
#         if self.db.delete_user(id):
#             return {'message': 'User deleted'}   
#         abort(404, message="Given user id doesn't exist.")


# @blp.route("/place-order")
# class User(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()
    
#     @blp.arguments(PlaceOrderSchema)
#     @blp.response(200, SuccessMessageSchema)
#     def post(self,request_data):
#         # check if already exists
#         user_id = request_data['user_id']
#         pay_id = request_data["pay_id"]
#         receipt_id = "rcpt_" + user_id
#         amount = "99"
#         amount_paid = "99"
#         amount_due = "0"
#         payment_date = request_data['payment_date']
#         if self.db.place_order(user_id,pay_id,amount,amount_paid,amount_due,receipt_id,payment_date):
#             return {"message": "Order Placed succesfully"}, 200
#         return {"message": "Please Try Again"}, 501
    
# @blp.route("/home")
# def home():
#     return render_template('home.html')

# @blp.route("/login")
# def login():
#     return render_template('login.html')


# @blp.route("/register")
# def register():
#     return render_template('register.html')

# @blp.route("/payment")
# def login():
#     return render_template('checkout.html')

# @blp.route("/subscribe")
# class User(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()

#     @blp.response(200, UserListSchema)
#     # @blp.arguments(SubscribeSchema, location="query")
#     def get(self):
#         result = self.db.get_subscriber_list()
#         if result is False:
#             abort(400, message="Please Try Again")
#         else:
#             return render_template('sample.html')
        
#     @blp.arguments(SubscribeSchema)
#     @blp.response(200, SubscribeQuerySchema)
#     def post(self, request_data):
#         # check if already exists
#         # emailid = request_data["email"]
#         # password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
#         emailid = request_data["emailid"]
#         #print(password)
#         # password = request_data["password"]
#         if self.db.verify_email(emailid):
#             return abort(403, message="User already subscribed")
#         if self.db.subscribe_user(emailid):
#             sender_email = "anuragnitw6@gmail.com"
#             receiver_email = emailid
#             password = 'jgptbdwflllooerb'

#             message = MIMEMultipart("alternative")
#             message["Subject"] = "Thank you for subscribing to Qmedia"
#             message["From"] = sender_email
#             message["To"] = receiver_email
            
#             message['X-MSMail-Priority'] = 'Normal'
#             # Create the plain-text and HTML version of your message
#             text = """\
#             Hi,
#             How are you?
#             Real Python has many great tutorials:
#             www.realpython.com"""
#             html = """\
# <!doctype html>
# <html lang="en">
#   <head>
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
#     <title>Simple Transactional Email</title>
#     <style media="all" type="text/css">
#     /* -------------------------------------
#     GLOBAL RESETS
# ------------------------------------- */
    
#     body {
#       font-family: Helvetica, sans-serif;
#       -webkit-font-smoothing: antialiased;
#       font-size: 16px;
#       line-height: 1.3;
#       -ms-text-size-adjust: 100%;
#       -webkit-text-size-adjust: 100%;
#     }
    
#     table {
#       border-collapse: separate;
#       mso-table-lspace: 0pt;
#       mso-table-rspace: 0pt;
#       width: 100%;
#     }
    
#     table td {
#       font-family: Helvetica, sans-serif;
#       font-size: 16px;
#       vertical-align: top;
#     }
#     /* -------------------------------------
#     BODY & CONTAINER
# ------------------------------------- */
    
#     body {
#       background-color: #f4f5f6;
#       margin: 0;
#       padding: 0;
#     }
    
#     .body {
#       background-color: #f4f5f6;
#       width: 100%;
#     }
    
#     .container {
#       margin: 0 auto !important;
#       max-width: 600px;
#       padding: 0;
#       padding-top: 24px;
#       width: 600px;
#     }
    
#     .content {
#       box-sizing: border-box;
#       display: block;
#       margin: 0 auto;
#       max-width: 600px;
#       padding: 0;
#     }
#     /* -------------------------------------
#     HEADER, FOOTER, MAIN
# ------------------------------------- */
    
#     .main {
#       background: #ffffff;
#       border: 1px solid #eaebed;
#       border-radius: 16px;
#       width: 100%;
#     }
    
#     .wrapper {
#       box-sizing: border-box;
#       padding: 24px;
#     }
    
#     .footer {
#       clear: both;
#       padding-top: 24px;
#       text-align: center;
#       width: 100%;
#     }
    
#     .footer td,
#     .footer p,
#     .footer span,
#     .footer a {
#       color: #9a9ea6;
#       font-size: 16px;
#       text-align: center;
#     }
#     /* -------------------------------------
#     TYPOGRAPHY
# ------------------------------------- */
    
#     p {
#       font-family: Helvetica, sans-serif;
#       font-size: 16px;
#       font-weight: normal;
#       margin: 0;
#       margin-bottom: 16px;
#     }
    
#     a {
#       color: #0867ec;
#       text-decoration: underline;
#     }
#     /* -------------------------------------
#     BUTTONS
# ------------------------------------- */
    
#     .btn {
#       box-sizing: border-box;
#       min-width: 100% !important;
#       width: 100%;
#     }
    
#     .btn > tbody > tr > td {
#       padding-bottom: 16px;
#     }
    
#     .btn table {
#       width: auto;
#     }
    
#     .btn table td {
#       background-color: #ffffff;
#       border-radius: 4px;
#       text-align: center;
#     }
    
#     .btn a {
#       background-color: #ffffff;
#       border: solid 2px #0867ec;
#       border-radius: 4px;
#       box-sizing: border-box;
#       color: #0867ec;
#       cursor: pointer;
#       display: inline-block;
#       font-size: 16px;
#       font-weight: bold;
#       margin: 0;
#       padding: 12px 24px;
#       text-decoration: none;
#       text-transform: capitalize;
#     }
    
#     .btn-primary table td {
#       background-color: #0867ec;
#     }
    
#     .btn-primary a {
#       background-color: #0867ec;
#       border-color: #0867ec;
#       color: #ffffff;
#     }
    
#     @media all {
#       .btn-primary table td:hover {
#         background-color: #ec0867 !important;
#       }
#       .btn-primary a:hover {
#         background-color: #ec0867 !important;
#         border-color: #ec0867 !important;
#       }
#     }
    
#     /* -------------------------------------
#     OTHER STYLES THAT MIGHT BE USEFUL
# ------------------------------------- */
    
#     .last {
#       margin-bottom: 0;
#     }
    
#     .first {
#       margin-top: 0;
#     }
    
#     .align-center {
#       text-align: center;
#     }
    
#     .align-right {
#       text-align: right;
#     }
    
#     .align-left {
#       text-align: left;
#     }
    
#     .text-link {
#       color: #0867ec !important;
#       text-decoration: underline !important;
#     }
    
#     .clear {
#       clear: both;
#     }
    
#     .mt0 {
#       margin-top: 0;
#     }
    
#     .mb0 {
#       margin-bottom: 0;
#     }
    
#     .preheader {
#       color: transparent;
#       display: none;
#       height: 0;
#       max-height: 0;
#       max-width: 0;
#       opacity: 0;
#       overflow: hidden;
#       mso-hide: all;
#       visibility: hidden;
#       width: 0;
#     }
    
#     .powered-by a {
#       text-decoration: none;
#     }
    
#     /* -------------------------------------
#     RESPONSIVE AND MOBILE FRIENDLY STYLES
# ------------------------------------- */
    
#     @media only screen and (max-width: 640px) {
#       .main p,
#       .main td,
#       .main span {
#         font-size: 16px !important;
#       }
#       .wrapper {
#         padding: 8px !important;
#       }
#       .content {
#         padding: 0 !important;
#       }
#       .container {
#         padding: 0 !important;
#         padding-top: 8px !important;
#         width: 100% !important;
#       }
#       .main {
#         border-left-width: 0 !important;
#         border-radius: 0 !important;
#         border-right-width: 0 !important;
#       }
#       .btn table {
#         max-width: 100% !important;
#         width: 100% !important;
#       }
#       .btn a {
#         font-size: 16px !important;
#         max-width: 100% !important;
#         width: 100% !important;
#       }
#     }
#     /* -------------------------------------
#     PRESERVE THESE STYLES IN THE HEAD
# ------------------------------------- */
    
#     @media all {
#       .ExternalClass {
#         width: 100%;
#       }
#       .ExternalClass,
#       .ExternalClass p,
#       .ExternalClass span,
#       .ExternalClass font,
#       .ExternalClass td,
#       .ExternalClass div {
#         line-height: 100%;
#       }
#       .apple-link a {
#         color: inherit !important;
#         font-family: inherit !important;
#         font-size: inherit !important;
#         font-weight: inherit !important;
#         line-height: inherit !important;
#         text-decoration: none !important;
#       }
#       #MessageViewBody a {
#         color: inherit;
#         text-decoration: none;
#         font-size: inherit;
#         font-family: inherit;
#         font-weight: inherit;
#         line-height: inherit;
#       }
#     }
#     </style>
#   </head>
#   <body>
#     <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="body">
#         <tr>
#             <td>&nbsp;</td>
#                 <td class="container">
#                     <div class="content">

#                         <!-- START CENTERED WHITE CONTAINER -->
#                         <span class="preheader">Welcome to Qmedia for daily newsletter updated.</span>
#                         <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="main">

#                             <!-- START MAIN CONTENT AREA -->
#                             <tr>
#                                 <td class="wrapper">
#                                     <p>Hi there!</p>
#                                     <p>Welcome to our 7 point daily bulletin to keep you updated in 5 minutes read. </p>
#                                     <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="btn btn-primary">
#                                         <tbody>
#                                             <tr>
#                                                 <td align="left">
#                                                     <table role="presentation" border="0" cellpadding="0" cellspacing="0">
#                                                         <tbody>
#                                                             <tr>
#                                                                 <td> <a href="http://htmlemail.io" target="_blank">Call To Action</a> </td>
#                                                             </tr>
#                                                         </tbody>
#                                                     </table>
#                                                 </td>
#                                             </tr>
#                                         </tbody>
#                                     </table>
#                                     <p>Sometimes we just want to go through what's going on outside of our work culture so We will deliver you top news for you.</p>
#                                     <p>Good luck! Hope it works.</p>
#                                 </td>
#                             </tr>

#                         <!-- END MAIN CONTENT AREA -->
#                         </table>

#                         <!-- START FOOTER -->
#                         <div class="footer">
#                         <table role="presentation" border="0" cellpadding="0" cellspacing="0">
#                             <tr>
#                                 <td class="content-block">
#                                     <span class="apple-link">Qmedia.ai, Bangalore,India</span>
#                                     <br> Don't like these emails? <a href="http://htmlemail.io/blog">Unsubscribe</a>.
#                                 </td>
#                             </tr>
#                             <tr>
#                                 <td class="content-block powered-by">
#                                     Powered by <a href="http://htmlemail.io">Qmedia.io</a>
#                                 </td>
#                             </tr>
#                         </table>
#                         </div>

#                         <!-- END FOOTER -->
            
#                         <!-- END CENTERED WHITE CONTAINER --></div>
#                         </td>
#                             <td>&nbsp;</td>
#                         </tr>
#                     </table>
#                 </body>
#             </html>
#             """

#             # Turn these into plain/html MIMEText objects
#             part1 = MIMEText(text, "plain")
#             part2 = MIMEText(html, "html")
#             # Add HTML/plain-text parts to MIMEMultipart message
#             # The email client will try to render the last part first
#             message.attach(part1)
#             message.attach(part2)

#             # Create secure connection with server and send email
#             context = ssl.create_default_context()
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                 server.login(sender_email, password)
#                 server.sendmail(
#                     sender_email, receiver_email, message.as_string()
#                 )

#             return {"message": "User added succesfully"}, 201

    # @blp.response(200, SuccessMessageSchema)
    # @blp.arguments(SignupQuerySchema, location="query")
    # def delete(self, args):
    #     id = args.get('id')
    #     if self.db.delete_user(id):
    #         return {'message': 'User deleted'}   
    #     abort(404, message="Given user id doesn't exist.")

 
# @blp.route("/new_interview")
# class NewInterview(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()
   
#     @blp.arguments(NewInterviewSchema)
#     def post(self, request_data):
#         #request_data = request.get_json()
#         #print(request_data)
#         username = request_data['candidatename']
#         emailid = request_data['emailid']
#         mobileno = request_data['mobileno']
#         jobprofile = request_data['jobprofile']
#         resume = request_data.__file__
#         keywords = request_data['keywords']
#         date = request_data['date']
#         time = request_data['time']
#         userid = request_data['userid']
#         #user_id = self.db.verify_user(username, password)
#         result = self.db.add_interview(username, emailid, mobileno, jobprofile, resume, keywords, date, time, userid)
#         if result:
#             return {
#                 "Message": "Interview Created Successfully",
#             }
#         abort(400, message="Username or password is incorrect")

# @blp.route("/chatbot")
# class Chatbot(MethodView):
#     def __init__(self):
#         self.db = UserDatabase()

#     @blp.arguments(ChatbotSchema)
#     def post(self, request_data):
#         #request_data = request.get_json()
#         #print(request_data)
#         role = request_data['role']
#         msg = request_data['content']
#         #user_id = self.db.verify_user(username, password)
#         result = self.db.ai_chat(msg)
#         if result:
#             return {
#                 "Message": result,
#             }
#         abort(400, message="Username or password is incorrect")

# @blp.route("/about")
# def chat():
#     return render_template('about.html')

# @blp.route("/")
# def chat():
#     return render_template('index.html')


# @blp.route("/userlist")
# class Bot(MethodView):

#     def __init__(self):
#         self.db = UserDatabase()

#     @blp.response(200, UserListSchema)
#     # @blp.arguments(UserListSchema, location="query")
#     def get(self):
#         result = self.get_subscriber_list()
#         if result is False:
#             abort(400, message="Please Try Again")
#         else:
#             return render_template('sample.html')
        
#     @blp.arguments(SignupSchema)
#     # @blp.response(200, SuccessMessageSchema)
#     def post(self, request_data):
#         # check if already exists
#         mobile = request_data["mobile"]
#         password = request_data["password"]
#         # password = hashlib.sha256(request_data["password"].encode('utf-8')).hexdigest()
#         emailid = request_data["emailid"]
#         #print(password)
#         # password = request_data["password"]
#         if self.db.verify_signup(mobile, password, emailid):
#             return abort(403, message="User already exists")
#         if self.db.add_user(mobile, password, emailid):
#             return {"message": "User added succesfully"}, 201

#     # @blp.response(200, SuccessMessageSchema)
#     @blp.arguments(SignupQuerySchema, location="query")
#     def delete(self, args):
#         id = args.get('id')
#         if self.db.delete_user(id):
#             return {'message': 'User deleted'}   
#         abort(404, message="Given user id doesn't exist.")

 
