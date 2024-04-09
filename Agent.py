class Agent:
    def __init__(self):
        self.__agentLoc = []  # location,                  format: [row, col]
        self.__unknown = []  # frontier cells, unknown,   format: 'row_col'
        self.__safe = []  # frontier cells, safe,      format: 'row_col'
        self.__visited = []  # visited cells,             format: 'row_col'
        self.__foundExit = False
        self.__isAlive = True
        self.__point = 0
        self.__isEscaping = False

    def __str__(self):
        pass

    @property
    def agentLoc(self):
        return self.__agentLoc

    @agentLoc.setter
    def agentLoc(self, agentLoc: list):
        self.__agentLoc = agentLoc

