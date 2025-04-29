from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent
from sympy.logic.inference import satisfiable
from sympy import simplify_logic


# Define propositional symbols
p, q, r = symbols("p q r")

# Define a belief base (a set of formulas)
belief_base = [p, Implies(p, q), q | p, And(p, q)]

print("Belief Base:", belief_base)


def is_consistent(beliefs):
    combined = And(*beliefs)
    return bool(satisfiable(combined))


print("Consistent?", is_consistent(belief_base))


def partial_meet_contraction(beliefs, p):
    from itertools import chain, combinations

    def all_subsets(s):
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

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
def equivalent(f1, f2):
    """Check semantic equivalence of two formulas."""
    return simplify_logic(f1) == simplify_logic(f2)


# Unit tests for AGM algorithm


def postulate_success(revise_fn, base, phi):
    revised = revise_fn(base, phi)
    return implies(revised, phi)


def postulate_inclusion(revise_fn, base, phi):
    revised = revise_fn(base, phi)
    expanded = base + [phi]
    return all(any(implies([b], r) for b in expanded) for r in revised)


def postulate_vacuity(revise_fn, base, phi):
    if implies(base, Not(phi)):
        return True  # not applicable
    revised = revise_fn(base, phi)
    expanded = base + [phi]
    return set(revised) == set(expanded)


def postulate_consistency(revise_fn, base, phi):
    revised = revise_fn(base, phi)
    return satisfiable(And(*revised)) != False


def postulate_extensionality(revise_fn, base, phi, psi):
    if not equivalent(phi, psi):
        return True  # not applicable
    return set(revise_fn(base, phi)) == set(revise_fn(base, psi))


# Implement code to test AGM postulates
