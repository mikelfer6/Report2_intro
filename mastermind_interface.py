import pygame
import sys
import random
import time
from Belief_revision import MastermindBeliefAgent  # Your belief agent

# Pygame settings
WIDTH, HEIGHT = 600, 750  # Reduced height
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind Belief Revision Visualizer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# Game settings
COLORS = [1, 2, 3, 4, 5, 6]  # Now using 6 colors
CODE_LENGTH = 4
COLOR_MAPPING = {
    1: RED,
    2: BLUE,
    3: YELLOW,
    4: GREEN,
    5: PURPLE,
    6: ORANGE
}

# --- Helper functions ---

def draw_guess(guess, feedback, y_pos):
    """Draw a guess and its feedback at a given position."""
    for idx in range(CODE_LENGTH):
        pygame.draw.circle(screen, GRAY, (50 + idx * 70, y_pos), 20, 3)  # Smaller outer circle
        if idx < len(guess):
            pygame.draw.circle(screen, COLOR_MAPPING[guess[idx]], (50 + idx * 70, y_pos), 15)  # Smaller colored peg
    feedback_text = font.render(f"Black: {feedback[0]}  White: {feedback[1]}", True, BLACK)
    screen.blit(feedback_text, (400, y_pos - 10))

def display_belief_base_size(agent, initial_size):
    """Display the number of possible codes left."""
    init_text = font.render(f"Initial: {initial_size}", True, BLACK)
    screen.blit(init_text, (300, 660))
    size_text = font.render(f"Belief Base Size: {len(agent.belief_base)}", True, BLACK)
    screen.blit(size_text, (20, 660))

def draw_secret_code(secret_code, won):
    """Draw the secret code or a winning message at the bottom."""
    y_pos = 700
    if won:
        label = font.render("Congratulations! You cracked the code!", True, GREEN)
        screen.blit(label, (20, y_pos))
    else:
        label = font.render("Secret Code:", True, BLACK)
        screen.blit(label, (20, y_pos - 10))
        for idx in range(CODE_LENGTH):
            pygame.draw.circle(screen, GRAY, (50 + idx * 70, y_pos + 30), 20, 3)
            pygame.draw.circle(screen, COLOR_MAPPING[secret_code[idx]], (50 + idx * 70, y_pos + 30), 15)

# --- Main visualizer ---

def mastermind_visualizer(secret_code):
    initial_size = len(MastermindBeliefAgent().all_codes)
    agent = MastermindBeliefAgent()
    moves = []
    running = True
    won = False

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if len(moves) == 0 or moves[-1][1] != (CODE_LENGTH, 0):
            guess = agent.make_guess()
            feedback = agent.compute_feedback(secret_code, guess)
            moves.append((guess, feedback))
            agent.receive_feedback(guess, feedback)
        else:
            won = True

        # Draw all previous guesses
        for i, (guess, feedback) in enumerate(moves):
            draw_guess(guess, feedback, 100 + i * 80)

        display_belief_base_size(agent, initial_size)

        draw_secret_code(secret_code, won)

        pygame.display.update()

        time.sleep(2)
        clock.tick(1)

# --- Main Runner ---

if __name__ == "__main__":
    secret = random.choice(MastermindBeliefAgent().generate_all_codes(COLORS, CODE_LENGTH))
    print("Secret Code (hidden):", secret)
    mastermind_visualizer(secret)
