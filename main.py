import pygame
import random

if __name__ == "__main__":
    pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Game Window")

font = pygame.font.SysFont("helvetica", 36)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    game_screen.blit(text_surface, text_rect)

numbers = [str(i) for i in range(1, 10)]

lines = []
for _ in range(15):
    line = ""
    for _ in range(15):
        line += random.choice(numbers)
    lines.append(line)

def draw_board(selected_numbers=None):
    for i in range(15):
        for j in range(15):
            if lines[i][j] != " ":
                color = GRAY
                if selected_numbers and (i, j) in selected_numbers:
                    color = GREEN
                pygame.draw.rect(game_screen, color, [j * 50, i * 50, 50, 50])
                draw_text(lines[i][j], font, WHITE, j * 50 + 25, i * 50 + 25 )

def can_remove(x1, y1, x2, y2):
    if not (0 <= x1 < len(lines) and 0 <= y1 < len(lines[0]) and 0 <= x2 < len(lines) and 0 <= y2 < len(lines[0])):
        return False

    if lines[x1][y1] == " " or lines[x2][y2] == " ":
        return False

    num1 = int(lines[x1][y1])
    num2 = int(lines[x2][y2])

    return num1 + num2 == 10 and (x1 == x2 or y1 == y2)

def remove_numbers(x1, y1, x2, y2):
    if not (0 <= x1 < len(lines) and 0 <= y1 < len(lines[0]) and 0 <= x2 < len(lines) and 0 <= y2 < len(lines[0])):
        return

    lines[x1] = lines[x1][:y1] + " " + lines[x1][y1+1:]
    lines[x2] = lines[x2][:y2] + " " + lines[x2][y2+1:]

def game():
    selected_numbers = []
    running = True
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

        game_over = all(" " in line for line in lines)
        if game_over:
            draw_text("You Win!", font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()

game()
