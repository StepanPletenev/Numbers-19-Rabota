import pygame
import random
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Чиселки"
WINDOW_BACKGROUND_COLOR = (255, 255, 255)

NUMBERS_FONT_SIZE = 48
NUMBERS_COLOR = (0, 0, 0)
NUMBERS_PADDING = 20

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

numbers_font = pygame.font.SysFont("Arial", NUMBERS_FONT_SIZE)

numbers = list(range(1, 10))
random.shuffle(numbers)

game_over = False
current_number = 1

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if numbers[0] == current_number:
                current_number += 1
                numbers.pop(0)

                if len(numbers) == 0:
                    game_over = True
            else:
                game_over = True

    window.fill(WINDOW_BACKGROUND_COLOR)

    for i, number in enumerate(numbers):
        x = (WINDOW_WIDTH - (NUMBERS_FONT_SIZE + NUMBERS_PADDING) * 3) / 2 + i % 3 * (NUMBERS_FONT_SIZE + NUMBERS_PADDING)
        y = (WINDOW_HEIGHT - (NUMBERS_FONT_SIZE + NUMBERS_PADDING) * 3) / 2 + i // 3 * (NUMBERS_FONT_SIZE + NUMBERS_PADDING)

        number_text = numbers_font.render(str(number), True, NUMBERS_COLOR)
        window.blit(number_text, (x, y))

    pygame.display.update()

pygame.quit()
