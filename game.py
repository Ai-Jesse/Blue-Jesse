import random
import json
import time
import threading
from API import Security
from API import Helper

helper = Helper()

class Snake():
    def __init__(self, direction, parts):
        self.direction = ""
        self.change_direction(direction)
        self.parts = parts

    def move_snake(self, food):
        head = {"x": self.parts[0]["x"] + self.dx, "y": self.parts[0]["y"] + self.dy}
        self.parts.insert(0, head)
        if not food.hit_food(head): # check if snake didn't hit food
            self.parts.pop(-1)
            return False
        return True

    def change_direction(self, direction):
        if direction == "left" and self.direction != "right":
            self.dx = -10
            self.dy = 0
            self.direction = direction
        elif direction == "up" and self.direction != "down":
            self.dx = 0
            self.dy = -10
            self.direction = direction
        elif direction == "right" and self.direction != "left":
            self.dx = 10
            self.dy = 0
            self.direction = direction
        elif direction == "down" and self.direction != "up":
            self.dx = 0
            self.dy = 10
            self.direction = direction

    def hit_self(self, head, same = 1):
        for i in range(same, len(self.parts)):
            if head["x"] == self.parts[i]["x"] and head["y"] == self.parts[i]["y"]:
                return True
        return False

def gen_fruit(board, snake):
    food_x = random.randrange(board.left_wall, board.right_wall, 10)
    food_y = random.randrange(board.top_wall, board.bottom_wall, 10)
    while True: # make sure food don't spawn on snake
        for i in snake:
            if i["x"] == food_x:
                food_x = random.randrange(board.left_wall, board.right_wall, 10)
                break
            if i["y"] == food_y:
                food_y = random.randrange(board.top_wall, board.bottom_wall, 10)
                break
        else:
            break

    fruit = Food(food_x, food_y)
    return fruit

class Food():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def hit_food(self, head):
        if head["x"] == self.x and head["y"] == self.y:
            return True
        return False

class Board():
    def __init__(self, width, height):
        self.left_wall = 0
        self.right_wall = width
        self.top_wall = 0
        self.bottom_wall = height

    def hit_wall(self, head):
        hit_left = head["x"] < self.left_wall;
        hit_right = head["x"] > self.right_wall - 10;
        hit_top = head["y"] < self.top_wall;
        hit_bottom = head["y"] > self.bottom_wall - 10;

        return hit_left or hit_right or hit_top or hit_bottom

class Player():
    def __init__(self, snake, socket=None, token=None, username=None, player_num = 1):
        self.player_num = player_num
        self.snake = snake
        self.username = username
        self.token = token
        self.died = False
        self.point = 0
        self.socket = socket

class SingleGame():
    def __init__(self, socket, token):
        self.socket = socket

        self.player = Player(
            Snake("right", [
                {"x": 200, "y": 200},
                {"x": 190, "y": 200}
            ]),
            token
        )

        self.board = Board(400, 400)
        self.food = gen_fruit(self.board, self.player.snake.parts)

        thread = threading.Thread(target=self.start)
        thread.start()

    def game_over(self):
        from app import mongo
        user_stat = mongo.grab_user_stat(self.player.token)

        prev_point = user_stat.get("highest_point", 0)
        if not prev_point or self.player.point > prev_point:
            mongo.update_user_point(self.player.token, self.player.point)

    def start(self):
        while not self.player.died:
            time.sleep(.1)
            if self.player.snake.move_snake(self.food):
                self.food = gen_fruit(self.board, self.player.snake.parts)
                self.player.point += 10
            if self.board.hit_wall(self.player.snake.parts[0]) or self.player.snake.hit_self(self.player.snake.parts[0]):
                self.player.died = True

            data = {
                "snake": self.player.snake.parts,
                "food": {"x": self.food.x, "y": self.food.y},
                "point": self.player.point,
                "died": self.player.died
            }

            if self.player.died:
                self.game_over()

            self.socket.send(json.dumps(data))

    
    def handle(self, data):
        data = json.loads(data)
        
        time.sleep(.1)
        direction = data["direction"]
        self.player.snake.change_direction(direction)


