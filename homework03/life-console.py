import curses

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        for i in range(life.rows):
            screen.addstr(i + 1, 0, '|')
            screen.addstr(i + 1, life.cols + 1, '|')

        for j in range(life.cols):
            screen.addstr(0, j + 1, '-')
            screen.addstr(life.rows + 1, j + 1, '-')

        screen.addstr(0, 0, '+')
        screen.addstr(life.rows + 1, 0, '+')
        screen.addstr(0, life.cols + 1, '+')
        screen.addstr(life.rows + 1, life.cols + 1, '+')

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(life.rows):
            for j in range(life.cols):
                if life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j + 1, '*')
                else:
                    screen.addstr(i + 1, j + 1, ' ')

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        self.draw_borders(screen)
        self.draw_grid(screen)

        while True:
            life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.5)
        curses.endwin()
