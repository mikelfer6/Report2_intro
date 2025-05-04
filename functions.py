"""Help functions for the Belief Base."""


def negate(literal):
    literal = literal.replace("\u00ac", "~")  # Support ¬ for NOT
    if literal.startswith("~"):
        return literal[1:]
    else:
        return "~" + literal


def convert_cnf(formula):
    formula = (
        formula.replace(" ", "")
        .replace("->", "=>")
        .replace("<->", "<=>")
        .replace("¬", "~")
    )

    if "<=>" in formula:
        parts = formula.split("<=>", 1)
        if len(parts) == 2:
            left, right = parts
            return [[negate(left), right], [left, negate(right)]]

    if "=>" in formula:
        parts = formula.split("=>", 1)
        if len(parts) == 2:
            left, right = parts
            return [[negate(left), right]]

    if formula.startswith("~(") and formula.endswith(")"):
        inner = formula[2:-1]
        if "&" in inner:
            parts = inner.split("&")
            return [[negate(part)] for part in parts]
        elif "|" in inner:
            parts = inner.split("|")
            return [[negate(part) for part in parts]]
        else:
            return [[negate(inner)]]

    if "&" in formula:
        parts = formula.split("&")
        return [[part] for part in parts]

    if "|" in formula:
        parts = formula.split("|")
        return [parts]

    return [[formula]]


def resolve(ci, cj):
    resolvents = []
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                new_clause = list(set(ci + cj))
                new_clause.remove(di)
                new_clause.remove(dj)
                resolvents.append(new_clause)
    return resolvents


def resolution(clauses):
    new = set()
    clauses = set(frozenset(clause) for clause in clauses)

    while True:
        pairs = [(ci, cj) for ci in clauses for cj in clauses if ci != cj]
        for ci, cj in pairs:
            resolvents = resolve(list(ci), list(cj))
            for resolvent in resolvents:
                if not resolvent:
                    return True
                new.add(frozenset(resolvent))
        if new.issubset(clauses):
            return False
        clauses.update(new)
