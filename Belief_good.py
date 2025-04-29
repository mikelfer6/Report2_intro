class Formula:
    """
    Represents a propositional logic formula as an Abstract Syntax Tree (AST).
    """
    def __init__(self, operator, operands=None):
        self.operator = operator  # 'AND', 'OR', 'NOT', 'IMPLIES', or variable like 'p'
        self.operands = operands if operands else []  # List of child Formula objects

    def __repr__(self):
        if not self.operands:
            return self.operator
        elif self.operator == 'NOT':
            return f"(NOT {self.operands[0]})"
        else:
            return f"({self.operands[0]} {self.operator} {self.operands[1]})"


class BeliefBase:
    """
    Represents a belief base: a list of independent beliefs (propositional formulas).
    """
    def __init__(self):
        self.beliefs = []  # List of Formula objects

    def add_belief(self, formula):
        """
        Expand the belief base with a new formula.
        :param formula: Formula object
        """
        self.beliefs.append(formula)

    def __repr__(self):
        return "Belief Base: [" + ", ".join(map(str, self.beliefs)) + "]"


# Example usage:
if __name__ == "__main__":
    # Let's manually build a formula: (p AND (NOT q))
    p = Formula('p')
    q = Formula('q')
    not_q = Formula('NOT', [q])
    formula = Formula('AND', [p, not_q])

    # Create a belief base
    bb = BeliefBase()

    # Add the formula to the belief base
    bb.add_belief(formula)

    # Print belief base
    print(bb)
