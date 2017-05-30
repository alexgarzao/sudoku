# coding: utf-8

# Algoritmo para chegar a solução (sem tentativa e erro):
#
# Cria a matriz com os resultados (9x9)
# Cria a matriz onde vão ficar os possveis números (9x9x9)
# Baseado no input inicial, popula a matriz de possíveis números com os números conhecidos
# Ajusta a matriz de possibilidades conforme o input inicial
# Fica no laço abaixo:
#   Ajusta a matriz de possibilidades conforme os números conhecidos
#   Se em alguma posição só ficou uma possibilidade, está resolvido esta posição. Tenta novamente.
#   Se em alguma linha só falta um número, está resolvida esta posição. Tenta novamente.
#   Se em alguma coluna só falta um número, está resolvida esta posição. Tenta novamente.
#   Se em algum agrupamento só falta um número, está resolvida esta posição. Tenta novamente.
#   Se todos os números foram resolvidos, finish.
#   Se algo foi alterado nesta iteração, vai para o início do laço.
#   Se nada mudou nesta iteração, sudoku sem resposta com este algoritmo :-/


GRID_SIZE = 9


class Square(object):
    def __init__(self, i, j, number):
        self.i = i
        self.j = j
        self.define_number(number)

    def define_number(self, number):
        self.number = number
        self.__init_possibilities()

    def __init_possibilities(self):
        if self.number == 0:
            self.possibilities = {i for i in xrange(1, GRID_SIZE + 1)}
        else:
            self.possibilities = set()

    def remove_possibility(self, number):
        self.possibilities.discard(number)

    def solve_number_with_one_possibility(self):
        if self.number != 0:
            return False

        assert len(self.possibilities) != 0, '%d, %d with 0 !!!' % (self.i, self.j)

        if len(self.possibilities) == 1:
            self.number = self.possibilities.pop()
            return True

    def print_number(self):
        print self.number,

    def print_possibilities(self):
        if len(self.possibilities) == 0:
            print self.number,
        else:
            print '[',
            for possibility in self.possibilities:
                print possibility,
            print ']',


class Row(object):
    def __init__(self, grid, row):
        self.grid = grid
        self.row = row

    def element(self, index):
        return self.grid[self.row][index]

    def define_possibilities(self):
        found = False
        for c1 in xrange(GRID_SIZE):
            current_number = self.grid[self.row][c1]
            if current_number.number != 0:
                continue
            for c2 in xrange(GRID_SIZE):
                if c1 == c2:
                    continue
                other_number = self.grid[self.row][c2]
                if other_number.number == 0:
                    continue
                current_number.remove_possibility(other_number.number)
                found = True
        return found


class Col(object):
    def __init__(self, grid, col):
        self.grid = grid
        self.col = col

    def element(self, index):
        return self.grid[index][self.col]

    def define_possibilities(self):
        found = False
        for r1 in xrange(GRID_SIZE):
            current_number = self.grid[r1][self.col]
            if current_number.number != 0:
                continue
            for r2 in xrange(GRID_SIZE):
                if r1 == r2:
                    continue
                other_number = self.grid[r2][self.col]
                if other_number.number == 0:
                    continue
                current_number.remove_possibility(other_number.number)
                found = True
        return found


class Box(object):
    def __init__(self, grid, row, col):
        self.grid = grid
        self.row = row
        self.col = col
        self.elements = [
            (row + 0, col + 0), (row + 0, col + 1), (row + 0, col + 2),
            (row + 1, col + 0), (row + 1, col + 1), (row + 1, col + 2),
            (row + 2, col + 0), (row + 2, col + 1), (row + 2, col + 2)
        ]

    def print_numbers(self):
        print 'box: ',
        for i1 in xrange(9):
            e1 = self.elements[i1]
            current_number = self.grid[e1[0]][e1[1]]
            print current_number.i, current_number.j, current_number.number, '|',
        print

    def define_possibilities(self):
        found = False
        for i1 in xrange(9):
            e1 = self.elements[i1]
            current_number = self.grid[e1[0]][e1[1]]
            if current_number.number != 0:
                continue
            for i2 in xrange(9):
                if i1 == i2:
                    continue
                e2 = self.elements[i2]
                other_number = self.grid[e2[0]][e2[1]]
                if other_number.number == 0:
                    continue
                current_number.remove_possibility(other_number.number)
                found = True
        return found

    def define_numbers_with_one_location(self):
        # Verifica se um numero so tem uma possivel localizacao no bloco.
        # 6         7           [4, 5, 9]
        # [8, 9]    [4, 8, 9]   [4, 9]
        # 2         1           [3, 5]
        found = False
        possible_locations = {i: set() for i in xrange(1,10)}

        for i in xrange(9):
            e = self.elements[i]
            number = self.grid[e[0]][e[1]]
            if number.number != 0:
                continue
            for possibility in number.possibilities:
                possible_locations[possibility].add((number.i,number.j))

        for possibility in possible_locations:
            possible_location = possible_locations[possibility]
            if len(possible_location) == 1:
                location = possible_location.pop()
                self.grid[location[0]][location[1]].define_number(possibility)
                found = True

        return found


