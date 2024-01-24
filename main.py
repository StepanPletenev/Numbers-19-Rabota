import pygame
import random
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Чиселки")

font = pygame.font.SysFont(None, 36)

numbers = []
for i in range(10):
    numbers.append(str(i))

lines = []
for i in range(10):
    line = ""
    for j in range(10):
        line += random.choice(numbers)
    lines.append(line)
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_board():
    for i in range(10):
        for j in range(10):
            if lines[i][j] != " ":
                pygame.draw.rect(screen, GRAY, [j * 50, i * 50, 50, 50])
                draw_text(lines[i][j], font, WHITE, j * 50 + 25, i * 50 + 25)

def can_remove(x1, y1, x2, y2):
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            if lines[x1][i] == " ":
                return False
        return True
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2) + 1):
            if lines[i][y1] == " ":
                return False
        return True
    else:
        return False

def remove_numbers(x1, y1, x2, y2):
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            lines[x1] = lines[x1][:i] + " " + lines[x1][i+1:]
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2) + 1):
            lines[i] = lines[i][:y1] + " " + lines[i][y1+1:]

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x = pos[1] // 50
            y = pos[0] // 50
            if lines[x][y] != " ":
                if can_remove(x, y, x, y-1) or can_remove(x, y, x, y+1) or can_remove(x, y, x-1, y) or can_remove(x, y, x+1, y) or can_remove(x, y, x-1, y-1) or can_remove(x, y, x+1, y+1) or can_remove(x, y, x-1, y+1) or can_remove(x, y, x+1, y-1):
                    remove_numbers(x, y, x, y-1)
                    remove_numbers(x, y, x, y+1)
                    remove_numbers(x, y, x-1, y)
                    remove_numbers(x, y, x+1, y)
                    remove_numbers(x, y, x-1, y-1)
                    remove_numbers(x, y, x+1, y+1)
                    remove_numbers(x, y, x-1, y+1)
                    remove_numbers(x, y, x+1, y-1)

    screen.fill(WHITE)
    draw_board()

    game_over = True
    for line in lines:
        if " " not in line:
            game_over = False
            break
    if game_over:
        draw_text("Вы выиграли!", font, BLACK, WIDTH // 2, HEIGHT // 2)

    pygame.display.update()

pygame.quit()

