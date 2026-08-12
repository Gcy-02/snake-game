const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('high-score');
const gameOverModal = document.getElementById('gameOverModal');
const finalScoreElement = document.getElementById('finalScore');
const playerNameInput = document.getElementById('playerName');

const WIDTH = canvas.width;
const HEIGHT = canvas.height;
const BLOCK_SIZE = 20;
const SPEED = 150;

let gameLoopId;
let snake = [];
let snakeLength = 1;
let food = { x: 0, y: 0 };
let dx = 0;
let dy = 0;
let score = 0;
let highScore = 0;
let gameOver = false;

function initGame() {
    snake = [{ x: WIDTH / 2, y: HEIGHT / 2 }];
    snakeLength = 1;
    score = 0;
    gameOver = false;
    dx = 0;
    dy = 0;
    
    scoreElement.textContent = score;
    gameOverModal.classList.remove('show');
    
    generateFood();
    loadHighScore();
    gameLoop();
}

function generateFood() {
    food.x = Math.floor(Math.random() * (WIDTH / BLOCK_SIZE)) * BLOCK_SIZE;
    food.y = Math.floor(Math.random() * (HEIGHT / BLOCK_SIZE)) * BLOCK_SIZE;
    
    for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
            generateFood();
            return;
        }
    }
}

function loadHighScore() {
    fetch('/api/get_scores')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                highScore = data[0].score;
                highScoreElement.textContent = highScore;
            }
        })
        .catch(() => {
            highScoreElement.textContent = '0';
        });
}

function saveScore() {
    const playerName = playerNameInput.value.trim() || '匿名玩家';
    
    fetch('/api/save_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            player_name: playerName,
            score: score
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('分数保存成功！');
            loadHighScore();
        }
    })
    .catch(() => {
        alert('保存失败，请重试');
    });
}

function gameLoop() {
    if (gameOver) return;
    
    setTimeout(() => {
        update();
        render();
        gameLoop();
    }, SPEED);
}

function update() {
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };
    
    if (head.x < 0 || head.x >= WIDTH || head.y < 0 || head.y >= HEIGHT) {
        gameOver = true;
        showGameOver();
        return;
    }
    
    for (let segment of snake) {
        if (head.x === segment.x && head.y === segment.y) {
            gameOver = true;
            showGameOver();
            return;
        }
    }
    
    snake.unshift(head);
    
    if (head.x === food.x && head.y === food.y) {
        snakeLength++;
        score++;
        scoreElement.textContent = score;
        generateFood();
    } else {
        snake.pop();
    }
}

function render() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(food.x, food.y, BLOCK_SIZE - 2, BLOCK_SIZE - 2);
    
    for (let i = 0; i < snake.length; i++) {
        const segment = snake[i];
        if (i === 0) {
            ctx.fillStyle = '#22c55e';
        } else {
            ctx.fillStyle = '#4ade80';
        }
        ctx.fillRect(segment.x, segment.y, BLOCK_SIZE - 2, BLOCK_SIZE - 2);
    }
}

function showGameOver() {
    finalScoreElement.textContent = score;
    gameOverModal.classList.add('show');
    playerNameInput.value = '';
}

document.addEventListener('keydown', (e) => {
    if (gameOver) {
        if (e.key === 'c' || e.key === 'C') {
            initGame();
        } else if (e.key === 'q' || e.key === 'Q') {
            window.location.href = '/';
        }
        return;
    }
    
    switch (e.key) {
        case 'ArrowUp':
            if (dy === 0) {
                dx = 0;
                dy = -BLOCK_SIZE;
            }
            break;
        case 'ArrowDown':
            if (dy === 0) {
                dx = 0;
                dy = BLOCK_SIZE;
            }
            break;
        case 'ArrowLeft':
            if (dx === 0) {
                dx = -BLOCK_SIZE;
                dy = 0;
            }
            break;
        case 'ArrowRight':
            if (dx === 0) {
                dx = BLOCK_SIZE;
                dy = 0;
            }
            break;
    }
});

document.getElementById('restartBtn').addEventListener('click', () => {
    initGame();
});

document.getElementById('quitBtn').addEventListener('click', () => {
    window.location.href = '/';
});

document.getElementById('saveBtn').addEventListener('click', () => {
    saveScore();
});

initGame();
