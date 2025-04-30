import itertools
import copy

class FormulaTransformer:
    @staticmethod
    def negate(literal):
        literal = literal.replace("\u00ac", "~")  # Support ¬ for NOT
        if literal.startswith('~'):
            return literal[1:]
        else:
            return '~' + literal

    @staticmethod
    def to_cnf(formula):
        formula = formula.replace(" ", "")
        formula = formula.replace("->", "=>").replace("<->", "<=>").replace("\u00ac", "~")

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
        if formula not in self.get_formulas():
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
        else:
            print(f"Belief '{formula}' was not added because it contradicts current beliefs.")

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
        print("\nTesting all AGM Postulates for:", formula)

        # Use a copy to avoid modifying the actual belief base
        test_base = copy.deepcopy(self)

        test_base.expand(formula)
        print("1. Success:", test_base.entails(formula))

        original_formulas = set(self.get_formulas())
        updated_formulas = set(test_base.get_formulas())
        print("2. Inclusion:", original_formulas.issubset(updated_formulas))

        before = set(test_base.get_formulas())
        test_base.expand(formula)
        after = set(test_base.get_formulas())
        print("3. Vacuity:", before == after)

        print("4. Consistency:", not test_base.entails("False"))

        formula_negated_negated = FormulaTransformer.negate(FormulaTransformer.negate(formula))
        ext_base = copy.deepcopy(self)
        ext_base.expand(formula_negated_negated)
        print("5. Extensionality:", set(test_base.get_formulas()) == set(ext_base.get_formulas()))

if __name__ == "__main__":
    bb = BeliefBase()

    while True:
        print("\nBELIEF BASE MENU")
        print("1. Add a belief")
        print("2. Remove a belief")
        print("3. Show belief base")
        print("4. Contract a belief")
        print("5. Revise a belief")
        print("6. Check entailment")
        print("7. Test AGM postulates")
        print("0. Exit")

        choice = input("Choose an option: ")
        show_after = True

        if choice == "1":
            print("Add a belief to the base. Example: A, A->B, A<->B, A&B, A|B, ¬A")
            belief = input("Enter the belief to add: ")
            bb.expand(belief)

        elif choice == "2":
            print("Remove a belief by typing it exactly as it appears in the base.")
            belief = input("Enter the belief to remove: ")
            bb.remove_belief(belief)

        elif choice == "3":
            print("Current belief base:")
            print(bb.get_formulas())
            show_after = False  # Don't show again after display

        elif choice == "4":
            print("Contract the belief base to stop entailing a formula.")
            belief = input("Enter the belief to contract: ")
            bb.contract(belief)

        elif choice == "5":
            print("Revise the belief base by a new belief (Levi identity).")
            belief = input("Enter the belief to revise with: ")
            bb.revise(belief)

        elif choice == "6":
            print("Check if a query is logically entailed by the belief base.")
            query = input("Enter the query to check entailment: ")
            print("Entails", query, "?", bb.entails(query))

        elif choice == "7":
            print("Tests all AGM postulates (Success, Inclusion, Vacuity, Consistency, Extensionality).")
            belief = input("Enter the belief to test AGM postulates on (or type 'all' to test every belief): ")
            if belief.lower() == "all":
                for f in bb.get_formulas():
                    bb.agm_postulates_test(f)
            else:
                bb.agm_postulates_test(belief)

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid option. Try again.")
            show_after = False

        if show_after:
            print("\nUpdated belief base:")
            print(bb.get_formulas())
0