class Grid(object):
    def __init__(self, grid):
        self.grid = [[Square(i, j, grid[i][j]) for j in xrange(GRID_SIZE)] for i in xrange(GRID_SIZE)]
        self.rows = [Row(self.grid, i) for i in xrange(GRID_SIZE)]
        self.cols = [Col(self.grid, i) for i in xrange(GRID_SIZE)]
        self.boxs = [
            Box(self.grid, 0, 0), Box(self.grid, 0, 3), Box(self.grid, 0, 6),
            Box(self.grid, 3, 0), Box(self.grid, 3, 3), Box(self.grid, 3, 6),
            Box(self.grid, 6, 0), Box(self.grid, 6, 3), Box(self.grid, 6, 6)
        ]
        for box in self.boxs:
            print 'box: ',
            box.print_numbers()
        self.count = 0

    def define_possibilities(self):
        while True:
            found = False
            for row in self.rows:
                if row.define_possibilities():
                    found = True
            for col in self.cols:
                if col.define_possibilities():
                    found = True
            for box in self.boxs:
                if box.define_possibilities():
                    found = True
                if box.define_numbers_with_one_location():
                    found = True
            break
        return found

    def solve_numbers_with_one_possibility(self):
        solved = False
        for r in xrange(GRID_SIZE):
            for c in xrange(GRID_SIZE):
                number = self.grid[r][c]
                if number.solve_number_with_one_possibility():
                    self.count += 1
                    solved = True

    def print_numbers(self):
        print 'Numbers'
        for r in xrange(GRID_SIZE):
            print 'Linha: %s\t' % str(r + 1),
            for c in xrange(GRID_SIZE):
                number = self.grid[r][c]
                number.print_number()
                print (' '),
            print ('')

    def print_possibilities(self):
        print 'Possibilities'
        for r in xrange(GRID_SIZE):
            print 'Linha: %s\t' % str(r + 1),
            for c in xrange(GRID_SIZE):
                number = self.grid[r][c]
                number.print_possibilities()
            print ('')


class SudokuSolver(object):
    def __init__(self, grid):
        self.grid = Grid(grid)

        print 'Original'
        self.grid.print_numbers()
        self.grid.define_possibilities()
        self.grid.print_possibilities()

    def run(self):
        grid = self.grid

        for i in xrange(50):
            print '\nRodada %d' % i
            grid.define_possibilities()
            while grid.solve_numbers_with_one_possibility():
                pass
            grid.print_numbers()
            grid.print_possibilities()
            print 'partial count=', grid.count

        print 'total count: ', grid.count

def sample_easy_11():
    grid = []
    grid.append([0, 3, 9, 0, 6, 0, 2, 1, 0])
    grid.append([5, 0, 0, 0, 2, 0, 0, 0, 8])
    grid.append([7, 0, 8, 0, 0, 0, 4, 0, 9])
    grid.append([0, 0, 9, 0, 5, 0, 0, 0, 0])
    grid.append([9, 8, 0, 0, 0, 0, 0, 5, 4])
    grid.append([0, 0, 0, 6, 0, 8, 0, 0, 0])
    grid.append([8, 0, 4, 0, 0, 0, 5, 0, 7])
    grid.append([3, 0, 0, 0, 9, 0, 0, 0, 1])
    grid.append([0, 1, 7, 0, 8, 0, 3, 9, 0])
    return grid


def test_1():
    grid = []
    grid.append([7, 9, 0, 0, 0, 0, 3, 0, 0])
    grid.append([0, 0, 0, 0, 0, 6, 9, 0, 0])
    grid.append([8, 0, 0, 0, 3, 0, 0, 7, 6])
    grid.append([0, 0, 0, 0, 0, 5, 0, 0, 2])
    grid.append([0, 0, 5, 4, 1, 8, 7, 0, 0])
    grid.append([4, 0, 0, 7, 0, 0, 0, 0, 0])
    grid.append([6, 1, 0, 0, 9, 0, 0, 0, 8])
    grid.append([0, 0, 2, 3, 0, 0, 0, 0, 0])
    grid.append([0, 0, 9, 0, 0, 0, 0, 5, 4])
    return grid


# Peguei deste site: http://www.247sudoku.com/sudokuEasy.php
def test_2():
    grid = []
    grid.append([0, 0, 0, 0, 0, 1, 9, 0, 0])
    grid.append([0, 0, 7, 5, 3, 0, 0, 6, 0])
    grid.append([5, 0, 0, 0, 0, 6, 1, 3, 2])
    grid.append([1, 0, 0, 0, 4, 7, 0, 8, 3])
    grid.append([0, 7, 0, 0, 0, 0, 0, 9, 0])
    grid.append([2, 5, 0, 8, 9, 0, 0, 0, 7])
    grid.append([6, 8, 9, 3, 0, 0, 0, 0, 1])
    grid.append([0, 3, 0, 0, 1, 9, 8, 0, 0])
    grid.append([0, 0, 1, 6, 0, 0, 0, 0, 0])

    # Expected result:
    # Linha: 1	3   6   2   4   8   1   9   7   5
    # Linha: 2	9   1   7   5   3   2   4   6   8
    # Linha: 3	5   4   8   9   7   6   1   3   2
    # Linha: 4	1   9   6   2   4   7   5   8   3
    # Linha: 5	8   7   3   1   6   5   2   9   4
    # Linha: 6	2   5   4   8   9   3   6   1   7
    # Linha: 7	6   8   9   3   2   4   7   5   1
    # Linha: 8	4   3   5   7   1   9   8   2   6
    # Linha: 9	7   2   1   6   5   8   3   4   9
    return grid


