# For now everyhting is in one file

import hashlib
import json # currently used by: Security class

# This class will be used for api class that will be needed through out the project 
# make sure to make keep thing neat and clean

class API:
    def __init__(self):
        return



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
    def vaild_post_data(self,ExectedKeys:list, IncomingData:json):
        return
    def hash_265(self, inputData):
        hashin = hashlib.sha256(inputData)
        return hashin.hexdigest() # return the has value
    def password_and_user_checker(self, username, password):
        bad_characters = ["/", "<", ">", ";", ")", "(", "&"]
        return bad_characters in username or bad_characters in password