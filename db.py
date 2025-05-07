import uuid
import mysql.connector
from mysql.connector import IntegrityError
from datetime import datetime
import random
import string

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
            
            # Return the inserted data as confirmation
            return {
                    "userid": userid,
                    "username": username,
                    "password": password,
                    "mobile": mobile,
                    "created_at": created_at.strftime("%d/%m/%Y %H:%M") if isinstance(created_at, (datetime,)) else str(created_at),
                    "last_login": last_login.strftime("%d/%m/%Y %H:%M") if isinstance(last_login, (datetime,)) else str(last_login),
                    "qms": bool(qms),
                    "aga": bool(aga),
                    "pushnotification": bool(pushnotification),
                    "bms": bool(bms),
                    "limit": user_limit
                }
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
                        "qms":bool(user["qms"]),
                        "aga":bool(user["aga"]),
                        "pushnotification":bool(user["pushnotification"]),
                        "bms":bool(user["bms"]),
                        "limit":user["limit"]
                        
                    }
                #return user  # or True if you just want a success indicator
            else:
                return None  # Invalid credentials
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return None
        
    def add_moist_history(self, id, userid, date, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId, qmsid, millerid, millername):
        try:
            # Convert the date string to a datetime object using the expected format
            moistdate_obj = datetime.strptime(date, '%d/%m/%Y %H:%M')
        except ValueError as ve:
            print("Date format error:", ve)
            return False
        query = """
        INSERT INTO MoistureHistory (userid, id, moistdate, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId, millerid, millername, qms_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (userid, id, moistdate_obj, commodity, lot, stack, moisture, temperature, humidity, depo, deviceId, millerid, millername, qmsid)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False
                
    def update_device_scan(self, userid, data):
        deviceid = data.get("deviceid")
        flag = data.get("flag")

        if not deviceid or flag is None:
            print("Missing deviceid or flag")
            return False

        # First, fetch the current values for the device
        select_query = """
        SELECT total_scan, above_limit, below_limit
        FROM user_device
        WHERE userid = %s AND deviceid = %s
        """
        try:
            self.cursor.execute(select_query, (userid, deviceid))
            result = self.cursor.fetchone()

            if not result:
                print("Device not found for update")
                return False

            total_scan = result["total_scan"]
            above_limit = result["above_limit"]
            below_limit = result["below_limit"]
            fetch_scan = total_scan
            fetch_above = above_limit
            fetch_below = below_limit
            # Increment values
            total_scan += 1
            if flag:
                above_limit += 1
            else:
                below_limit += 1
            update_query = """
            UPDATE user_device
            SET total_scan = %s, above_limit = %s, below_limit = %s
            WHERE userid = %s AND deviceid = %s
            """
            update_values = (total_scan, above_limit, below_limit, userid, deviceid)

            self.cursor.execute(update_query, update_values)
            self.conn.commit()

            return {
                "message": "Device scan updated successfully"
            }

        except Exception as e:
            self.conn.rollback()
            return {
               "message": "Database error",
               "error": str(e)
            }
    def get_moist_history_by_userid(self, userid):
        query = """
        SELECT * FROM MoistureHistory
        WHERE userid = %s
        ORDER BY moistdate DESC
        """
        try:
            self.cursor.execute(query, (userid,))
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as e:
            print("Database Error:", e)
            return []

    def update_user_profile(self, userid, fields_to_update):
        try:
            print("Incoming update fields:", fields_to_update)

            # Explicitly convert booleans to integers (MySQL stores 1/0)
            for key in ["qms", "bms", "aga", "pushnotification"]:
                value = fields_to_update[key]
                fields_to_update[key] = 1 if value else 0

            query = """
            UPDATE samvaad_user
            SET qms = %s, bms = %s, aga = %s, pushnotification = %s
            WHERE userid = %s
            """
            values = (
                fields_to_update["qms"],
                fields_to_update["bms"],
                fields_to_update["aga"],
                fields_to_update["pushnotification"],
                userid
            )

            print("Executing query:", query)
            print("With values:", values)

            self.cursor.execute(query, values)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                # Fetch and return the updated user data
                self.cursor.execute("SELECT * FROM samvaad_user WHERE userid = %s", (userid,))
                user = self.cursor.fetchone()

                if user:
                    return {
                        "userid": user["userid"],
                        "username": user["username"],
                        "password": user["password"],
                        "mobile": user["mobile"],
                        "created_at": str(user.get("createdat")),
                        "last_login": str(user.get("lastlogin")),
                        "qms": bool(user["qms"]),
                        "aga": bool(user["aga"]),
                        "pushnotification": bool(user["pushnotification"]),
                        "bms": bool(user["bms"]),
                        "limit": user["limit"]
                    }
            else:
                print("No rows updated.")
                return False

        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False

    def update_user_data(self, userid, fields_to_update):
        try:
            print("Incoming update fields:", fields_to_update)
            query = """
            UPDATE samvaad_user
            SET username = %s, password = %s, mobile = %s
            WHERE userid = %s
            """
            values = (
                fields_to_update["username"],
                fields_to_update["password"],
                fields_to_update["mobile"],
                userid
            )

            print("Executing query:", query)
            print("With values:", values)

            self.cursor.execute(query, values)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                # Fetch and return the updated user data
                self.cursor.execute("SELECT * FROM samvaad_user WHERE userid = %s", (userid,))
                user = self.cursor.fetchone()

                if user:
                    return {
                        "userid": user["userid"],
                        "username": user["username"],
                        "password": user["password"],
                        "mobile": user["mobile"],
                        "created_at": str(user.get("createdat")),
                        "last_login": str(user.get("lastlogin")),
                        "qms": bool(user["qms"]),
                        "aga": bool(user["aga"]),
                        "pushnotification": bool(user["pushnotification"]),
                        "bms": bool(user["bms"]),
                        "limit": user["limit"]
                    }
            else:
                print("No rows updated.")
                return False

        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False
        
    def update_moist_limit(self, userid, fields_to_update):
        try:
            print("Incoming update fields:", fields_to_update)
            query = """
            UPDATE samvaad_user
            SET `limit` = %s
            WHERE userid = %s
            """
            values = (
                fields_to_update["limit"],
                userid
            )

            print("Executing query:", query)
            print("With values:", values)

            self.cursor.execute(query, values)
            self.conn.commit()

            if self.cursor.rowcount > 0:
                # Fetch and return the updated user data
                self.cursor.execute("SELECT * FROM samvaad_user WHERE userid = %s", (userid,))
                user = self.cursor.fetchone()

                if user:
                    return {
                        "userid": user["userid"],
                        "username": user["username"],
                        "password": user["password"],
                        "mobile": user["mobile"],
                        "created_at": str(user.get("createdat")),
                        "last_login": str(user.get("lastlogin")),
                        "qms": bool(user["qms"]),
                        "aga": bool(user["aga"]),
                        "pushnotification": bool(user["pushnotification"]),
                        "bms": bool(user["bms"]),
                        "limit": user["limit"]
                    }
            else:
                print("No rows updated.")
                return False

        except mysql.connector.Error as e:
            print("Database Error:", e)
            return False
        
    def add_device(self, userid, deviceid, devicename, macaddress, charuuid, status,
               total_scan=0, above_limit=0, below_limit=0):
        query = """
        INSERT INTO user_device (userid, deviceid, devicename, macaddress, charuuid, status, total_scan, above_limit, below_limit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (userid, deviceid, devicename, macaddress, charuuid, status, total_scan, above_limit, below_limit)
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

    def edit_device(self, userid, deviceid, devicename, macaddress, charuuid):
        
        query = """
        UPDATE user_device
        SET devicename = %s, macaddress = %s, charuuid = %s
        WHERE deviceid = %s AND userid = %s
        """
        values = (devicename, macaddress, charuuid, deviceid, userid)

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

    def add_notification(self, id, userid, title, description, notif_date, notif_type, status):
        try:
            # Convert the date string to datetime object
            notif_date_obj = datetime.strptime(notif_date, '%d/%m/%Y %H:%M')
        except ValueError as ve:
            print("Date format error:", ve)
            return False
        query = """
        INSERT INTO notification (id, userid, title, description, date, type, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (id, userid, title, description, notif_date_obj, notif_type, status)
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
        ORDER BY date DESC
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
        
    def mark_notification_as_read(self, notif_id, status):
        query = "UPDATE notification SET status = FALSE WHERE id = %s"
        try:
            self.cursor.execute(query, (notif_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            print("Database Error (mark_notification_as_read):", e)
            return False

    def update_user_password(self, username, new_password):
        query = """
        UPDATE samvaad_user 
        SET password = %s 
        WHERE username = %s OR mobile = %s
        """
        try:
            self.cursor.execute(query, (new_password, username, username))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as e:
            print("Database Error (update_user_password):", e)
            return False

    def add_miller(self, request_data):
        millerid = request_data["millerid"]
        millername = request_data["millername"]
        userid = request_data["userid"]
        query = """
        INSERT INTO miller (millerid, millername, userid)
        VALUES (%s, %s, %s)
        """
        values = (millerid, millername, userid)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print("Database Error (add_miller):", e)
            return False

    def get_miller(self, request_data):
        userid = request_data.get("userid")
        sampleid = request_data.get("sampleid")
        query = """
        SELECT commodity, millername, lot
        FROM MoistureHistory
        WHERE userid = %s AND lot = %s
        """
        values = (userid, sampleid)

        try:
            self.cursor.execute(query, values)
            rows = self.cursor.fetchall()
            # columns = [col[0] for col in self.cursor.description]
            # result = [dict(zip(columns, row)) for row in rows]
            return rows
        except mysql.connector.Error as e:
            print("Database Error (get_moisture_history):", e)
            return []

    def get_miller_of_userid(self, request_data):
        userid = request_data.get("userid")
        query = """
        SELECT millername, millerid
        FROM miller
        WHERE userid = %s
        """
        values = (userid, )

        try:
            self.cursor.execute(query, values)
            rows = self.cursor.fetchall()
            # columns = [col[0] for col in self.cursor.description]
            # result = [dict(zip(columns, row)) for row in rows]
            return rows
        except mysql.connector.Error as e:
            print("Database Error (get_moisture_history):", e)
            return []


    def generate_qms_of_userid(self, request_data):
        qms_id = self.generate_random_qms_id()
        userid = request_data.get("userid")

        insert_query = """
        INSERT INTO UserQms (qms_id, userid, qmsstatus)
        VALUES (%s, %s, %s)
        """
        values = (qms_id, userid, True)

        try:
            self.cursor.execute(insert_query, values)
            self.conn.commit()
            return {"qms_id": qms_id}
        except mysql.connector.Error as e:
            print("Database Error (generate_qms_of_userid):", e)
            return {"error": "Database insertion failed"}
            
    def generate_random_qms_id(self):
        letters = ''.join(random.choices(string.ascii_lowercase, k=4))  # 4 letters
        numbers = ''.join(random.choices(string.digits, k=3))           # 3 numbers
        return f"samvaad-{letters}-{numbers}"

    def get_qms_of_userid(self, request_data):
        userid = request_data.get("userid")

        select_query = """
        SELECT qms_id FROM UserQms
        WHERE userid = %s
        ORDER BY created_at DESC
        LIMIT 1
        """
        try:
            self.cursor.execute(select_query, (userid,))
            result = self.cursor.fetchone()
        
            if result:  # Check if result is not None and has a value
                return {"qms_id": result["qms_id"]}  # result[0] is the qms_id
            else:
                return {"error": "No QMS ID found for the given user"}
    
        except mysql.connector.Error as e:
            print("Database Error (get_qms_of_userid):", e)
            return {"error": "Database query failed", "details": str(e)}
