import time
from typing import List


class TPGameOfLife:
"""Simulates a Game of Life following 2plife rules."""

    def __init__(self, columns: int, rows: int) -> None:
        """Create TPGameOfLife object.

        grid        A finite grid representing the Life universe
        columns     The number of columns in the grid (max x)
        rows        The number of rows in the grid (max y)
        """
        self.grid = [[Cell() for row in range(rows)] for column in
                    range(columns)]
        self.columns = columns
        self.rows = rows

    def seed(self, coordinates: List[List[int]]) -> None:
        """Set alive multiple Cells on grid."""
        for coord in coordinates:
            self.grid[coord[0]][coord[1]].alive = True
            
    def tick(self) -> None:
        """Apply changes to all Cells on grid to move forward a generation."""
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid[x][y].tick()

    def prepare_tick(self) -> None:
        """Let all Cells on grid know what their next move is."""
        for x in range(self.columns):
            for y in range(self.rows):  # Loop over every Cell
                cell = self.grid[x][y]
                live_neighbours = 0

                for n_x in range(x-1, x+2):
                    for n_y in range(y-1, y+2):  # Loop over all neighbours
                        if not ((n_x == x and n_y == y) and 
                                0 <= n_x < self.columns and
                                0 <= n_y < self.rows):
                                # If neighbour is not the Cell itself and
                                # if neighbour is within grid
                            if self.grid[n_x][n_y].alive:
                                live_neighbours += 1

                if (cell.alive and (live_neighbours == 2 or
                    live_neighbours == 3)):
                    cell.live()  # Survival
                elif cell.alive and live_neighbours <= 1:
                    cell.kill()  # Underpopulation
                elif cell.alive and live_neighbours >= 4:
                    cell.kill()  # Overpopulation
                elif not cell.alive and live_neighbours == 3:
                    cell.live()  # Birth

    def display(self) -> None:
        """Print grid in ASCII"""
        for y in reversed(range(self.rows)):
            for x in range(self.columns):
                if self.grid[x][y].alive:
                    print('*', end ='')
                else:
                    print('o', end ='')
            print()

    def play(self) -> None:
        """Start running the Game of Life via display()"""
        while True:
            print()
            self.display()
            self.prepare_tick()
            self.tick()
            time.sleep(0.5)


if __name__ == '__main__':
    pass
