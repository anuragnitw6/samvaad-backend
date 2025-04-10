
# import json
# import pyodbc
# import uuid
# import random
# import json

# import torch
# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# import random
# # from model import NeuralNet
# # from nltk_utils import bag_of_dazzy, bag_of_words, tokenize
# # from gtts import gTTS 
# import os
# # import playsound
# import time
# # import news
# import mysql.connector
# from mysql.connector import errorcode

# class UserDatabase:
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root@localhost",
#             password="Admin123!",
#             database="my_nw"
#         )
#         self.cursor = self.conn.cursor()
#         # self.conn = pyodbc.connect(
#         #     'DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:audiobookdb.database.windows.net,1433;Encrypt=yes;TrustServerCertificate=no;DATABASE=audiotune;UID=audiobookdb;PWD=@nurAgmishr@12')
#         # self.cursor = self.conn.cursor()

#     def get_user(self, username, password):
#         query = f"SELECT * FROM users WHERE mobile = '{username}' OR emailid = '{username}' AND password = '{password}'"
#         #query2 = f"SELECT * FROM interviews WHERE UserID= '{id}"
#         self.cursor.execute(query)
#         result = self.cursor.fetchone()
#         if result is not None:
#             return result

#     def add_user(self, id,username,password,mobile,created_at,last_login):
#         # print(password)
#         uid = uuid.uuid4().hex
#         #print(uid)
#         query = f"INSERT INTO users(userid,username, password, mobile,created_at,last_login) VALUES('{id}','{username}', '{password}', '{mobile}','{created_at}','{last_login}')"
#         try:
#             self.cursor.execute(query)
#             self.conn.commit()
#             return True
#         except pyodbc.IntegrityError:
#             return False

#     def delete_user(self, id):
#         query = f"DELETE FROM users WHERE id = {id}"
#         self.cursor.execute(query)
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return True

#     def verify_user(self, username, password):
#         query = f"SELECT userid FROM users WHERE username = '{username}' AND passcode = '{password}'"
#         self.cursor.execute(query)
#         result = self.cursor.fetchone()
#         if result is not None:
#             return result[0]
        
#     def verify_signup(self, mobile, password, emailid):
#         query = f"SELECT mobile,password,emailid FROM users WHERE mobile='{mobile}' OR password='{password}' OR emailid='{emailid}'"
#         self.cursor.execute(query)
#         # news.server.login
#         # news.server.send
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return True
        
#     def verify_email(self, emailid):
#         sender_email = "noreplyaudiotune@gmail.com"
#         receiver_email = emailid
#         password = 'qjuwduthphcmilxb'

#         message = MIMEMultipart("alternative")
#         message["Subject"] = "One Time Password - Podio"
#         message["From"] = sender_email
#         message["To"] = receiver_email  
#         message['X-Priority'] = '3'
#         message["X-MSMail-Priority"] = 'Normal'
#         message['Importance'] = 'Normal'
#         minimum = 100000
#         maximum = 1000000

#         otp = minimum+int(random.random()*(maximum-minimum))

#         html = """\
#         <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
#         <div style="margin:50px auto;width:70%;padding:20px 0">
#             <div style="border-bottom:1px solid #eee">
#                 <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
#                 </div>
#                 <p style="font-size:1.1em">Hi,</p>
#                 <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
#                 <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">""" + str(otp) + """</h2>
#                 <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
#                 <hr style="border:none;border-top:1px solid #eee" />
#                 <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
#                     <p>Your Brand Inc</p>
#                     <p>1600 Amphitheatre Parkway</p>
#                     <p>California</p>
#                 </div>
#             </div>
#         </div>
#         """
        
#         # Turn these into plain/html MIMEText objects
#         # part1 = MIMEText(text, "plain")
#         part2 = MIMEText(html, "html")

#         # Add HTML/plain-text parts to MIMEMultipart message
#         # The email client will try to render the last part first
#         # message.attach(part1)
#         message.attach(part2)