class MultiGame():
    games = {}
    def __init__(self, code):
        self.player1 = Player(
            Snake("right", [
                {"x": 100, "y": 200},
                {"x": 90, "y": 200}
            ]),
            player_num=1
        )

        self.player2 = Player(
            Snake("left", [
                {"x": 700, "y": 200},
                {"x": 710, "y": 200}
            ])  ,
            player_num=2
        )

        self.code = code
        self.games[code] = self
        self.game_start = False
        self.board = Board(800, 400)
        self.food = gen_fruit(self.board, self.player1.snake.parts + self.player2.snake.parts)

    def game_over(self, data):
        if self.player1.socket:
            self.player1.socket.close()
        if self.player2.socket:
            self.player2.socket.close()
        del self.games[self.code]
        time.sleep(10)
        

    def start(self):
        while not self.player1.died and not self.player2.died:
            time.sleep(.1)
            if self.player1.snake.move_snake(self.food):
                self.food = gen_fruit(self.board, self.player1.snake.parts + self.player2.snake.parts)
                self.point1 += 10
            if self.player2.snake.move_snake(self.food):
                self.food = gen_fruit(self.board, self.player1.snake.parts + self.player2.snake.parts)
                self.point2 += 10
            if self.board.hit_wall(self.player1.snake.parts[0]) or self.player1.snake.hit_self(self.player1.snake.parts[0]) or self.player2.snake.hit_self(self.player1.snake.parts[0], 0):
                self.player1.died = True
            if self.board.hit_wall(self.player2.snake.parts[0]) or self.player1.snake.hit_self(self.player2.snake.parts[0], 0) or self.player2.snake.hit_self(self.player2.snake.parts[0]):
                self.player2.died = True

            data = {
                "snake1": self.player1.snake.parts,
                "snake2": self.player2.snake.parts,
                "food": {"x": self.food.x, "y": self.food.y},
                "point1": self.player1.point,
                "point2": self.player2.point,
                "died1": self.player1.died,
                "died2": self.player2.died
            }

            if self.player1.died or self.player2.died:
                self.game_over(data)

            if self.player1.socket:
                self.player1.socket.send(json.dumps(data))
            if self.player2.socket:
                self.player2.socket.send(json.dumps(data))
        

    def leave(self, socket):
        if self.player1.socket == socket:
            self.player1.socket = None
            self.player1.died = True
        elif self.player2.socket == socket:
            self.player2.socket = None
            self.player2.died = True

    def join(self, socket, token):
        from app import mongo
        username = mongo.grab_user_stat(token).get("username")
        if not self.player1.socket:
            self.player1.socket = socket
            self.player1.token = token
            self.player1.username = username
        else:
            self.player2.socket = socket
            self.player2.token = token
            self.player2.username = username
        
            self.game_start = True
            thread = threading.Thread(target=self.start)
            thread.start()

    def handle(self, data, socket):
        data = json.loads(data)
        direction = data["direction"]

        time.sleep(.1)
        if self.player1.socket == socket:
            self.player1.snake.change_direction(direction)
        if self.player2.socket == socket:
            self.player2.snake.change_direction(direction)
        

class Lobby():
    lobbies = {}

    def __init__(self):
        self.socket = []
        self.chat_history = []
        self.code = str(random.randint(1000, 9999)) # generate room code
        while self.code in self.lobbies.keys():
            self.code = str(random.randint(1000, 9999))
        self.lobbies[self.code] = self # add room code and lobby to dictionary
    
    def join(self, socket, token):
        from app import mongo
        username = mongo.grab_user_stat(token).get("username")
        self.socket.append({"socket": socket, "username": "temp", "ready": False, "username": username, "token": token}) # join a player to room
        for i in self.chat_history:
            socket.send(i)

    def leave(self, socket):
        for i in range(len(self.socket)): # find the correct player to remove
            if self.socket[i]["socket"] == socket:
                del self.socket[i]
        if len(self.socket) == 0: # if no more player, remove room
            del self.lobbies[self.code]
            del self

    def send_chat(self, data, socket):
        xsrf_token = data["xsrf_token"]
        s = Security()
        message = data["message"]
        auth_token = None
        for i in self.socket:
            if i["socket"] == socket:
                username = i["username"]
                auth_token = i["token"]
        
        from app import mongo
        if not helper.check_xsrf_token(xsrf_token, auth_token, mongo, "chat_xsrf"):
            socket.send(json.dumps({"messageType": "leave"}))
            self.leave(socket)
            return
        
        escaped_message = s.escapeHTML(message)
        escaped_username = s.escapeHTML(username)

        to_send = {"messageType": "chatMessage", "message": escaped_message, "username": escaped_username} # create message
        to_send = json.dumps(to_send)
        self.chat_history.append(to_send)
        for i in self.socket: # send too all player
            i["socket"].send(to_send)
    
    def start_game(self, socket):
        for i in self.socket: # find the player and mark ready as true
            if i["socket"] == socket:
                i["ready"] = True
        if len(self.socket) == 2 and self.socket[0]["ready"] == True and self.socket[1]["ready"] == True: # start the game if both player are ready
            code = str(random.randint(1000, 9999)) # generate room code
            while code in MultiGame.games.keys():
                code = str(random.randint(1000, 9999))
            multi_game = MultiGame(code)
            
            to_send = {"messageType": "start", "code": code}
            to_send = json.dumps(to_send)
            for i in self.socket:
                i["socket"].send(to_send)
        

    def handle(self, data, socket):
        data = json.loads(data)
        type = data["messageType"]

        if type == "chatMessage":
            self.send_chat(data, socket)
        if type == "start":
            self.start_game(socket)
