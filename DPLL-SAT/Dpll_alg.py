import argparse
import os
import time
from collections import defaultdict


# Function to parse a DIMACS file
def parse_dimacs(filename):
    Clauses = []
    with open(filename, 'r') as input_file:
        for line in input_file:
            # Skip comment and problem lines
            if line[0] in ['c', 'p']:
                continue
            # Convert literals to integers and remove trailing zero
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            literals = literals[:-1]
            # Add clause to list of clauses
            Clauses.append(literals)
    return Clauses


# Function to implement the Jeroslow-Wang heuristic
def jersolow_wang_method(cnf):
    literal_weight = defaultdict(int)
    for clause in cnf:
        for literal in clause:
            # Increase weight of literal by 2^-length of clause
            literal_weight[literal] += 2 ** -len(clause)
    # Return literal with maximum weight
    return max(literal_weight, key=literal_weight.get)


# Function to implement the two-sided Jeroslow-Wang heuristic
def jersolow_wang_2_sided_method(cnf):
    literal_weight = defaultdict(int)
    for clause in cnf:
        for literal in clause:
            # Increase weight of absolute value of literal by 2^-length of clause
            literal_weight[abs(literal)] += 2 ** -len(clause)
    # Return literal with maximum weight
    return max(literal_weight, key=literal_weight.get)


# Function to perform Boolean Constraint Propagation (BCP)
def bcp(cnf, unit):
    new_cnf = []
    for clause in cnf:
        # Skip clauses that contain the unit
        if unit in clause:
            continue
        # Remove negated unit from clauses
        if -unit in clause:
            new_clause = [literal for literal in clause if literal != -unit]
            # If clause is empty, return -1
            if not new_clause:
                return -1
            new_cnf.append(new_clause)
        else:
            new_cnf.append(clause)
    return new_cnf


# Function to assign units
def assign_unit(cnf):
    I = []  # contains the bool assignments for each variable
    unit_clauses = [clause for clause in cnf if len(clause) == 1]
    while unit_clauses:
        unit = unit_clauses[0][0]
        cnf = bcp(cnf, unit)  # assign true to unit
        I += [unit]
        if cnf == -1:
            return -1, []
        # base case: empty conjunct so it is SAT
        if not cnf:
            return cnf, I
        unit_clauses = [clause for clause in cnf if len(clause) == 1]  # update
    return cnf, I


# DPLL algorithm
def backtrack(cnf, I):
    cnf, unit_I = assign_unit(cnf)
    I = I + unit_I
    if cnf == -1:
        return []
    if not cnf:
        return I
    selected_literal = jersolow_wang_2_sided_method(cnf)
    res = backtrack(bcp(cnf, selected_literal), I + [selected_literal])
    # if no solution when assigning to True, try to assign to False
    if not res:
        res = backtrack(bcp(cnf, -selected_literal), I + [-selected_literal])
    return res


# Function to run benchmarks
def run_benchmarks(Fname):
    print('Running on benchmarks...')
    start_time = time.time()
    with open(Fname, 'w') as out_file:
        for filename in os.listdir("benchmarks"):
            Clauses = parse_dimacs(os.path.join("benchmarks", filename))
            Assignment = backtrack(Clauses, [])
            if Assignment:
                out_file.write('SAT')
            else:
                out_file.write('UNSAT')
            out_file.write('\n')
    end_time = time.time()
    print('Execution time: %.2f seconds' % (end_time - start_time))


# Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_benchmarks', action='store_true',
                        help='Run the sat solver over all files in the benchmarks folder')
    parser.add_argument('--input_file', default=None,
                        help='input file following DIMACS format (ignored if run_benchmarks is set to True')
    args = parser.parse_args()
    if args.run_benchmarks:
        run_benchmarks('benchmarks-results.log')
    elif args.input_file is not None:
        f = args.input_file
        assert os.path.exists(f), '{} does not exists'.format(f)
        clauses = parse_dimacs(f)
        assignment = backtrack(clauses, [])
        if assignment:
            print('SAT')
            assignment.sort(key=lambda x: abs(x))
            print(assignment)
        else:
            print('UNSAT')
    else:
        print('Please either choose an input file or run the benchmarks. Type --help for more details')
