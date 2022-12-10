const board_border = 'white';
const board_background = '#040406';
const snake_col_1 = 'green';
const snake_col_2 = 'blue';
const snake_border = 'darkblue';

// Get the canvas element
const snakeboard = document.getElementById("snakeboard");
// Return a two dimensional drawing context
const snakeboard_ctx = snakeboard.getContext("2d");
const code = window.location.href.slice(-4)
const socket = new WebSocket('ws://' + window.location.host + '/multigame/' + code);
socket.onmessage = function (ws_message) {
    const data = JSON.parse(ws_message.data);
    draw(data)
    // update_score(data.point1, data.point2)
    gameover(data.died1, data.died2, data.username1, data.username2)
}

// Draw game
function draw(data) {
    clearCanvas()
    // console.log(data)
    // console.log(data.snake1)
    // console.log(data.snake2)
    drawSnake(data.snake1,snake_col_1)
    drawSnake(data.snake2, snake_col_2)
    drawFood(data.food)
}

document.addEventListener("keydown", change_direction);

// draw a border around the canvas
function clearCanvas() {
    //  Select the colour to fill the drawing
    snakeboard_ctx.fillStyle = board_background;
    //  Select the colour for the border of the canvas
    snakeboard_ctx.strokestyle = board_border;
    // Draw a "filled" rectangle to cover the entire canvas
    snakeboard_ctx.fillRect(0, 0, snakeboard.width, snakeboard.height);
    // Draw a "border" around the entire canvas
    snakeboard_ctx.strokeRect(0, 0, snakeboard.width, snakeboard.height);
} 

function change_direction(event) {
    const LEFT_KEY = 37;
    const RIGHT_KEY = 39;
    const UP_KEY = 38;
    const DOWN_KEY = 40;

    // Prevent the snake from reversing
    const keyPressed = event.keyCode;
    if (keyPressed === LEFT_KEY) {
        sendMessage({"direction": "left"})
    }
    if (keyPressed === UP_KEY) {
        sendMessage({"direction": "up"})
    }
    if (keyPressed === RIGHT_KEY) {
        sendMessage({"direction": "right"})
    }
    if (keyPressed === DOWN_KEY) {
        sendMessage({"direction": "down"})
    }
}

function sendMessage(message) {
    message = JSON.stringify(message)
    socket.send(message)
}


// Draw the snake on the canvas
function drawSnake(snake, color) {
    // Draw each part
    for (i of snake){
        drawSnakePart(i,color)
    }
    // snake.forEach(drawSnakePart)
}

// Draw one snake part
function drawSnakePart(snakePart, color) {

    // Set the colour of the snake part
    snakeboard_ctx.fillStyle = color;
    // Set the border colour of the snake part
    snakeboard_ctx.strokestyle = snake_border;
    // Draw a "filled" rectangle to represent the snake part at the coordinates
    // the part is located
    snakeboard_ctx.fillRect(snakePart.x, snakePart.y, 10, 10);
    // Draw a border around the snake part
    snakeboard_ctx.strokeRect(snakePart.x, snakePart.y, 10, 10);
}

function drawFood(food) {
    snakeboard_ctx.fillStyle = 'red';
    snakeboard_ctx.strokestyle = 'darkgreen';
    snakeboard_ctx.fillRect(food.x, food.y, 10, 10);
    snakeboard_ctx.strokeRect(food.x, food.y, 10, 10);
}

// function update_score(score1, score2){
//     document.getElementById("points-1").innerHTML=score1;
//     document.getElementById("points-2"),innerHTML=score2;
// }

function gameover(dead1, dead2, username1, username2){
    if (dead1 && dead2){
        alert("Both lost the game");
        window.location.href="/userpage";

    }
    else if(dead2){
        alert("Game Over. " + username1 + " wins!");
        window.location.href="/userpage";

    }
    else if (dead1) {
        alert("Game Over. " + username2 + " wins!");
        window.location.href="/userpage";

    }
}