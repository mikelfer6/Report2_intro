import itertools
import copy


class BeliefBase:
    def __init__(self):
        """Initialize an empty belief base with a list to hold (priority, formula) tuples."""
        self.beliefs = []

    def add_belief(self, formula, priority=0):
        """Add a belief with an associated priority to the belief base."""
        self.beliefs.append((priority, formula))
        self.beliefs.sort(reverse=True)

    def remove_belief(self, formula):
        """Remove a specific belief from the belief base."""
        self.beliefs = [(p, f) for (p, f) in self.beliefs if f != formula]

    def get_formulas(self):
        """Return a list of all belief formulas in the belief base."""
        return [f for (_, f) in self.beliefs]

    def entails(self, query):
        """Check if the belief base entails a given query using resolution."""
        clauses = [self.to_cnf(formula) for formula in self.get_formulas()]
        query_cnf = self.to_cnf(f"~({query})")
        all_clauses = list(itertools.chain(*clauses)) + query_cnf
        return self.resolution(all_clauses)

    def expand(self, formula):
        """Expand the belief base by adding a new belief."""
        self.add_belief(formula)

    def contract(self, formula):
        """Contract the belief base by removing beliefs to no longer entail the given formula."""
        if self.entails(formula):
            for priority, belief in sorted(self.beliefs, key=lambda x: -x[0]):
                temp_beliefs = copy.deepcopy(self)
                temp_beliefs.remove_belief(belief)
                if not temp_beliefs.entails(formula):
                    self.remove_belief(belief)
                    break

    def to_cnf(self, formula):
        """Convert a formula to a naive conjunctive normal form (CNF)."""
        formula = formula.replace("=>", ")|(").replace("<=>", ")=(")
        formula = formula.replace(" ", "")
        literals = formula.replace("(", "").replace(")", "").split("|")
        return [[lit] for lit in literals]

    def resolve(self, ci, cj):
        """Resolve two clauses and return the resulting resolvents."""
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == self.negate(dj):
                    new_clause = list(set(ci + cj))
                    new_clause.remove(di)
                    new_clause.remove(dj)
                    resolvents.append(new_clause)
        return resolvents

    def resolution(self, clauses):
        """Apply the resolution algorithm to check satisfiability of clauses."""
        new = set()
        clauses = [frozenset(clause) for clause in clauses]

        while True:
            pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]
            for ci, cj in pairs:
                resolvents = self.resolve(list(ci), list(cj))
                for resolvent in resolvents:
                    if not resolvent:
                        return True
                    new.add(frozenset(resolvent))
            if new.issubset(clauses):
                return False
            clauses.update(new)

    def negate(self, literal):
        """Negate a literal (add or remove the negation symbol)."""
        if literal.startswith("~"):
            return literal[1:]
        else:
            return "~" + literal


if __name__ == "__main__":
    bb = BeliefBase()

    # Initial beliefs
    bb.expand("A")
    bb.expand("A => B")

    print("Beliefs:", bb.get_formulas())

    print("Entails B?", bb.entails("B"))

    # Contract B
    bb.contract("B")

    print("Beliefs after contracting B:", bb.get_formulas())
    print("Entails B now?", bb.entails("B"))
