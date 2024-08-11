import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Установка размеров окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Отскакивающий мяч")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Параметры мяча
BALL_RADIUS = 20
BALL_SPEED = 5

# Класс для мяча
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = pygame.math.Vector2(1, 1).normalize()

    def draw(self):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.direction.x * BALL_SPEED
        self.y += self.direction.y * BALL_SPEED

        # Проверка столкновения с краями окна
        if self.x <= 0 or self.x >= WIDTH:
            self.direction.x *= -1
        if self.y <= 0:
            self.direction.y *= -1
        elif self.y >= HEIGHT:
            # Случайный угол от -45 до 45 градусов
            random_angle = random.uniform(-math.pi/4, math.pi/4)
            self.direction = pygame.math.Vector2(math.cos(random_angle), -math.sin(random_angle))

# Класс для квадрата
class Square:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(win, self.color, self.rect)

# Функция для отрисовки объектов
def draw_window(ball, squares):
    win.fill(WHITE)
    ball.draw()
    for square in squares:
        square.draw()
    pygame.display.update()

# Основной цикл программы
def main():
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BLUE)
    squares = [Square(200, 200, 100, 100, RED), Square(500, 300, 80, 80, RED)]
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ball.update()

        # Проверка столкновения мяча с квадратами
        for square in squares:
            if ball.x - ball.radius < square.rect.right and ball.x + ball.radius > square.rect.left and \
               ball.y - ball.radius < square.rect.bottom and ball.y + ball.radius > square.rect.top:
                if ball.x < square.rect.left or ball.x > square.rect.right:
                    ball.direction.x *= -1
                if ball.y < square.rect.top or ball.y > square.rect.bottom:
                    ball.direction.y *= -1

        draw_window(ball, squares)
        clock.tick(60)

if __name__ == "__main__":
    main()
