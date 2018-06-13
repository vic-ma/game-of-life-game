import time
import random
from typing import List


class TPGameOfLife:
    """Simulates a version of Life based on p2life."""
    # Cell state codes
    DEAD = 0
    RED = 1
    GREEN = 2

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

    def seed(self, state, coordinates: List[List[int]]) -> None:
        """Set state of multiple Cells on grid."""
        for coord in coordinates:
            self.grid[coord[0]][coord[1]].state = True
            
    def prepare_tick(self) -> None:
        """Let all Cells on grid know what their next move is."""
        for x in range(self.columns):
            for y in range(self.rows):  # Loop over every Cell
                cell = self.grid[x][y]
                red_neighbours = 0
                green_neighbours = 0

                for n_x in range(x-1, x+2):
                    for n_y in range(y-1, y+2):  # Loop over all neighbours
                        if not ((n_x == x and n_y == y) and 
                                0 <= n_x < self.columns and
                                0 <= n_y < self.rows):
                                # If neighbour is not the Cell itself and
                                # if neighbour is within grid
                            if self.grid[n_x][n_y].state == RED:
                                red_neighbours += 1
                            elif self.grid[n_x][n_y].state == GREEN:
                                green_neighbours += 1

                if cell.state == DEAD:  #Birth
                    if red_neighbours == 3 and green_neighbours == 3:
                        if random.randint(1, 2) == 1:
                            cell.next_state == RED
                        else:
                            cell.next_state == GREEN
                    elif red_neighbours == 3 and green_neighbours != 3:
                        cell.next_state = RED
                    elif green_neighbours == 3 and red_neighbours !=3:
                        cell.next_state = GREEN
                elif cell.state == RED:  # Red survival/death
                    if 2 <= red_neighbours - green_neighbours <= 3:
                        cell.next_state = RED
                    elif (red_neighbours - green_neighbours == 1 and
                          red_neighbours >= 2):
                        cell.next_state = RED
                    else:
                        cell.next_state = DEAD
                elif cell.state == GREEN: # Green survival/death
                    if 2 <= green_neighbours - red_neighbours <= 3:
                        cell.next_state = GREEN
                    elif (green_neighbours - red_neighbours == 1 and
                          green_neighbours >= 2):
                        cell.next_state = GREEN
                    else:
                        cell.next_state = DEAD



    def tick(self) -> None:
        """Apply changes to all Cells on grid to move forward a generation."""
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid[x][y].tick()

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


class Cell:
    """A cell within a grid in a TPGameOfLife"""

    def __init__(self, state: int):
        """Create Cell object.

        state           The state of the Cell (dead=0/red=1/green=2)
        next_state      The state of the Cell in the next generation
        """
        self.state = state
        self.next_state = self.state

if __name__ == '__main__':
    pass
