import random
import json

class SingleGame():
    def __init__(self, socket):
        self.socket = socket

    def handle(self, data):
        self.socket.send(data)


class MultiGame():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

class Lobby():
    lobbies = {}

    def __init__(self):
        self.socket = []
        self.code = str(random.randint(1000, 9999))
        self.lobbies[self.code] = self
    
    def join(self, socket):
        self.socket.append(socket)

    def leave(self, socket):
        self.socket.remove(socket)
        if len(self.socket) == 0:
            del self.lobbies[self.code]
            del self

    def send_chat(self, data):
        message = data["message"]
        username = "temp"

        to_send = {"messageType": "chatMessage", "message": message, "username": username}
        to_send = json.dumps(to_send)
        for i in self.socket:
            i.send(to_send)
    
    def start_game(self):
        pass

    def handle(self, data, socket):
        data = json.loads(data)
        type = data["messageType"]

        if type == "leave":
            self.leave(socket)
        if type == "chatMessage":
            self.send_chat(data)
        if type == "start":
            self.start_game()
