import pathlib
import random


from typing import List, Optional, Tuple
from copy import deepcopy

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

        self.pause = False

    def create_grid(self, randomize: bool=False) -> Grid:
        if randomize == True:
            self.clist = []
            for i in range(self.rows):
                self.clist.append([])
                for j in range(self.cols):
                    self.clist[i].append(random.randint(0, 1))
        else:
            self.clist = []
            for i in range(self.rows):
                self.clist.append([])
                for j in range(self.cols):
                    self.clist[i].append(0)

        return self.clist



    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        cell_row, cell_col = cell
        neighbours = []

        if cell_row == 0:
            r, k = 0, 2
        elif cell_row == self.rows - 1:
            r, k = -1, 1
        else:
            r, k = -1, 2

        if cell_col == 0:
            c, t = 0, 2
        elif cell_col == self.cols - 1:
            c, t = -1, 1
        else:
            c, t = -1, 2

        for i in range(cell_row + r, cell_row + k):
            for j in range(cell_col + c, cell_col + t):
                if i == cell_row and j == cell_col:
                    pass
                else:
                    neighbours.append((i, j))
        return neighbours


    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        count = 0
        newgrid = []

        for i in range(self.rows):
            newgrid.append([])
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))

                for k in range (len(neighbours)):
                    cell_row, cell_col = neighbours[k]
                    if self.curr_generation[cell_row][cell_col] == 1:
                        count += 1

                if (count == 2 or count == 3) and self.curr_generation[i][j] == 1:
                    newgrid[i].append(1)
                elif count == 3 and self.curr_generation[i][j] == 0:
                    newgrid[i].append(1)
                else:
                    newgrid[i].append(0)

                count = 0

        return newgrid


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = deepcopy(self.get_next_generation())

        self.generations += 1


    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations <= self.max_generations


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation


    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []

        for line in open(filename).read().split("\n"):
            #print (list(line))
            if len(line) != 0:
                grid.append(list(line))

        life = GameOfLife((len(grid), len(grid[0])))
        life.curr_generation = grid

        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename,'w')
        for line in range(self.rows):
            file.write(''.join(self.curr_generation[line]))
            file.write("\n")
        file.close()

        pass
