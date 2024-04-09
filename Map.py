from turtle import update

R = [-1, 0, 1, 0]
C = [0, -1, 0, 1]


def updateInfo(self):
    n = self.size()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(4):
                if 'P' in self[i + R[k]][j + C[k]] and 'B' not in self[i][j]:
                    self[i][j] += 'B'
                if 'W' in self[i + R[k]][j + C[k]] and 'S' not in self[i][j]:
                    self[i][j] += 'S'


def INPUT(filePath):
    with open(filePath, 'r') as file:
        n = int(file.readline().splitlines()[0])
        MAP = [['' for i in range(n + 2)]]
        for i in range(n):
            line = '.' + file.readline().splitlines()[0] + '.'
            MAP.append(line.replace('-', '').split('.'))
        MAP.append(['' for i in range(n + 2)])

    MAP.reverse()

    agentLoc = [0, 0]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if 'A' in MAP[i][j]:
                agentLoc = [i, j]
                i = n + 1
                break

    MAP = Map(n, MAP)
    MAP.updateInfo()
    return Map(n, MAP), agentLoc


# map = input('tests/test1.txt')
# print(map)


class Map:
    def __init__(self, n=0, MAP=None):
        if MAP is None:
            MAP = []
        self.__size = n
        self.__map = MAP
        if n != 0 and MAP == []:
            MAP = [[[''] for c in range(n + 3)] for r in range(n + 3)]

    def __getitem__(self, row):
        return self.__map[row]

    def __setitem__(self, row, data):
        self.__map[row] = data

    def size(self):
        return self.__size

    updateInfo = updateInfo
    input = INPUT
