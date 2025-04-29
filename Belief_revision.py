import random
import sys
import pygame
import time

# Constants
COLORS = [1, 2, 3, 4, 5, 6]  # Updated to 6 colors
CODE_LENGTH = 4  # Code is 4 colors

# --- Belief Revision Engine for Mastermind ---

class MastermindBeliefAgent:
    def __init__(self):
        self.all_codes = self.generate_all_codes(COLORS, CODE_LENGTH)
        self.belief_base = self.all_codes.copy()
        self.history = []

    def generate_all_codes(self, colors, length):
        """Generate all possible combinations of codes."""
        if length == 0:
            return [[]]
        smaller = self.generate_all_codes(colors, length - 1)
        return [s + [c] for s in smaller for c in colors]

    def make_guess(self):
        """Pick a random guess from current belief base."""
        if not self.belief_base:
            print("Belief base empty! No possible codes left.")
            sys.exit()
        guess = random.choice(self.belief_base)
        self.history.append(("guess", guess))
        return guess

    def receive_feedback(self, guess, feedback):
        """Revise belief base: eliminate inconsistent codes."""
        revised = []
        for code in self.belief_base:
            if self.compute_feedback(code, guess) == feedback:
                revised.append(code)
        self.belief_base = revised
        self.history.append(("feedback", feedback))

    def compute_feedback(self, code, guess):
        """Compute Mastermind feedback (black pegs, white pegs)."""
        black = sum([1 for i in range(len(code)) if code[i] == guess[i]])
        # Count colors ignoring positions
        code_colors = {}
        guess_colors = {}
        for c in set(COLORS):
            code_colors[c] = code.count(c)
            guess_colors[c] = guess.count(c)
        total_common = sum(min(code_colors[c], guess_colors[c]) for c in COLORS)
        white = total_common - black
        return (black, white)

    def print_belief_base_size(self):
        print(f"Belief Base Size: {len(self.belief_base)} possible codes left.")

    def check_agm_postulates(self):
        """Very basic checks for Success, Consistency, etc."""
        # Success: last feedback must hold
        if not self.history:
            return
        last = self.history[-2:]
        if len(last) == 2 and last[0][0] == "guess" and last[1][0] == "feedback":
            guess = last[0][1]
            feedback = last[1][1]
            for code in self.belief_base:
                if self.compute_feedback(code, guess) != feedback:
                    print("Violation: Success Postulate Failed.")
                    break
        # Consistency
        if not self.belief_base:
            print("Warning: Belief Base became empty (inconsistent).")

# --- Simulating a Mastermind Game ---

def play_mastermind(secret_code):
    agent = MastermindBeliefAgent()
    moves = 0

    # Print belief base size at the beginning
    print("\n--- Initial Belief Base ---")
    agent.print_belief_base_size()

    while True:
        print("\n--- Turn", moves + 1, "---")
        guess = agent.make_guess()
        print("Guess:", guess)

        feedback = agent.compute_feedback(secret_code, guess)
        print("Feedback: (black, white) =", feedback)

        if feedback == (CODE_LENGTH, 0):
            print("Code broken! Secret code was:", secret_code)
            print("Total moves:", moves + 1)
            break

        agent.receive_feedback(guess, feedback)
        agent.print_belief_base_size()
        agent.check_agm_postulates()

        moves += 1


# --- Main ---

if __name__ == "__main__":
    # You can randomly generate a secret code
    secret = random.choice(MastermindBeliefAgent().generate_all_codes(COLORS, CODE_LENGTH))
    print("Secret Code (hidden):", secret)

    play_mastermind(secret)
