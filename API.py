# For now everyhting is in one file

# Currently used by: Security class
import hashlib
import json
import random
import string
import base64
import time
import bcrypt

# Currently used by MongoDB

# This class will be used for api class that will be needed through out the project 
# make sure to make keep thing neat and clean

class Helper:
    def __init__(self):
        return
    def Better_Print(self, input_name:str, value ):
        print(input_name + ": "+ str(value), flush=True)
    def generate_path(self):
        timestamp = str(time.time_ns())
        pool = string.ascii_letters
        random_characters = ""
        for i in range(25):
            addon = random.choice(pool)
            random_characters = random_characters + addon
        encoded = base64.b64encode(bytes(random_characters + timestamp, "utf-8"))
        return encoded
    def new_login(self, database, new_token, username):
        search_user = {"username": username}
        print(search_user, flush=True)
        old_token = database.search(search_user, "user_authorize_token").get("authorize_token")
        print("old token: " + str(old_token), flush=True)

        # Update token in user table
        replace_token_user = {"old_token": new_token}
        database.update(search_user, replace_token_user, "user")

        # Update token in user authorize token
        replace_token_user = {"authorize_token": new_token}
        database.update(search_user, replace_token_user, "user_authorize_token")

        # Update the temp_path
        search_temp_path = {"authorize_token": old_token}
        replace_temp_path = {"authorize_token": new_token, "path": self.generate_path()}
        database.update(search_temp_path, replace_temp_path, "temp_path")
        print(database, flush=True)

        # Update the user_stat
        search_user_stat = {"authorize_token": old_token}
        database.update(search_user_stat, replace_token_user, "user_stat")
        return None

    def leadboard_ranking_sort(self, ranking_item):
        return ranking_item["highest_point"]

    def gernate_xsrf_token(self, database, table):
        insert_data = {}



# For all the database that will be used in this project we can put htem inside this wrapper
# so that we can use it to help orgianizing the program
class MongoDB_wrapper:
    def __init__(self, mongoDB):
        self.database = mongoDB
        return

    def insert(self, InputData, tableName):
        currentTable = self.database[tableName]
        currentTable.insert_one(InputData)
        return None

    def search(self, InputData, tableName):
        currentTable = self.database[tableName]
        search_result = currentTable.find_one(InputData)
        return search_result
    def update(self, searchData, InputData, tableName):
        currentTable = self.database[tableName]
        update_value = {"$set": InputData}
        print("test")
        currentTable.update_one(searchData, update_value)
        return None

    def update_user_point(self, token, point):
        encoded_token = bytes(token, "utf-8")

        update_value = {"highest_point": point}
        search_user_stat = {"authorize_token": hashlib.sha256(encoded_token).hexdigest()}
        self.update(search_user_stat, update_value, "user_stat")

    def grab_user_stat(self, token):
        encoded_token = bytes(token, "utf-8")

        search_user_stat = {"authorize_token": hashlib.sha256(encoded_token).hexdigest()}
        user_data = self.search(search_user_stat, "user_stat")
        return user_data

    def grab_path(self, token):
        encoded_token = bytes(token, "utf-8")

        search_user_stat = {"authorize_token": hashlib.sha256(encoded_token).hexdigest()}

        path = self.search(search_user_stat, "temp_path")
        return path.get("path", None)
    def check_if_user_exist(self, token, username=None):
        # if no token
        if token == None:
            return False

        encoded_token = bytes(token, "utf-8")
        token_search = {"authorize_token": hashlib.sha256(encoded_token).hexdigest()}
        token_database_checker = self.search(token_search, "user_authorize_token")


        if token_database_checker == None:
            return False
        else:
            return True

    def check_if_path_exist(self, path, token):
        encoded_token = bytes(token, "utf-8")

        hashed_token = hashlib.sha256(encoded_token).hexdigest()
        print("hashed token: "+ str(hashed_token))
        if path == None:
            return None
        # Check if it is the user itself visting than we don't care if the profile is private or not
        print("my own path type" + str(type(path)))
        print("my own hash token type" + str(type(hashed_token)))
        path_encode = bytes(path, "utf-8")
        path_search = {"authorize_token": hashed_token, "path": path_encode}
        path_database_checker = self.search(path_search, "temp_path")
        print("path_database_check: " + str(path_database_checker), flush=True)
        for i in self.database["temp_path"].find():
            print("temp_path: " + str(i), flush=True)
            for key in i:
                print(str(key) + " type " + str(type(key)))
                print(str(i[key]) + " type " + str(type(i[key])))
        return path_database_checker
    def vist_public_profile(self, path, token):
        # Check if it is a public profile
        path_public_search = {"path": path, "profile_status": "public"}
        result = self.search(path_public_search, "temp_path")

        return result

    def check_if_token_exist(self, token):
        encoded_token = bytes(token, "utf-8")

        hashed_token = hashlib.sha256(encoded_token).hexdigest()
        token_search = {"authorize_token": hashed_token}

        resutl = self.search(token_search, "user_stat")
        return resutl

    def grab_all_user_stat(self):
        return self.database["user_stat"].find()


# Security check/things goes here
class Security:
    def __init__(self):
        return

    def vaild_post_data(self, ExectedKeys: list, IncomingData: json):
        return

    def hash_265(self, inputData):
        encoding_input = bytes(inputData, "utf-8")
        hashin = hashlib.sha256(encoding_input)
        return hashin.hexdigest()  # return the hash value

    def password_and_user_checker(self, username, password):
        bad_characters = ["/", "<", ">", ";", ")", "(", "&"]
        for character in bad_characters:
            # checking username and password
            if character in username or character in password:
                return True
        # if it does not
        return False
    def duplicate_username(self, username, database):
        search_user = {"username": username}
        current_user = database.search(search_user, "user")
        if current_user == None:
            return False
        else:
            return True

    def generate_token(self, username, useragent):
        pool = string.printable
        timestamp = bytes(time.asctime(), "utf-8")
        random_characters_unencoder = ""
        for i in range(20):
            random_characters_unencoder = random_characters_unencoder + random.choice(pool)

        # encoding the ranomd cahracgers
        random_characters = base64.b64encode(bytes(random_characters_unencoder, "utf-8"))

        encoded_username = base64.b64encode(bytes(username, "utf-8"))
        encoded_useragent = base64.b64encode(bytes(str(useragent), "utf-8"))
        token = encoded_username + timestamp + random_characters + encoded_useragent
        hash_token = hashlib.sha256(token)
        return (hash_token.hexdigest(), token)
    def hash_and_salt_password(self, password):
        encoded_password = bytes(password, "utf-8")
        hash_salt = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
        return hash_salt
    def check_password(self, password, hashed_password):
        encoded_password = bytes(password, "utf-8")
        return bcrypt.checkpw(encoded_password, hashed_password)
