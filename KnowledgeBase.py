from Dpll import *


def solve(self, Assignment, allowBranching=False):
    """
    Solve the knowledge base using DPLL algorithm or unit propagation based on the allowBranching flag.

    Parameters:
    Assignment (dict): A dictionary representing the current assignment of variables.
    allowBranching (bool, optional): A flag indicating whether to use DPLL algorithm or unit propagation. Defaults to False.

    Returns:
    dict: The final assignment of variables.
    """
    if allowBranching:
        Result, Assignment = dpll(self.clauses)
    else:
        Result, Assignment = unitPropagation(self.clauses, {})
    return Assignment


def addClause(self, clause, source):
    """
    Add a clause to the knowledge base.

    Parameters:
    clause (list): A list representing a clause to be added.
    source (str): The source of the clause.
    """
    self.sources.append(source)
    self.clauses.append(clause)


def remove(self, source):
    """
    Remove a clause from the knowledge base.

    Parameters:
    source (str): The source of the clause to be removed.
    """
    for i, s in enumerate(self.sources):
        if s == source:
            self.sources.pop(i)
            self.clauses.pop(i)
            break


def findLiteral(self, literal):
    """
    Find a literal in the knowledge base.

    Parameters:
    literal (str): The literal to be found.

    Returns:
    bool: True if the literal is found, False otherwise.
    """
    for clause in self.clauses:
        if literal in clause:
            return True
    return False


class KnowledgeBase:
    """A class representing a knowledge base for a logic system."""

    def __init__(self):
        self.__clauses = []
        self.__sources = []

    solve = solve
    addClause = addClause
    remove = remove
    findLiteral = findLiteral

    @property
    def clauses(self):
        """
        Get the clauses of the knowledge base.

        Returns:
        list: The clauses of the knowledge base.
        """
        return self.__clauses

    @property
    def sources(self):
        """
        Get the sources of the clauses in the knowledge base.

        Returns:
        list: The sources of the clauses in the knowledge base.
        """
        return self.__sources