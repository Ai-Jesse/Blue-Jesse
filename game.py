import random
import json
import time
import threading

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

class SingleGame():
    def __init__(self, socket):
        self.socket = socket
        
        self.snake = Snake("right", [
            {"x": 200, "y": 200},
            {"x": 190, "y": 200}
        ])
        self.board = Board(400, 400)
        self.food = gen_fruit(self.board, self.snake.parts)
        self.point = 0
        self.died = False
        self.win = False

        thread = threading.Thread(target=self.start)
        thread.start()

    def game_over(self, condition):
        pass

    def start(self):
        while not self.died and not self.win:
            time.sleep(.1)
            if self.snake.move_snake(self.food):
                self.food = gen_fruit(self.board, self.snake.parts)
                self.point += 10
            if self.board.hit_wall(self.snake.parts[0]) or self.snake.hit_self(self.snake.parts[0]):
                self.game_over("died")
                self.died = True

            data = {
                "snake": self.snake.parts,
                "food": {"x": self.food.x, "y": self.food.y},
                "died": self.died,
                "win": self.win,
                "point": self.point
            }

            self.socket.send(json.dumps(data))

    
    def handle(self, data):
        data = json.loads(data)
        
        direction = data["direction"]
        self.snake.change_direction(direction)


class MultiGame():
    games = {}
    def __init__(self, code):
        self.player = []
        self.code = code
        self.games[code] = self

        self.snake1 = Snake("right", [
            {"x": 100, "y": 200},
            {"x": 90, "y": 200}
        ])
        self.snake2 = Snake("left", [
            {"x": 700, "y": 200},
            {"x": 710, "y": 200}
        ])
        self.board = Board(800, 400)
        combined = []
        for i in self.snake1.parts:
            combined.append(i)
        for i in self.snake2.parts:
            combined.append(i)
        self.food = gen_fruit(self.board, combined)
        self.point1 = 0
        self.point2 = 0
        self.died1 = False
        self.died2 = False

    def game_over(self, condition):
        pass

    def start(self):
        while not self.died1 and not self.died2:
            time.sleep(.1)
            combined = []
            for i in self.snake1.parts:
                combined.append(i)
            for i in self.snake2.parts:
                combined.append(i)
            if self.snake1.move_snake(self.food):
                self.food = gen_fruit(self.board, combined)
                self.point1 += 10
            if self.snake2.move_snake(self.food):
                self.food = gen_fruit(self.board, combined)
                self.point2 += 10
            if self.board.hit_wall(self.snake1.parts[0]) or self.snake1.hit_self(self.snake1.parts[0]) or self.snake2.hit_self(self.snake1.parts[0], 0):
                self.game_over("died")
                self.died1 = True
            if self.board.hit_wall(self.snake2.parts[0]) or self.snake1.hit_self(self.snake2.parts[0], 0) or self.snake2.hit_self(self.snake2.parts[0]):
                self.game_over("died")
                self.died2 = True

            data = {
                "snake1": self.snake1.parts,
                "snake2": self.snake2.parts,
                "food": {"x": self.food.x, "y": self.food.y},
                "point1": self.point1,
                "point2": self.point2,
                "died1": self.died1,
                "died2": self.died2
            }

            for i in self.player:
                i["socket"].send(json.dumps(data))
        

    def leave(self, socket):
        # a player left the game, make the other player win
        pass

    def join(self, socket):
        self.player.append({"socket": socket, "username": "temp", "snake": len(self.player) + 1}) # join a player to game
        if len(self.player) == 2:
            thread = threading.Thread(target=self.start)
            thread.start()

    def handle(self, data, socket):
        data = json.loads(data)
        direction = data["direction"]
        player = None
        for i in self.player:
            if i["socket"] == socket:
                player = i["snake"]
        time.sleep(.05)
        if player == 1:
            self.snake1.change_direction(direction)
        if player == 2:
            self.snake2.change_direction(direction)
        

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
        for i in range(len(self.socket)): # find the correct player to remove
            if self.socket[i]["socket"] == socket:
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
