import pygame
import random

if __name__ == "__main__":
    pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

WIDTH = 600
HEIGHT = 600

menu_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

font = pygame.font.SysFont("helvetica", 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    menu_screen.blit(text_surface, text_rect)

game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игровое окно")

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
    if text_surface is not None:
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        menu_screen.blit(text_surface, text_rect)


def draw_board(selected_numbers=None):
    for i in range(10):
        for j in range(10):
            if lines[i][j] != " ":
                color = GRAY
                if selected_numbers and (i, j) in selected_numbers:
                    color = GREEN
                pygame.draw.rect(game_screen, color, [j * 50, i * 50, 50, 50])
                draw_text(lines[i][j], font, WHITE, j * 50 + 25, i * 50 + 25)

def can_remove(x1, y1, x2, y2):
    if x1 < 0 or x1 >= len(lines) or y1 < 0 or y1 >= len(lines[0]) or x2 < 0 or x2 >= len(lines) or y2 < 0 or y2 >= len(lines[0]):
        return False

    if lines[x1][y1] == " " or lines[x2][y2] == " ":
        return False

    num1 = int(lines[x1][y1])
    num2 = int(lines[x2][y2])

    if num1 + num2 == 10:
        return True
    else:
        return False

def remove_numbers(x1, y1, x2, y2):
    if x1 < 0 or x1 >= len(lines) or y1 < 0 or y1 >= len(lines[0]) or x2 < 0 or x2 >= len(lines) or y2 < 0 or y2 >= len(lines[0]):
        return
    lines[x1] = lines[x1][:y1] + " " + lines[x1][y1+1:]
    lines[x2] = lines[x2][:y2] + " " + lines[x2][y2+1:]

def get_sum(num1, num2):
    if num1 == '' or num2 =='':
        return False
    if int(num1) + int(num2) == 10:
        return True
    else:
        return False
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

                if len(selected_numbers) < 2:
                    if lines[x][y] != " ":
                        selected_numbers.append((x, y))

                if len(selected_numbers) == 2:
                    x1, y1 = selected_numbers[0]
                    x2, y2 = selected_numbers[1]

                    if can_remove(x1, y1, x2, y2):
                        remove_numbers(x1, y1, x2, y2)
                        selected_numbers = []
                    else:
                        selected_numbers = []

        game_screen.fill(WHITE)
        draw_board(selected_numbers)

        game_over = True
        for line in lines:
            if " " not in line:
                game_over = False
                break

        if game_over:
            draw_text("Вы выиграли!", font, BLACK, WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()

game()
pygame.quit()