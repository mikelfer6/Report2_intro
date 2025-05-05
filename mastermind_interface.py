import pygame
import sys
import time

# --- Visual Settings ---
WIDTH, HEIGHT = 600, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

COLOR_MAPPING = {
    "r": RED,
    "g": GREEN,
    "b": BLUE,
    "y": YELLOW,
    "o": ORANGE,
    "p": PURPLE
}

CODE_LENGTH = 4


def draw_guess(screen, font, guess, feedback, y_pos):
    """Draw a single guess with feedback."""
    for idx in range(CODE_LENGTH):
        pygame.draw.circle(screen, GRAY, (50 + idx * 70, y_pos), 30, 3)
        if idx < len(guess):
            pygame.draw.circle(screen, COLOR_MAPPING[guess[idx]], (50 + idx * 70, y_pos), 25)
    fb_text = font.render(f"Black: {feedback[0]}  White: {feedback[1]}", True, BLACK)
    screen.blit(fb_text, (400, y_pos - 15))


def draw_final_secret_code(screen, font, code):
    """Draw the secret code at the bottom with the same style as guesses."""
    y_pos = 670
    label = font.render("Secret Code:", True, BLACK)
    screen.blit(label, (20, y_pos - 50))
    for idx, color in enumerate(code):
        pygame.draw.circle(screen, GRAY, (50 + idx * 70, y_pos), 30, 3)
        pygame.draw.circle(screen, COLOR_MAPPING[color], (50 + idx * 70, y_pos), 25)


def draw_turn_counter(screen, font, turn):
    """Draw current turn number at bottom right."""
    turn_text = font.render(f"Turn: {turn}", True, BLACK)
    screen.blit(turn_text, (WIDTH - 120, HEIGHT - 70))


def mastermind_visualizer(secret_code, history):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mastermind Belief Revision Visualizer")
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()

    running = True
    index = 0
    last_update_time = time.time()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw guesses so far
        for i in range(index):
            guess, feedback = history[i]
            draw_guess(screen, font, guess, feedback, 70 + i * 70)

        # Draw secret code at the bottom
        draw_final_secret_code(screen, font, secret_code)

        # Draw current turn number
        draw_turn_counter(screen, font, index + 1)

        pygame.display.update()

        if index < len(history) and time.time() - last_update_time > 3:
            index += 1
            last_update_time = time.time()

        clock.tick(60)
