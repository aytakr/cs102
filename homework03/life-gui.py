import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(
        self,
        life: GameOfLife,
        cell_size: int = 10,
        speed: int = 2
    ) -> None:
        super().__init__(life)
        self.height = 480
        self.width = 480
        self.cell_size = self.height // life.rows
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment
        s = self.cell_size
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.width))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.height, y))
        pass

    def draw_grid(self) -> None:
        # Copy from previous assignment
        s = self.cell_size
        for i in range(life.rows):
            for j in range(life.cols):
                if life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (
                        s*i, s*j, s, s))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (
                        s*i, s*j, s, s))

    def run(self) -> None:
        # Copy from previous assignment
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.draw_grid()
        running = True
        while running:
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            while (
                life.is_changing and
                life.is_max_generations_exceeded and
                running
            ):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        break
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            life.pause = not life.pause
                    if event.type == MOUSEBUTTONDOWN:
                        pos_row, pos_col = pygame.mouse.get_pos()
                        row = pos_row // self.cell_size
                        col = pos_col // self.cell_size
                        cell = life.curr_generation[row][col]
                        life.curr_generation[row][col] = 1 - cell
                if not life.pause:
                    life.step()

                self.draw_grid()
                self.draw_lines()

                pygame.display.flip()
                clock.tick(self.speed)

            pygame.quit()
            exit()
