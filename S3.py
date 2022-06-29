# Sudoku Try 3

import numpy as np
import pickle
np.random.seed(1)

def read(num):
    with open(f'SBoard{num}.sav', 'rb') as file:
        g = pickle.load(file)
        return g


class Cell:
    def __init__(self, num=0):
        if num != 0:
            self.num = num
            self.poss = [num]
        else:
            self.num = num
            self.poss = [i for i in range(1, 10)]

    def __add__(self, num):
        if num not in self.poss:
            raise TypeError
        if self.num == 0:
            self.num = num
            self.poss = [num]
        else:
            if self.num != num:
                print(self.num, num)
                raise ZeroDivisionError

    def __sub__(self, num):
        if self.num != 0:
            pass
        else:
            if num in self.poss:
                self.poss.remove(num)

    def set_row(self, r):
        self.r = r

    def set_col(self, c):
        self.c = c

    def set_box(self, b):
        self.b = b


test = None


class Grid:
    def __init__(self, arr):
        self.grid = []
        for row in arr:
            cell_row = []
            for k in row:
                cell_row.append(Cell(k))
            self.grid.append(cell_row)
        self.grid = np.array(self.grid)
        self.boxes = {k:[] for k in range(9)}
        for i in range(9):
            for j in range(9):
                bn = 3 * (i // 3) + j // 3
                self.boxes[bn].append(self.grid[i, j])
                self.grid[i, j].set_box(bn)
                self.grid[i, j].set_row(i)
                self.grid[i, j].set_col(j)



    def __repr__(self):
        out = "\n\n"
        for i in range(9):
            rowS = "    "
            for j in range(9):
                if j != 0:
                    rowS += " | "
                n = self.grid[i,j].num
                if n != 0:
                    rowS += f"{n}"
                else:
                    rowS += " "
            if i != 0:
                out += "   -----------------------------------\n"
            out += rowS + "\n"
        return out + "\n\n"

    def check_rows(self):
        for row in self.grid:
            for cell in row:
                if cell.num != 0:
                    for cell2 in row:
                        cell2 - cell.num

    def check_cols(self):
        for col in self.grid.T:
            for cell in col:
                if cell.num != 0:
                    for cell2 in col:
                        cell2 - cell.num

    def check_boxes(self):
        for k in self.boxes.keys():
            box = self.boxes[k]
            for cell in box:
                if cell.num != 0:
                    for cell2 in box:
                        cell2 - cell.num

    def check_box_doubles(self):
        for k in self.boxes.keys():
            box = self.boxes[k]
            for p in range(1, 10):
                v_rows = list(set([cell1.r for cell1 in box if p in cell1.poss]))
                v_cols = list(set([cell1.c for cell1 in box if p in cell1.poss]))
                if len(v_rows) == 1:
                    for cell in self.grid[v_rows[0]]:
                        if cell not in box:
                            cell -  p
                if len(v_cols) == 1:
                    for cell in self.grid[: , v_cols[0]]:
                        if cell not in box:
                            cell -  p




    def set_singles(self):
        for i in range(9):
            for j in range(9):
                if len(self.grid[i,j].poss) == 1 and self.grid[i, j].num == 0:
                    try:
                        self.grid[i, j] + self.grid[i, j].poss[0]
                    except TypeError:
                        print(i, j, self.grid[i, j].poss[0])
                        raise TypeError

    def check_all(self):
        self.check_rows()
        self.check_cols()
        self.check_boxes()
        self.check_box_doubles()

    def step(self):
        self.check_all()
        self.set_singles()


    def is_solved(self):
        for cell in self.grid.flatten():
            if cell.num == 0:
                return False
        return True

    def is_real(self):
        self.check_all()
        for cell in self.grid.flatten():
            if len(cell.poss) == 0:
                return False
        for row in self.grid:
            st1 = [cell.num for cell in row if cell.num != 0]
            if len(set(st1)) != len(st1):
                return False
        for row in self.grid.T:
            st1 = [cell.num for cell in row if cell.num != 0]
            if len(set(st1)) != len(st1):
                return False
        for k in self.boxes.keys():
            row = self.boxes[k]
            st1 = [cell.num for cell in row if cell.num != 0]
            if len(set(st1)) != len(st1):
                return False
        return True

    def solve(self, verbose=True):
        sc = 0
        while sc < 50 and not self.is_solved():
            if verbose:
                print(self)
            sc += 1
            self.step()
        if verbose:
            print(self)

    def make_arr(self):
        return np.array([c.num for c in self.grid.flatten()]).reshape((9,9))

    def gsolve(self):
        self.solve(verbose=False)
        if self.is_real() and self.is_solved():
            G.grid = self.grid
            return True
        if not self.is_real():
            return False
        else:
            G2 = Grid(self.make_arr())
            G2.solve(verbose=False)
            if G2.is_solved():
                # print('this1')
                return G2.gsolve()
            lpos = np.min([len(c.poss) for c in G2.grid.flatten() if len(c.poss) >= 2])
            change_cells = [c for c in G2.grid.flatten() if len(c.poss) == lpos and c.num == 0]
            if len(change_cells) == 0:
                # print('this3')
                return False
            cc = change_cells[0]
            debug = (cc.r, cc.c, cc.num, cc.poss)
            cc + cc.poss[0]
            res = G2.gsolve()
            if res == False:
                self.grid[cc.r, cc.c] - cc.poss[0]
                return self.gsolve()
            else:
                # print('this2')
                return res



solved = 0
for num in range(50):
    g = read(num)
    G = Grid(g)
    G.solve(verbose=False)
    G.gsolve()
    if G.is_solved() and G.is_real():
        print(G)
        solved += 1

print(f"{solved} out of 50")

