# For now everyhting is in one file

# Currently used by: Security class
import hashlib
import json
import random
import string
import base64
import time


# Currently used by MongoDB

# This class will be used for api class that will be needed through out the project 
# make sure to make keep thing neat and clean

class Helper:
    def __init__(self):
        return
    def generate_path(self):
        timestamp = str(time.time_ns())
        pool = string.printable
        random_characters = ""
        for i in range(25):
            addon = random.choice(pool)
            random_characters = random_characters + addon
        encoded = base64.b64encode(bytes(random_characters + timestamp, "utf-8"))
        return encoded


# For all the database that will be used in this project we can put htem inside this wrapper
# so that we can use it to help orgianizing the program
class MongoDB_wrapper:
    def __init__(self, mongoDB):
        self.database = mongoDB
        return

    def insert(self, InputData, tableName):
        currentTable = self.database[tableName]
        currentTable.insert_one(InputData)
        return

    def search(self, InputData, tableName):
        currentTable = self.database[tableName]
        search_result = currentTable.find_one(InputData)
        return search_result


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

    def generate_token(self, username, useragent):
        pool = string.printable
        timestamp = bytes(time.asctime(), "utf-8")
        random_characters = base64.b64encode(bytes("".join(random.sample(pool, 5)), "utf-8"))
        encoded_username = base64.b64encode(bytes(username, "utf-8"))
        encoded_useragent = base64.b64encode(bytes(useragent, "utf-8"))
        token = encoded_username + timestamp + random_characters + encoded_useragent
        hash_token = hashlib.sha256(token)
        return hash_token.hexdigest()
