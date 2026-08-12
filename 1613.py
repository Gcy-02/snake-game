import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 窗口设置
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 蛇方块大小、速度
BLOCK_SIZE = 20
SPEED = 15

# 字体
try:
    font = pygame.font.SysFont(None, 35)
except:
    font = pygame.font.Font(pygame.font.get_default_font(), 35)

# 显示文字函数
def show_text(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, (x, y))

# 游戏主逻辑
def game_loop():
    game_over = False
    game_close = False

    # 蛇初始坐标（屏幕中心）
    x, y = WIDTH / 2, HEIGHT / 2
    # 移动偏移
    x_change, y_change = 0, 0

    # 蛇身体列表
    snake_body = []
    snake_length = 1

    # 食物随机生成（对齐方块）
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    clock = pygame.time.Clock()

    while not game_over:
        # 游戏失败弹窗
        while game_close:
            screen.fill(BLACK)
            show_text("游戏结束！按Q退出，按C重新开始", RED, 60, 150)
            show_text(f"当前得分：{snake_length - 1}", WHITE, 180, 200)
            pygame.display.update()

            # 失败界面按键判断
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Q退出
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:  # C重开
                        game_loop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # 关闭窗口事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            # 方向键控制
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change != BLOCK_SIZE:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -BLOCK_SIZE:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != BLOCK_SIZE:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change != -BLOCK_SIZE:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # 撞墙判定
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(BLACK)

        # 绘制食物
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # 更新蛇头
        snake_head = [x, y]
        snake_body.append(snake_head)
        # 超出长度就删掉尾部（移动效果）
        if len(snake_body) > snake_length:
            del snake_body[0]

        # 撞到自己判定
        for seg in snake_body[:-1]:
            if seg == snake_head:
                game_close = True

        # 绘制整条蛇
        for seg in snake_body:
            pygame.draw.rect(screen, GREEN, [seg[0], seg[1], BLOCK_SIZE, BLOCK_SIZE])

        # 显示分数
        show_text(f"得分：{snake_length - 1}", WHITE, 10, 10)
        pygame.display.update()

        # 吃到食物：加长身体，刷新食物
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        clock.tick(SPEED)

    pygame.quit()
    sys.exit()

# 启动游戏
if __name__ == "__main__":
    game_loop()