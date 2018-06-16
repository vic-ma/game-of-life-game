import time
import random
import sys
from typing import List, Tuple

import pygame
pygame.init()


class Cell:
    """A cell within a grid in a TPGameOfLife"""

    def __init__(self, state: int):
        """Create Cell object.

        state           The state of the Cell (dead=0/red=1/green=2)
        next_state      The state of the Cell in the next generation
        """
        self.state = state
        self.next_state = self.state


class TPGameOfLife:
    """A simulation of a version of Life based on p2life."""
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
        self.grid = [[Cell(self.DEAD) for row in range(rows)] for column in
                    range(columns)]
        self.columns = columns
        self.rows = rows

    def modify_cell(self, state: int, coordinates: List[Tuple[int]]) -> None:
        """Set state of Cells on grid."""
        for coord in coordinates:
            self.grid[coord[0]][coord[1]].state = state
            
    def tick(self) -> None:
        """Let all Cells on grid know what their next move is."""
        for x in range(self.columns):
            for y in range(self.rows):  # Loop over every Cell
                cell = self.grid[x][y]
                red_neighbours = 0
                green_neighbours = 0

                for n_x in range(x-1, x+2):
                    for n_y in range(y-1, y+2):  # Loop over all neighbours
                        if (not(n_x == x and n_y == y) and 
                            0 <= n_x < self.columns and
                            0 <= n_y < self.rows):
                                # If neighbour is not the Cell itself and
                                # if neighbour is within grid
                            if self.grid[n_x][n_y].state == self.RED:
                                red_neighbours += 1
                            elif self.grid[n_x][n_y].state == self.GREEN:
                                green_neighbours += 1

                if cell.state == self.DEAD:  #Birth
                    if red_neighbours == 3 and green_neighbours == 3:
                        if random.randint(1, 2) == 1:
                            cell.next_state = self.RED
                        else:
                            cell.next_state = self.GREEN
                    elif red_neighbours == 3 and green_neighbours != 3:
                        cell.next_state = self.RED
                    elif green_neighbours == 3 and red_neighbours !=3:
                        cell.next_state = self.GREEN
                elif cell.state == self.RED:  # Red survival/death
                    if 2 <= red_neighbours - green_neighbours <= 3:
                        cell.next_state = self.RED
                    elif (red_neighbours - green_neighbours == 1 and
                          red_neighbours >= 2):
                        cell.next_state = self.RED
                    else:
                        cell.next_state = self.DEAD
                elif cell.state == self.GREEN: # Green survival/death
                    if 2 <= green_neighbours - red_neighbours <= 3:
                        cell.next_state = self.GREEN
                    elif (green_neighbours - red_neighbours == 1 and
                          green_neighbours >= 2):
                        cell.next_state = self.GREEN
                    else:
                        cell.next_state = self.DEAD

        # Apply changes to all Cells on grid to move forward a generation
        for x in range(self.columns):
            for y in range(self.rows):
                self.grid[x][y].state = self.grid[x][y].next_state

    def display(self) -> None:
        """Print grid in ASCII"""
        for y in reversed(range(self.rows)):
            for x in range(self.columns):
                if self.grid[x][y].state == self.RED:
                    print('R', end='')
                elif self.grid[x][y].state == self.GREEN:
                    print('G', end='')
                else:
                    print('-', end='')
            print()

    def play(self) -> None:
        """Start running the Game of Life via display()"""
        while True:
            print()
            self.display()
            self.tick()
            time.sleep(0.5)


class GameScreen:
    """A screen that vizualizes an instance of TPGameOfLife."""

    def __init__(self, resolution: Tuple[int, int]) -> None:
        """Create a GameScreen object.
        
        screen      A pygame.Surface object representing the computer monitor
        """
        self.screen = pygame.display.set_mode(resolution)

    def draw_grid(self, colour: Tuple[int, int, int]) -> None:
        """Draw gridlines onto screen."""
        x_pixels = pygame.display.Info().current_w
        y_pixels = pygame.display.Info().current_h
        for x in range(0, x_pixels+1, 20):
            pygame.draw.line(self.screen, colour, (x, 0), (x, x_pixels))
        for y in range(0, y_pixels+1, 20):
            pygame.draw.line(self.screen, colour, (0, y), (y_pixels, y))

    def colour_cell(self, colour: Tuple[int, int, int], \
            mouse_pos: Tuple[int, int]):
        """Change the colour of a cell on screen and return a pygame.Rect
        object for efficient updating of the screen.
        """
        x = mouse_pos[0]//20 * 20
        y = mouse_pos[1]//20 * 20
        cell_rect = pygame.Rect(x+1, y+1, 19, 19)  # Offset for grid lines
        pygame.draw.rect(self.screen, colour, cell_rect)

class Graphics:
    """A Graphical implementation of TPGameOfLife."""
    # colour tuples
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    def __init__(self, tpgol: TPGameOfLife, gs: GameScreen):
        """Create Graphics object."""
        self.tpgol = tpgol
        self.gs = gs

    def start_game(self):
        """Begin the main game loop."""
        self.gs.draw_grid(self.WHITE)
        pygame.display.update()

        m1_ready = False      # If M1 is pressed down
        m1_cancelled = False  # If M2 was pressed (thus cancelling M1)

        pause = False  # Pause GOL ticks or not

        clock = pygame.time.Clock()  # Clock for managing framerate

        GOLTICK = pygame.USEREVENT  # Event indicating to update GOL board
        FREQUENCY = 1000  # How often to update GOL board, in milliseconds
        pygame.time.set_timer(GOLTICK, FREQUENCY)

        while True:
            events = pygame.event.get()
            mouse_buttons = pygame.mouse.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:  # Quit game by closing window
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # Key presses
                    key = event.key
                    if key == pygame.K_ESCAPE:  # Quit game by <Esc>
                        sys.exit()
                    elif key == pygame.K_SPACE:  # Pause game
                        pause = not pause
                elif event.type == GOLTICK and not pause:  # Update GOL board
                    tpgol.tick()

            # Mouse Behaviour:
            # For an M1 click to count, M1 must be pressed and let go of.
            # In addition, pressing M2 will cancel any pending M1 click and
            # disallow any M1 click so long as any pending M1 click is not
            # let go of and so long as M2 is held down.

            if not m1_cancelled and mouse_buttons[0]:
                m1_ready = True
            elif m1_cancelled and not mouse_buttons[0]:
                m1_cancelled = False
            if mouse_buttons[2]:
                m1_ready = False
                m1_cancelled = True
            if m1_ready and not mouse_buttons[0]:  # Completed press
                mouse_pos = pygame.mouse.get_pos()
                coordinates = (mouse_pos[0]//20, mouse_pos[1]//20)
                tpgol.modify_cell(2, (coordinates,))
                m1_ready = False

            for x in range(tpgol.columns):
                for y in range(tpgol.rows):
                    state = tpgol.grid[x][y].state
                    if state == tpgol.DEAD:
                        colour = self.BLACK
                    elif state == tpgol.RED:
                        colour = self.RED
                    elif state == tpgol.GREEN:
                        colour = self.GREEN
                    gs.colour_cell(colour, (x*20, y*20))

            clock.tick(60)
            pygame.display.update()


if __name__ == '__main__':
    tpgol = TPGameOfLife(50, 50)
    gs = GameScreen((500, 500))
    g = Graphics(tpgol, gs)
    g.start_game()
