import itertools
import copy

class FormulaTransformer:
    @staticmethod
    def negate(literal):
        if literal.startswith('~'):
            return literal[1:]
        else:
            return '~' + literal

    @staticmethod
    def to_cnf(formula):
        formula = formula.replace(" ", "")

        if "=>" in formula:
            parts = formula.split("=>")
            left = parts[0]
            right = parts[1]
            return [[FormulaTransformer.negate(left), right]]

        if "<=>" in formula:
            parts = formula.split("<=>")
            left = parts[0]
            right = parts[1]
            return [[FormulaTransformer.negate(left), right], [left, FormulaTransformer.negate(right)]]

        if formula.startswith("~(") and formula.endswith(")"):
            inner = formula[2:-1]
            if "&" in inner:
                a, b = inner.split("&")
                return [[FormulaTransformer.negate(a)], [FormulaTransformer.negate(b)]]
            elif "|" in inner:
                a, b = inner.split("|")
                return [[FormulaTransformer.negate(a), FormulaTransformer.negate(b)]]
            else:
                return [[FormulaTransformer.negate(inner)]]

        if "&" in formula:
            literals = formula.split("&")
            return [[lit] for lit in literals]

        if "|" in formula:
            literals = formula.split("|")
            return [literals]

        return [[formula]]

class ResolutionChecker:
    @staticmethod
    def resolve(ci, cj):
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == FormulaTransformer.negate(dj):
                    new_clause = list(set(ci + cj))
                    new_clause.remove(di)
                    new_clause.remove(dj)
                    resolvents.append(new_clause)
        return resolvents

    @staticmethod
    def resolution(clauses):
        new = set()
        clauses = set(frozenset(clause) for clause in clauses)

        while True:
            pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]
            for (ci, cj) in pairs:
                resolvents = ResolutionChecker.resolve(list(ci), list(cj))
                for resolvent in resolvents:
                    if not resolvent:
                        return True
                    new.add(frozenset(resolvent))
            if new.issubset(clauses):
                return False
            clauses.update(new)

class BeliefBase:
    def __init__(self):
        self.beliefs = []

    def add_belief(self, formula, priority=0):
        self.beliefs.append((priority, formula))
        self.beliefs.sort(reverse=True)

    def remove_belief(self, formula):
        self.beliefs = [(p, f) for (p, f) in self.beliefs if f != formula]

    def get_formulas(self):
        return [f for (_, f) in self.beliefs]

    def entails(self, query):
        clauses = [FormulaTransformer.to_cnf(formula) for formula in self.get_formulas()]
        query_cnf = FormulaTransformer.to_cnf(f"~({query})")
        all_clauses = list(itertools.chain(*clauses)) + query_cnf
        return ResolutionChecker.resolution(all_clauses)

    def expand(self, formula):
        if not self.entails(FormulaTransformer.negate(formula)):
            self.add_belief(formula)

    def contract(self, formula):
        if self.entails(formula):
            for priority, belief in sorted(self.beliefs, key=lambda x: -x[0]):
                temp_beliefs = copy.deepcopy(self)
                temp_beliefs.remove_belief(belief)
                if not temp_beliefs.entails(formula):
                    self.remove_belief(belief)
                    break

    def revise(self, formula):
        self.contract(FormulaTransformer.negate(formula))
        self.expand(formula)

    def agm_postulates_test(self, formula):
        print("\nTesting AGM Postulates for:", formula)

        original_beliefs = copy.deepcopy(self)

        self.expand(formula)
        success = self.entails(formula)
        print("Success:", success)

        inclusion = set(original_beliefs.get_formulas()).issubset(set(self.get_formulas()))
        print("Inclusion:", inclusion)

        before = set(self.get_formulas())
        self.expand(formula)
        after = set(self.get_formulas())
        vacuity = before == after
        print("Vacuity:", vacuity)

        consistency = not self.entails("False")
        print("Consistency:", consistency)

        formula_negated_negated = FormulaTransformer.negate(FormulaTransformer.negate(formula))
        ext_base = copy.deepcopy(original_beliefs)
        ext_base.expand(formula_negated_negated)
        extensionality = set(self.get_formulas()) == set(ext_base.get_formulas())
        print("Extensionality:", extensionality)

if __name__ == "__main__":
    bb = BeliefBase()

    bb.expand("A")
    bb.expand("A=>B")

    print("Beliefs:", bb.get_formulas())
    print("Entails B?", bb.entails("B"))

    bb.contract("B")

    print("Beliefs after contracting B:", bb.get_formulas())
    print("Entails B now?", bb.entails("B"))

    bb.agm_postulates_test("C")
