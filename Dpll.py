def simplify_clause(clauses, assignment):
    simplifiedClauses = []
    for clause in clauses:
        simplifiedClause = []
        for literal in clause:
            variable = literal.replace('-', '')
            if assignment.get(variable) is None:
                simplifiedClause.append(literal)
        simplifiedClauses.append(simplifiedClause)
    return simplifiedClauses


def unitPropagation(clauses, assignment):
    unit_clauses = [clause[0] for clause in clauses if len(clause) == 1]
    while unit_clauses:
        literal = unit_clauses[0]
        variable = literal.replace('-', '')
        assignment[variable] = literal[0] != '-'
        clauses = [clause for clause in clauses if literal not in clause]
        clauses = simplify_clause(clauses, assignment)
        if any(len(clause) == 0 for clause in clauses):
            return "UNSAT", {}
        unit_clauses = [clause[0] for clause in clauses if len(clause) == 1]
    return clauses, assignment


def choose_literal(clauses):
    for clause in clauses:
        for literal in clause:
            return literal


def dpll(clauses, assignment={}):
    clauses, assignment = unitPropagation(clauses, assignment)
    if clauses == "UNSAT":
        return "UNSAT", {}
    if all(len(clause) == 0 for clause in clauses):
        return "SAT", assignment

    literal = choose_literal(clauses)
    variable = literal.replace('-', '')
    new_assignment = assignment.copy()
    new_assignment[variable] = True
    new_clauses = [clause for clause in clauses if literal not in clause]
    Result = dpll(simplify_clause(new_clauses, {variable: True}), new_assignment)
    if Result[0] == "SAT":
        return Result

    new_assignment = assignment.copy()
    new_assignment[variable] = False
    return dpll(simplify_clause(new_clauses, {variable: False}), new_assignment)


if __name__ == "__main__":
    clauses = [['1'], ['-1', '-3'], ['2', '3']]
    assignment = {}

    result, final_assignment = dpll(clauses, assignment)
    if result == "SAT":
        print("Satisfiable")
        print("Assignment:", final_assignment)
    else:
        print("Unsatisfiable")