# Peguei deste site: http://www.247sudoku.com/sudokuEasy.php
def test_3():
    grid = []
    grid.append([5, 0, 0, 0, 4, 0, 6, 9, 7])
    grid.append([8, 0, 0, 0, 0, 2, 0, 4, 0])
    grid.append([0, 0, 9, 5, 0, 3, 1, 0, 8])
    grid.append([0, 0, 1, 4, 3, 0, 0, 7, 0])
    grid.append([0, 0, 0, 7, 0, 9, 0, 0, 0])
    grid.append([0, 7, 0, 0, 6, 5, 4, 0, 0])
    grid.append([1, 0, 3, 2, 0, 4, 7, 0, 0])
    grid.append([0, 2, 0, 9, 0, 0, 0, 0, 4])
    grid.append([6, 9, 4, 0, 1, 0, 0, 0, 5])

    # Expected result:
    # Linha: 1	5   3   2   8   4   1   6   9   7
    # Linha: 2	8   1   7   6   9   2   5   4   3
    # Linha: 3	4   6   9   5   7   3   1   2   8
    # Linha: 4	2   5   1   4   3   8   9   7   6
    # Linha: 5	3   4   6   7   2   9   8   5   1
    # Linha: 6	9   7   8   1   6   5   4   3   2
    # Linha: 7	1   8   3   2   5   4   7   6   9
    # Linha: 8	7   2   5   9   8   6   3   1   4
    # Linha: 9	6   9   4   3   1   7   2   8   5
    return grid


# Peguei deste site: http://www.247sudoku.com/sudokuMedium.php
def test_4():
    grid = []
    grid.append([0, 2, 4, 3, 8, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 0, 6, 0, 0, 7])
    grid.append([0, 5, 8, 0, 0, 0, 4, 0, 0])
    grid.append([4, 0, 0, 0, 1, 0, 0, 0, 0])
    grid.append([0, 0, 0, 7, 0, 5, 0, 0, 0])
    grid.append([0, 0, 0, 0, 2, 0, 0, 0, 8])
    grid.append([0, 0, 1, 0, 0, 0, 6, 7, 0])
    grid.append([3, 0, 0, 5, 0, 0, 0, 0, 0])
    grid.append([0, 0, 0, 0, 4, 9, 2, 1, 0])

    # Expected result:
    # Linha: 1	6 2 4 3 8 7 5 9 1
    # Linha: 2	1 3 9 4 5 6 8 2 7
    # Linha: 3	7 5 8 1 9 2 4 3 6
    # Linha: 4	4 9 6 8 1 3 7 5 2
    # Linha: 5	2 8 3 7 6 5 1 4 9
    # Linha: 6	5 1 7 9 2 4 3 6 8
    # Linha: 7	9 4 1 2 3 8 6 7 5
    # Linha: 8	3 6 2 5 7 1 9 8 4
    # Linha: 9	8 7 5 6 4 9 2 1 3
    return grid


# Peguei deste site: http://www.247sudoku.com/sudokuHard.php
def test_5():
    grid = []
    grid.append([3, 0, 0, 5, 0, 0, 0, 0, 0])
    grid.append([4, 0, 9, 0, 0, 0, 6, 0, 0])
    grid.append([7, 0, 0, 4, 0, 3, 0, 0, 9])
    grid.append([0, 0, 0, 0, 0, 0, 8, 4, 0])
    grid.append([6, 0, 0, 0, 0, 0, 0, 0, 5])
    grid.append([0, 7, 1, 0, 0, 0, 0, 0, 0])
    grid.append([2, 0, 0, 6, 0, 9, 0, 0, 8])
    grid.append([0, 0, 4, 0, 0, 0, 5, 0, 7])
    grid.append([0, 0, 0, 0, 0, 8, 0, 0, 3])

    # Expected result:
    # Linha: 1	3 1 2 5 9 6 7 8 4
    # Linha: 2	4 5 9 2 8 7 6 3 1
    # Linha: 3	7 8 6 4 1 3 2 5 9
    # Linha: 4	9 2 3 1 7 5 8 4 6
    # Linha: 5	6 4 8 9 3 2 1 7 5
    # Linha: 6	5 7 1 8 6 4 3 9 2
    # Linha: 7	2 3 7 6 5 9 4 1 8
    # Linha: 8	8 9 4 3 2 1 5 6 7
    # Linha: 9	1 6 5 7 4 8 9 2 3
    return grid


if __name__ == '__main__':
    solver = SudokuSolver(test_5())
    solver.run()
