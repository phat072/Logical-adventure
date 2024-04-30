from Dpll import *


def solve(self, Assignment, allowBranching=False):
    if allowBranching:
        Result, Assignment = dpll(self.clauses)
    else:
        Result, Assignment = unitPropagation(self.clauses, {})
    return Assignment


def addClause(self, clause, source):
    self.sources.append(source)
    self.clauses.append(clause)


def remove(self, source):
    for i, s in enumerate(self.sources):
        if s == source:
            self.sources.pop(i)
            self.clauses.pop(i)
            break


def findLiteral(self, literal):
    for clause in self.clauses:
        if literal in clause:
            return True
    return False


class KnowledgeBase:
    def __init__(self):
        self.__clauses = []
        self.__sources = []

    solve = solve
    addClause = addClause
    remove = remove
    findLiteral = findLiteral

    @property
    def clauses(self):
        return self.__clauses

    @property
    def sources(self):
        return self.__sources