import pygame
import sys
import random
import time
from Belief_revision import MastermindBeliefAgent  # Your belief agent

# Pygame settings
WIDTH, HEIGHT = 600, 850
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind Belief Revision Visualizer")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)

# Game settings
COLORS = [1, 2, 3, 4]
CODE_LENGTH = 4
COLOR_MAPPING = {
    1: RED,
    2: BLUE,
    3: YELLOW,
    4: GREEN
}

# --- Helper functions ---

def draw_guess(guess, feedback, y_pos):
    """Draw a guess and its feedback at a given position."""
    for idx in range(CODE_LENGTH):
        pygame.draw.circle(screen, GRAY, (50 + idx * 70, y_pos), 30, 3)
        if idx < len(guess):
            pygame.draw.circle(screen, COLOR_MAPPING[guess[idx]], (50 + idx * 70, y_pos), 25)
    feedback_text = font.render(f"Black: {feedback[0]}  White: {feedback[1]}", True, BLACK)
    screen.blit(feedback_text, (400, y_pos - 15))

def display_belief_base_size(agent):
    """Display the number of possible codes left."""
    size_text = font.render(f"Belief Base Size: {len(agent.belief_base)}", True, BLACK)
    screen.blit(size_text, (20, 720))

def draw_final_winning_code(winning_guess):
    """Always draw the final winning code at the bottom, after it is found."""
    if winning_guess:
        y_pos = 780
        label = font.render("Winning Guess:", True, GREEN)
        screen.blit(label, (20, y_pos - 30))
        for idx in range(CODE_LENGTH):
            pygame.draw.circle(screen, GRAY, (50 + idx * 70, y_pos), 30, 3)
            pygame.draw.circle(screen, COLOR_MAPPING[winning_guess[idx]], (50 + idx * 70, y_pos), 25)

# --- Main visualizer ---

def mastermind_visualizer(secret_code):
    agent = MastermindBeliefAgent()
    moves = []
    winning_guess = None
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if len(moves) == 0 or (moves[-1][1] != (CODE_LENGTH, 0) and not winning_guess):
            guess = agent.make_guess()
            feedback = agent.compute_feedback(secret_code, guess)
            moves.append((guess, feedback))
            agent.receive_feedback(guess, feedback)

            if feedback == (CODE_LENGTH, 0):
                winning_guess = guess  # Save the winning guess!

        # Draw all previous guesses
        for i, (guess, feedback) in enumerate(moves):
            draw_guess(guess, feedback, 100 + i * 100)

        display_belief_base_size(agent)

        draw_final_winning_code()

        if winning_guess:
            draw_final_winning_code(winning_guess)

        pygame.display.update()
        
        time.sleep(5)
        clock.tick(1)

# --- Main Runner ---

if __name__ == "__main__":
    secret = random.choice(MastermindBeliefAgent().generate_all_codes(COLORS, CODE_LENGTH))
    print("Secret Code (hidden):", secret)
    mastermind_visualizer(secret)
