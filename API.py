# For now everyhting is in one file


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
    def insert(self, InputData, TableName):
        return



# Security check goes here
class Security:
    def __init__(self):
        return
    def vaild_post_data(self,ExectedKeys:list, IcomingData:json):
        return
    