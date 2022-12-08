import random
import json

class SingleGame():
    def __init__(self, socket):
        self.socket = socket

    def handle(self, data):
        self.socket.send(data)


class MultiGame():
    games = {}
    def __init__(self, code):
        self.player = []
        self.code = code
        self.games[code] = self

    def leave(self, socket):
        # a player left the game, make the other player win
        pass

    def join(self, socket):
        self.player.append({"socket": socket, "username": "temp", "ready": False}) # join a player to game

    def handle(self, data, socket):
        data = json.loads(data)
        type = data["messageType"]
        

class Lobby():
    lobbies = {}

    def __init__(self):
        self.socket = []
        self.code = str(random.randint(1000, 9999)) # generate room code
        while self.code in self.lobbies.keys():
            self.code = str(random.randint(1000, 9999))
        self.lobbies[self.code] = self # add room code and lobby to dictionary
    
    def join(self, socket):
        self.socket.append({"socket": socket, "username": "temp", "ready": False}) # join a player to room

    def leave(self, socket):
        for i in range(len(socket)): # find the correct player to remove
            if socket[i]["socket"] == socket:
                del self.socket[i]
        if len(self.socket) == 0: # if no more player, remove room
            del self.lobbies[self.code]
            del self

    def send_chat(self, data):
        message = data["message"]
        username = "temp"

        to_send = {"messageType": "chatMessage", "message": message, "username": username} # create message
        to_send = json.dumps(to_send)
        for i in self.socket: # send too all player
            i["socket"].send(to_send)
    
    def start_game(self, socket):
        for i in self.socket: # find the player and mark ready as true
            if i["socket"] == socket:
                i["ready"] = True
        if len(self.socket) == 2 and self.socket[0]["ready"] == True and self.socket[1]["ready"] == True: # start the game if both player are ready
            multi_game = MultiGame(self.code)
            to_send = {"messageType": "start"}
            to_send = json.dumps(to_send)
            for i in self.socket:
                i["socket"].send(to_send)
        

    def handle(self, data, socket):
        data = json.loads(data)
        type = data["messageType"]

        if type == "leave":
            self.leave(socket)
        if type == "chatMessage":
            self.send_chat(data)
        if type == "start":
            self.start_game(socket)
