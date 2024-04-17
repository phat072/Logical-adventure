# DPLL SAT Solver

This project implements the Davis-Putnam-Logemann-Loveland (DPLL) algorithm, a complete, backtracking-based search algorithm for deciding the satisfiability of propositional logic formulae in conjunctive normal form (CNF-SAT problem).

## Features

- Parses DIMACS format files.
- Implements the Jeroslow-Wang heuristic for literal selection.
- Performs Boolean Constraint Propagation (BCP).
- Assigns units and simplifies the CNF.
- Backtracks when necessary.
- Runs benchmarks on a set of problems.

## Usage

You can run the SAT solver on a specific input file or on all files in the benchmarks folder.

To run the script on a specific input file, use the `--input_file` argument followed by the path to your file:

```bash
python Dpll_alg.py --input_file path_to_your_file
```

To run the script on all files in the benchmarks folder, use the `--run_benchmarks` flag:

```bash
python Dpll_alg.py --run_benchmarks
```

Replace `path_to_your_file` with the actual path to your input file.

## Dependencies

- Python
- argparse
- os
- time
- collections

## License

This project is licensed under the terms of the MIT license.
```

Please replace the license and dependencies as per your project's requirements.