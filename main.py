import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Чиселки 19")

font = pygame.font.SysFont(None, 36)

numbers = []
for i in range(1,10):
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

def draw_board(selected_numbers=None):
    for i in range(10):
        for j in range(10):
            if lines[i][j] != " ":
                color = GRAY
                if selected_numbers and (i, j) in selected_numbers:
                    color = GREEN
                pygame.draw.rect(screen, color, [j * 50, i * 50, 50, 50])
                draw_text(lines[i][j], font, WHITE, j * 50 + 25, i * 50 + 25)

def can_remove(x1, y1, x2, y2):
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            if lines[x1][i] == " ":
                return False
            elif not get_sum(lines[x1][i], lines[x1][y1]):
                return False
        return True
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2) + 1):
            if lines[i][y1] == " ":
                return False
            elif not get_sum(lines[i][y1], lines[x1][y1]):
                return False
        return True
    else:
        sum_positions = get_sum_positions()
        for pos1, pos2 in sum_positions:
            if (x1, y1) in pos1 and (x2, y2) in pos2:
                return True
        return False

def remove_numbers(x1, y1, x2, y2):
    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            lines[x1] = lines[x1][:i] + " " + lines[x1][i+1:]
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2) + 1):
            lines[i] = lines[i][:y1] + " " + lines[i][y1+1:]
    else:
        sum_positions = get_sum_positions()
        for pos1, pos2 in sum_positions:
            if (x1, y1) in pos1 and (x2, y2) in pos2:
                for x, y in pos1 + pos2:
                    lines[x] = lines[x][:y] + " " + lines[x][y+1:]

def get_sum(num1, num2):
    if num1 == '' or num2 =='':
        return False
    if int(num1) + int(num2) == 10:
        return True
    else:
        return False

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 200 <= pos[0] <= 400 and 300 <= pos[1] <= 350:
                    return

        screen.fill(WHITE)
        draw_text("Чиселки 19", font, BLACK, WIDTH // 2, HEIGHT // 2 -90)
        pygame.draw.rect(screen, GREEN, [200, 300, 200, 50])
        draw_text("Начать игру", font, BLACK, WIDTH // 2, 325)
        pygame.display.flip()

def game():
    running = True
    selected_numbers = []
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x = pos[1] // 50
                y = pos[0] // 50
                if len(selected_numbers) == 0:
                    if lines[x][y] != " ":
                        selected_numbers.append((x, y))
                elif len(selected_numbers) == 1:
                    if (x, y) != selected_numbers[0]:
                        if lines[x][y] != " " and (
                                can_remove(selected_numbers[0][0], selected_numbers[0][1], x, y) or get_sum(
                                lines[selected_numbers[0][0]][selected_numbers[0][1]], lines[x][y])):
                            remove_numbers(selected_numbers[0][0], selected_numbers[0][1], x, y)
                        selected_numbers.clear()
                else:
                    selected_numbers.clear()

        screen.fill(WHITE)
        draw_board(selected_numbers)

        game_over = True
        for line in lines:
            if " " not in line:
                game_over = False
                break
        if game_over:
            draw_text("Вы выиграли!", font, BLACK, WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

main_menu()
game()
pygame.quit()