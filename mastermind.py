import itertools
from belief_base import BeliefBase
from functions import negate


class LogicalMastermindAI:
    def __init__(self, code_length=4, colors="rgbyop"):
        self.code_length = code_length
        self.colors = colors
        self.belief_base = BeliefBase()
        self.all_codes = list(itertools.product(colors, repeat=code_length))
        self.known_valid_codes = self.all_codes.copy()

    def feedback(self, guess, code):
        black = sum(g == c for g, c in zip(guess, code))
        white = sum(min(guess.count(n), code.count(n)) for n in set(guess)) - black
        return black, white

    def encode_feedback_as_belief(self, guess, feedback):
        black, white = feedback
        high = 10  # Very strong belief
        medium = 5  # Less certain (disjunctive or partial)

        if black == 0 and white == 0:
            for color in guess:
                for pos in range(1, self.code_length + 1):
                    clause = f"~p{pos}{color}"
                    self.belief_base.expand(clause, priority=high)
        else:
            for pos, color in enumerate(guess):
                var = f"p{pos+1}{color}"
                if black == 0:
                    self.belief_base.expand(negate(var), priority=medium)

            for color in set(guess):
                if (black + white) > 0:
                    or_clause = []
                    for pos in range(1, self.code_length + 1):
                        or_clause.append(f"p{pos}{color}")

                    if or_clause:
                        clause = "|".join(or_clause)
                        self.belief_base.expand(clause, priority=medium)

        if not self.belief_base.is_consistent():
            self.belief_base.auto_fix()

    def consistent_with_beliefs(self, code):
        for pos, color in enumerate(code):
            var = f"p{pos+1}{color}"
            if not self.belief_base.entails(var) and self.belief_base.entails(
                negate(var)
            ):
                return False
        return True

    def update_knowledge(self, guess, feedback):
        self.encode_feedback_as_belief(guess, feedback)
        self.known_valid_codes = [
            c
            for c in self.known_valid_codes
            if self.feedback(guess, c) == feedback and self.consistent_with_beliefs(c)
        ]

    def make_guess(self):
        for code in self.known_valid_codes:
            if self.consistent_with_beliefs(code):
                return code
        return None
    
    def compute_feedback(self, secret, guess):
        """Compute feedback in (black, white) format."""
        return self.feedback(guess, secret)

    def receive_feedback(self, guess, feedback):
        """Update belief base and filter codes after receiving feedback."""
        self.update_knowledge(guess, feedback)

    def generate_all_codes(self, colors, length):
        """Generate all color combinations as tuples of strings."""
        return list(itertools.product(map(str, colors), repeat=length))

    @property
    def belief_base_size(self):
        """Return the current number of consistent valid codes."""
        return len(self.known_valid_codes)
