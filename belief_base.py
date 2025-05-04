import itertools
import copy
from functions import *

"""Belief Base Class"""


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
        clauses = [convert_cnf(formula) for formula in self.get_formulas()]
        query_cnf = convert_cnf(f"~({query})")
        all_clauses = list(itertools.chain(*clauses)) + query_cnf
        return resolution(all_clauses)

    def is_consistent(self):
        return not self.entails("False")

    def expand(self, formula, priority=0):
        if formula in self.get_formulas():
            return

        self.add_belief(formula, priority)

        if not self.is_consistent():
            print(f"Warning: belief base is now inconsistent after adding '{formula}'.")

    def contract(self, formula):
        if self.entails(formula):
            for priority, belief in sorted(self.beliefs, key=lambda x: -x[0]):
                temp_beliefs = copy.deepcopy(self)
                temp_beliefs.remove_belief(belief)
                if not temp_beliefs.entails(formula):
                    self.remove_belief(belief)
                    break

    def revise(self, formula):
        self.contract(negate(formula))
        self.expand(formula)

    def agm_postulates_test(self, formula):
        print("\nTesting all AGM Postulates for:", formula)
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
        formula_negated_negated = negate(negate(formula))
        ext_base = copy.deepcopy(self)
        ext_base.expand(formula_negated_negated)
        print(
            "5. Extensionality:",
            set(test_base.get_formulas()) == set(ext_base.get_formulas()),
        )

    def auto_fix(self):
        if self.is_consistent():
            print("Belief base is already consistent.")
            return

        print("Inconsistency detected. Attempting to fix...")
        for priority, belief in sorted(self.beliefs, key=lambda x: x[0]):
            print(f"Trying to remove: {belief} (priority {priority})")
            temp = copy.deepcopy(self)
            temp.remove_belief(belief)
            if temp.is_consistent():
                self.remove_belief(belief)
                print(f"Removed belief '{belief}' to restore consistency.")
                return self.auto_fix()

        print(
            "Failed to restore consistency automatically. Manual review may be required."
        )
