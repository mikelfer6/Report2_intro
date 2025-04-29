from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent
from sympy.logic.inference import satisfiable


# Define propositional symbols
p, q, r = symbols('p q r')

# Define a belief base (a set of formulas)
belief_base = [
    p,
    Implies(p, q),
    q | p ,
    And(p, q)
]

print("Belief Base:", belief_base)


def is_consistent(beliefs):
    combined = And(*beliefs)
    return bool(satisfiable(combined))

print("Consistent?", is_consistent(belief_base))


def partial_meet_contraction(beliefs, p):
    from itertools import chain, combinations

    def all_subsets(s):
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    maximal_subsets = []

    for subset in all_subsets(beliefs):
        subset = list(subset)
        # If subset does NOT imply p
        if not implies(subset, p):
            # Check maximality: no superset of subset (with one more belief) also does NOT imply p
            is_maximal = True
            for belief in beliefs:
                if belief not in subset:
                    extended = subset + [belief]
                    if not implies(extended, p):
                        is_maximal = False
                        break
            if is_maximal:
                maximal_subsets.append(subset)
    return maximal_subsets

def implies(beliefs, formula):
    combined = And(*beliefs)
    return not satisfiable(And(combined, Not(formula)))

reduced_sets = partial_meet_contraction(belief_base, p)

for s in reduced_sets:
    print("Subset:", s)


#########################
# Unit tests for AGM algorithm