#         # Create secure connection with server and send email
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(
#                 sender_email, receiver_email, message.as_string()
#                 )
#         return otp

#         # return {"otp":"12345","email":"emailid"}
        
#     def save_user(self, name,userid,email,login_time):
#         query4 = f"SELECT * FROM users where CONVERT(VARCHAR,email) = '{email}'"
#         self.cursor.execute(query4)
#         user_exist = self.cursor.fetchone()
#         if user_exist is not None:
#             self.conn.commit()
#             return False
#         query = f"INSERT INTO users(user_id,username,email,mobile) VALUES('{userid}', '{name}','{email}','{9999999999}')"
#         query1 = f"INSERT INTO planstatus(user_id,status) VALUES('{userid}', '0')"
#         query2 = f"INSERT INTO user_login(user_id,login_time,logout_time,last_track_id,last_track_time) VALUES('{userid}', '{login_time}','0','0','0')"
#         query3 = f"INSERT INTO payment(user_id,order_id,reciept_id,amount_paid,amount_due,offer_id,amount,pay_date) values('{userid}','0','0','0','99','0','99',null)"
#         try:
#             self.cursor.execute(query)
#             self.cursor.execute(query1)
#             self.cursor.execute(query2)
#             self.cursor.execute(query3)
#             self.conn.commit()
#             return True
#         except pyodbc.IntegrityError:
#             return False
        
#     def delete_user(self,user_id):
#         query = f"delete from users where user_id = '{user_id}'"
#         self.cursor.execute(query)
#         query1 = f"delete from user_login where user_id = '{user_id}'"
#         self.cursor.execute(query1)
#         self.conn.commit()
#         return True
    
#     def create_visitor(self, cst_id,name,email,mobile,passcode,cart_id):
#         query = f"INSERT INTO customers(cst_id,name,email,mobile,passcode,cart_id) VALUES('{cst_id}','{name}', '{mobile}','{passcode}','{passcode}','{cart_id}')"
#         self.cursor.execute(query)
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return True
            
#     def visitor_login(self, email,login_time):
#         query = f"select * from users where CONVERT(VARCHAR, email)='{email}'"
#         self.cursor.execute(query)
#         result = self.cursor.fetchone()
#         if result is None:
#             return False
#         sender_email = "noreplyaudiotune@gmail.com"
#         receiver_email = email
#         password = 'qjuwduthphcmilxb'

#         message = MIMEMultipart("alternative")
#         message["Subject"] = "One Time Password - Podio"
#         message["From"] = sender_email
#         message["To"] = receiver_email  
#         message['X-Priority'] = '3'
#         message["X-MSMail-Priority"] = 'Normal'
#         message['Importance'] = 'Normal'
#         minimum = 100000
#         maximum = 1000000

#         otp = minimum+int(random.random()*(maximum-minimum))

#         html = """\
#         <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
#         <div style="margin:50px auto;width:70%;padding:20px 0">
#             <div style="border-bottom:1px solid #eee">
#                 <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
#                 </div>
#                 <p style="font-size:1.1em">Hi,</p>
#                 <p>Thank you for choosing Your Brand. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
#                 <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">""" + str(otp) + """</h2>
#                 <p style="font-size:0.9em;">Regards,<br />Your Brand</p>
#                 <hr style="border:none;border-top:1px solid #eee" />
#                 <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
#                     <p>Your Brand Inc</p>
#                     <p>1600 Amphitheatre Parkway</p>
#                     <p>California</p>
#                 </div>
#             </div>
#         </div>
#         """
        
#         # Turn these into plain/html MIMEText objects
#         # part1 = MIMEText(text, "plain")
#         part2 = MIMEText(html, "html")

#         # Add HTML/plain-text parts to MIMEMultipart message
#         # The email client will try to render the last part first
#         # message.attach(part1)
#         message.attach(part2)

#         # Create secure connection with server and send email
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(
#                 sender_email, receiver_email, message.as_string()
#                 )
        
#         user_id = result[0]
#         query1 = f"select * from user_login where user_id = '{user_id}'"
#         self.cursor.execute(query1)
#         track_login = self.cursor.fetchone()
#         print(track_login)
#         if track_login[2] != "0":
#             return {"message":"You are already logged in to other device"}
#         query1 = f"UPDATE user_login set login_time = '{login_time}',logout_time = null where user_id = '{user_id}'"
#         self.cursor.execute(query1)
#         query = f"select * from planstatus where user_id = '{user_id}'"
#         self.cursor.execute(query)
#         plan = self.cursor.fetchone()
#         status = '0'
#         if plan is not None:
#             status = plan[1]
#         #if self.cursor.rowcount == 0:
#         #    return False
#         #else:
#         self.conn.commit()
#         return {"user_id":user_id,"name":result[1],"email":result[2],"status":status,"last_track_id":track_login[1],"track_time":track_login[4],"otp":otp}
        
#     def add_audio(self, audio_id,title,description,rating,author,link,length,totalpart,image_url,keywords,drive_link,language):
#         query = f"INSERT INTO parentAudio(parent_id,title,description,rating,author,link,length,totalpart,image_url,keywords,drive_link,lang) VALUES('{audio_id}','{title}', '{description}','{rating}','{author}','{link}','{length}','{totalpart}','{image_url}','{keywords}','{drive_link}','{language}')"
#         self.cursor.execute(query)
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return True
    
#     def user_logout(self,user_id,logout_time,track_id,track_time):
#         query = f"update user_login set login_time = '0', logout_time = '{logout_time}', last_track_id = '{track_id}', last_track_time = '{track_time}' where user_id = '{user_id}'"
#         self.cursor.execute(query)
#         self.conn.commit()
#         return True
 
#     def add_favourite(self, parentid,user_id):
#         query = f"INSERT INTO favouriteaudio(parentid,user_id) VALUES('{parentid}','{user_id}')"
#         self.cursor.execute(query)
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return True
    
#     def guest_search(self, query):
#         query = f"SELECT * FROM parentAudio where CONVERT(VARCHAR,keywords) = '{query}'"
#         self.cursor.execute(query)
#         result = self.cursor.fetchall()
#         search = list()
#         for i,row in result:
#             abc = {}
#             abc['parent_id'] = row[0]
#             abc['title'] = row[1]
#             abc['description'] = row[2]
#             abc['rating'] = row[3]
#             abc['author'] = row[4]
#             abc['link'] = row[5]
#             abc['length'] = row[6]
#             abc['totalpart'] = row[7]
#             abc['image_url'] = row[8]
#             abc['keywords'] = row[9]
#             search.append(abc)
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return {"data":search}
        
#     def get_favourite(self, query):
#         query = f"SELECT * FROM favourite_audio where CONVERT(VARCHAR,user_id) = '{query}'"
#         self.cursor.execute(query)
#         result = self.cursor.fetchall()
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return {"data":result}
            
#     def remove_favourite(self, parent_id,user_id):
#         query = f"DELETE FROM favourite_audio WHERE user_id = '{user_id}' and parent_id = '{parent_id}'"
#         self.cursor.execute(query)
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return True
        
#     def plan_status(self, user_id):
#         query = f"select * FROM planstatus WHERE user_id = '{user_id}'"
#         self.cursor.execute(query)
#         result = self.cursor.fetchall()
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             return {"data":result}
        
#     def home_page(self, query):
#         if query == 'locate':
#             query1 = f"SELECT * FROM parentAudio"
#             self.cursor.execute(query1)
#             result = self.cursor.fetchall()
#             audio = list()
#             # json_string = json.dumps(result)
#             # print(json_string)
#         # if self.cursor.rowcount == 0:
#         #     return False
#         # else:
#             self.conn.commit()
#             for i,row in enumerate(result):
#                 # print(row[i])
#                 abc = {}
#                 abc['parent_id'] = row[0]
#                 abc['title'] = row[1]
#                 abc['description'] = row[2]
#                 abc['rating'] = row[3]
#                 abc['author'] = row[4]
#                 abc['link'] = row[5]
#                 abc['length'] = row[6]
#                 abc['totalpart'] = row[7]
#                 abc['image_url'] = row[8]
#                 abc['keywords'] = row[9]
#                 abc['drive_link'] = row[10]
#                 abc['lang'] = row[11]
#                 # i = i+1
#                 audio.append(abc)
#             return {"audio":audio}
        
#     def get_restaurant_details(self, rst_id):
#         query = f"SELECT * FROM items where rst_id = '{rst_id}'"
#         self.cursor.execute(query)
#         result = self.cursor.fetchall()
#         rest = list()
#         if self.cursor.rowcount == 0:
#             return False
#         else:
#             self.conn.commit()
#             for i,row in enumerate(result):
#                 abc = {};
#                 abc['item_id'] = row[0]
#                 abc['name'] = row[1]
#                 abc['price'] = row[3]
#                 abc['category'] = row[4]
#                 abc['rst_id'] = row[5]
#                 rest.append(abc)
#             return {"items":rest}
    

#     def place_order(self, user_id,order_id,amount,amount_paid,amount_due,receipt,payment_date):
        
#         query1 = f"UPDATE payment set order_id = '{order_id}',reciept_id='{receipt}',amount_paid='{amount_paid}',amount_due='{amount_due}',offer_id='0',amount='{amount}' where user_id = '{user_id}'"
#         self.cursor.execute(query1)
#         query = f"UPDATE planstatus set status = '1' where user_id = '{user_id}'"
#         self.cursor.execute(query)
#         #if self.cursor.rowcount == 0:
#         #    return False
#         #else:
#         self.conn.commit()
#         return True
        
import uuid
import mysql.connector
from mysql.connector import IntegrityError

class UserDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Admin123!',
            database='my_nw'
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def add_user(self, username, password, mobile, created_at, last_login, qms=True, aga=True, pushnotification=True, bms=True, user_limit=15):
        userid = uuid.uuid4().hex
        query = """
        INSERT INTO samvaad_user (userid, username, password, mobile, createdat, lastlogin, qms, aga, pushnotification, bms, `limit`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (userid, username, password, mobile, created_at, last_login, qms, aga, pushnotification, bms, user_limit)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print("IntegrityError:", e)
            return False
        
    def signin_user(self, username, password):
        query = """
        SELECT * FROM samvaad_user
        WHERE (username = %s OR mobile = %s) AND password = %s
        """
        values = (username, username, password)

        try:
            self.cursor.execute(query, values)
            user = self.cursor.fetchone()
            print("Fetched user:", user)  # Debug: See what's being returned

            if user:
                userid = user["userid"]
                # Optionally update last_login time here
                update_query = "UPDATE samvaad_user SET lastlogin = NOW() WHERE userid = %s"
                self.cursor.execute(update_query, (userid,))
                self.conn.commit()
                # Only return required fields
                return {
                        "userid": userid,
                        "username": user["username"],
                        "password": user["password"],
                        "mobile": user["mobile"],
                        "lastlogin": str(user.get("lastlogin")),
                        "qms":user["qms"],
                        "aga":user["aga"],
                        "pushnotification":user["pushnotification"],
                        "bms":user["bms"],
                        "limit":user["limit"]
                        
                    }
                #return user  # or True if you just want a success indicator
            else:
                return None  # Invalid credentials
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return None
        
    def add_moist_history(self, userid, date, time, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId):
        query = """
        INSERT INTO moist_history (userid, date, time, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (userid, date, time, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False
        
    def get_moist_history_by_userid(self, userid):
        query = """
        SELECT * FROM moist_history
        WHERE userid = %s
        ORDER BY date DESC, time DESC
        """
        try:
            self.cursor.execute(query, (userid,))
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return []
    
    def update_user_profile(self, userid, fields_to_update):
        if not fields_to_update:
                print("No fields to update.")
                return False

        try:
                set_clause = ", ".join([f"{key} = %s" for key in fields_to_update])
                values = list(fields_to_update.values())
                values.append(userid)
                query = f"UPDATE samvaad_user SET {set_clause} WHERE userid = %s"
                print("Executing query:", query)
                print("With values:", values)
                self.cursor.execute(query, values)
                self.conn.commit()

                if self.cursor.rowcount > 0:
                    return True
                else:
                    print("Update query ran, but no rows affected.")
                    return False

        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False

        
        
    def add_device(self, userid, deviceid, devicename, macaddress, charuuid, status):
        query = """
        INSERT INTO user_device (userid, deviceid, devicename, macaddress, charuuid, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (userid, deviceid, devicename, macaddress, charuuid, status)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False

    def get_devices_by_userid(self, userid):
        query = "SELECT * FROM user_device WHERE userid = %s"
        try:
            self.cursor.execute(query, (userid,))
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return []

    def edit_device(self, deviceid, devicename=None, macaddress=None, charuuid=None, status=None):
        updates = []
        values = []

        if devicename is not None:
            updates.append("devicename = %s")
            values.append(devicename)
        if macaddress is not None:
            updates.append("macaddress = %s")
            values.append(macaddress)
        if charuuid is not None:
            updates.append("charuuid = %s")
            values.append(charuuid)
        if status is not None:
            updates.append("status = %s")
            values.append(status)

        values.append(deviceid)

        query = f"UPDATE user_device SET {', '.join(updates)} WHERE deviceid = %s"
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False

    def get_device_history(self, deviceid):
        query = "SELECT * FROM moist_history WHERE deviceId = %s ORDER BY date DESC, time DESC"
        try:
            self.cursor.execute(query, (deviceid,))
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return []

    def add_notification(self, userid, title, description, date, time, notif_type, status=False):
        query = """
        INSERT INTO notification (userid, title, description, date, time, type, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (userid, title, description, date, time, notif_type, status)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error (add_notification):", e)
            return False
        
    def get_notifications_by_userid(self, userid):
        query = """
        SELECT * FROM notification
        WHERE userid = %s
        ORDER BY date DESC, time DESC
        """
        try:
            self.cursor.execute(query, (userid,))
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print("Database Error (get_notifications_by_userid):", e)
            return []
        
    def delete_notification_by_id(self, notif_id):
        query = "DELETE FROM notification WHERE id = %s"
        try:
            self.cursor.execute(query, (notif_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            print("Database Error (delete_notification_by_id):", e)
            return False
        
    def mark_notification_as_read(self, notif_id):
        query = "UPDATE notification SET status = TRUE WHERE id = %s"
        try:
            self.cursor.execute(query, (notif_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            print("Database Error (mark_notification_as_read):", e)
            return False

