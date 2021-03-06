from abc import ABC, abstractmethod
import time
import random
import sys
from typing import List, Tuple

import pygame
pygame.init()


class Cell:
    """A cell within a grid in a TPGameOfLife"""

    def __init__(self, state: int) -> None:
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

    def modify_cells(self, state: int, coordinates: List[Tuple[int]]) -> None:
        """Set state of multiple Cells on grid."""
        for coord in coordinates:
            self.grid[coord[0]][coord[1]].state = state
            
    def tick(self) -> None:
        """Move forward one generation."""
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
                    elif green_neighbours == 3 and red_neighbours != 3:
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

    def print(self) -> None:
        """Print grid in ASCII."""
        for y in reversed(range(self.rows)):
            for x in range(self.columns):
                if self.grid[x][y].state == self.RED:
                    print('R', end='')
                elif self.grid[x][y].state == self.GREEN:
                    print('G', end='')
                else:
                    print('-', end='')
            print()

    def start(self) -> None:
        """Start running the Game of Life via print method."""
        while True:
            print()
            self.print()
            self.tick()
            time.sleep(0.5)


class Graphics:
    """An object for displaying graphics, including the main menu and game."""
    # colour tuples
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    def __init__(self, resolution: Tuple[int, int]) -> None:
        """Create a Graphics object.
        
        screen      A pygame.Surface object representing the computer monitor
        """
        self.screen = pygame.display.set_mode(resolution)
        self.x_pixels = resolution[0]
        self.y_pixels = resolution[1]

    def draw_text(self, font: pygame.font.Font, word: str, colour:
                  Tuple[int, int], x_frac: Tuple[int, int],
                  y_frac: Tuple[int, int], sub_x_pixels: int = None,
                  sub_y_pixels: int = None,
                  sub_coordinates: Tuple[int, int] = [0, 0]) -> pygame.Rect:
        """Draw text onto the screen and return the corresponding pygame.Rect.

        x_frac and y_frac are tuples where the first element is the numerator and
        the second element is the denominator in a fraction that splits the
        screen lengthwise and widthwise, respectively.

        Normally, the entire screen is used for partitioning. However, the
        coordinates and resolution for a subwindow can be given to be used
        instead.
        """
        if sub_x_pixels and sub_y_pixels:
            x_pixels = sub_x_pixels
            y_pixels = sub_y_pixels
        else:
            x_pixels = self.x_pixels
            y_pixels = self.y_pixels

        word_surface = font.render(word, True, colour)
        x_coord = (((x_pixels/x_frac[1] - font.size(word)[0]) / 2)
                   + ((x_frac[0]-1)/x_frac[1]) * x_pixels)
        y_coord = (((y_pixels/y_frac[1] - font.size(word)[1]) / 2)
                   + ((y_frac[0]-1)/y_frac[1]) * y_pixels)
        self.screen.blit(word_surface, (x_coord+sub_coordinates[0],
                            y_coord+sub_coordinates[1]))
        return pygame.Rect((x_coord+sub_coordinates[0],
                            y_coord+sub_coordinates[1]), (font.size(word)[0],
                            font.size(word)[1]))

    def draw_main_menu(self) -> List[pygame.Rect]:
        """Draw the main menu and return the pygame.Rect that represent the
        buttons, top to bottom.
        """
        self.screen.fill(self.BLACK)
        title_font = pygame.font.SysFont('Arial', 100)
        button_font = pygame.font.SysFont('Arial', 200)
        self.draw_text(title_font, 'Game of Life Game', self.WHITE, (1, 1),
                       (1, 3))
        levels_button = self.draw_text(button_font, 'LEVELS', self.WHITE,
                                       (1, 1), (2, 3))
        quit_button = self.draw_text(button_font, 'QUIT', self.WHITE, (1, 1),
                                     (3, 3))
        return (levels_button, quit_button)

    def draw_level_select(self) -> None:
        """Draw the level select menu."""
        self.screen.fill(self.BLACK)
        level_font = pygame.font.SysFont('Arial', 400)
        self.draw_text(level_font, '1', self.WHITE, (1, 3), (1, 2))
        self.draw_text(level_font, '2', self.WHITE, (2, 3), (1, 2))
        self.draw_text(level_font, '3', self.WHITE, (3, 3), (1, 2))
        self.draw_text(level_font, '4', self.WHITE, (1, 3), (2, 2))
        self.draw_text(level_font, '5', self.WHITE, (2, 3), (2, 2))
        self.draw_text(level_font, '6', self.WHITE, (3, 3), (2, 2))

    def draw_grid(self) -> None:
        """Draw and empty grid onto the screen."""
        self.screen.fill(self.BLACK)
        for x in range(0, self.x_pixels, 20):
            pygame.draw.line(self.screen, self.WHITE, (x, 0),
                             (x, self.y_pixels))
        for y in range(0, self.y_pixels, 20):
            pygame.draw.line(self.screen, self.WHITE, (0, y),
                             (self.x_pixels, y))

    def draw_bar(self) -> None:
        """Draw status bar onto bottom of screen."""
        bar_rect = pygame.Rect((1, self.y_pixels-40), (self.x_pixels-2,
                                39))
        pygame.draw.rect(self.screen, self.BLACK, bar_rect)

    def colour_cell(self, colour: Tuple[int, int, int], \
                    mouse_pos: Tuple[int, int]):
        """Change the colour of a cell on screen."""
        x = mouse_pos[0]//20 * 20
        y = mouse_pos[1]//20 * 20
        cell_rect = pygame.Rect(x+1, y+1, 19, 19)
        pygame.draw.rect(self.screen, colour, cell_rect)


class GUI(ABC):
    """A Graphical User Interface, with methods for taking in user input."""

    def __init__(self, tpgol: TPGameOfLife, gr: Graphics):
        self.tpgol = tpgol
        self.gr = gr
        self.m1_ready = False
        self.m1_cancelled = False

    @abstractmethod
    def start(self):
        """Start the GUI."""
        pass

    def check_quit(self, event: pygame.event.EventType) -> None:
        """Terminate program if event calls for it."""
        if (event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

    def m1_pressed(self, mouse_buttons: Tuple[int, int, int]) -> bool:
        """Return whether a M1 press has been succesfully completed.

        Mouse press behaviour:
        For an M1 click to count, M1 must be pressed and let go of.
        In addition, pressing M2 will cancel any pending M1 click and
        disallow any M1 click so long as any pending M1 click is not
        let go of and so long as M2 is held down.
        """
        if not self.m1_cancelled and mouse_buttons[0]:
            self.m1_ready = True
        elif self.m1_cancelled and not mouse_buttons[0]:
            self.m1_cancelled = False
        if mouse_buttons[2]:
            self.m1_ready = False
            self.m1_cancelled = True
        if self.m1_ready and not mouse_buttons[0]:  # Completed press
            self.m1_ready = False
            return True
        return False


class MainMenu(GUI):
    """A menu for starting the game and exiting."""

    def __init__(self, tpgol: TPGameOfLife, gr: Graphics):
        super().__init__(tpgol, gr)

    def start(self):
        """Begin the main menu loop."""
        button_rects = gr.draw_main_menu()
        pygame.display.flip()

        while True:
            events = pygame.event.get()
            mouse_buttons = pygame.mouse.get_pressed()
            for event in events:
                self.check_quit(event)
            if self.m1_pressed(mouse_buttons):
                mouse_pos = pygame.mouse.get_pos()
                if button_rects[0].collidepoint(mouse_pos):
                    ls = LevelSelect(tpgol, gr)
                    ls.start()
                elif button_rects[1].collidepoint(mouse_pos):
                    sys.exit()


class LevelSelect(GUI):
    """A menu for selecting a level."""

    def __init__(self, tpgol: TPGameOfLife, gr: Graphics):
        super().__init__(tpgol, gr)

    def start(self):
        """Begin the level select menu loop."""
        while True:
            level = None  # Level selected by user

            self.gr.draw_level_select()
            pygame.display.flip()
            pygame.display.flip()  # This is not a typo

            while True:
                events = pygame.event.get()
                mouse_buttons = pygame.mouse.get_pressed()

                for event in events:
                    self.check_quit(event)

                if self.m1_pressed(mouse_buttons):
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos[0], mouse_pos[1]
                    x_pixels = pygame.display.Info().current_w
                    y_pixels = pygame.display.Info().current_h
                    if x in range(0, x_pixels//3) and y in range(0, y_pixels//2):
                        level = 1
                    elif (x in range(x_pixels//3, 2*x_pixels//3)
                          and y in range(0, y_pixels//2)):
                        level = 2
                    elif (x in range(2*x_pixels//3, x_pixels)
                          and y in range(0, y_pixels//2)):
                        level = 3
                    elif (x in range(0, x_pixels//3)
                          and y in range(y_pixels//2, y_pixels)):
                        level = 4
                    elif (x in range(x_pixels//3, 2*x_pixels//3)
                          and y in range(y_pixels//2, y_pixels)):
                        level = 5
                    elif (x in range(2*x_pixels//3, x_pixels)
                          and y in range(y_pixels//2, y_pixels)):
                        level = 6

                if level:
                    g = Game(tpgol, gr)
                    g.start(level)
                    break


class Game(GUI):
    """A gamified, graphical implementation of TPGameOfLife."""

    def __init__(self, tpgol: TPGameOfLife, gr: Graphics) -> None:
        """Create Graphics object."""
        super().__init__(tpgol, gr)
        self.tpgol = tpgol
        self.gr = gr

    def apply_level(self, level: int) -> None:
        # X and Y values of centre or pseudo-center cell
        cx = self.tpgol.columns // 2
        cy = self.tpgol.rows // 2
        # Max X and Y values
        mx = self.tpgol.columns
        my = self.tpgol.rows
        for column in range(self.tpgol.columns):
            for row in range(self.tpgol.rows):
                self.tpgol.grid[column][row].state = self.tpgol.DEAD
                self.tpgol.grid[column][row].next_state = self.tpgol.DEAD

        if level == 1:  # Glider
            self.starting_births = 8
            self.max_births = 8
            tpgol.modify_cells(tpgol.RED, [(1, 0), (2, 1), (0, 2), (1, 2),
                               (2, 2)])
        elif level == 2:  # R-pentomino
            self.starting_births = 0
            self.max_births = 5
            tpgol.modify_cells(tpgol.RED, [(cx, cy), (cx, cy-1), (cx+1, cy-1),
                               (cx-1, cy), (cx, cy+1)])
        elif level == 3:  # Pulsar
            self.starting_births = 3
            self.max_births = 3
            tpgol.modify_cells(tpgol.RED, [(cx-2, cy-2), (cx-2, cy-1),
                               (cx-2, cy), (cx-2, cy+1), (cx-2, cy+2),
                               (cx+2, cy-2), (cx+2, cy-1), (cx+2, cy),
                               (cx+2, cy+1), (cx+2, cy+2), (cx, cy+2),
                               (cx, cy-2)])
        elif level == 4:  # Thunderbird
            self.starting_births = 0
            self.max_births = 5
            x1 = self.tpgol.columns // 4
            x2 = 3 * self.tpgol.columns // 4
            tpgol.modify_cells(tpgol.RED, [(x1-1, cy-3), (x1, cy-3),
                               (x1+1, cy-3), (x1, cy-1), (x1, cy), (x1, cy+1),
                               (x2-1, cy-3), (x2, cy-3), (x2+1, cy-3),
                               (x2, cy-1), (x2, cy), (x2, cy+1)])
        elif level == 5:  # Pentadecathlon
            self.starting_births = 10
            self.max_births = 3
            tpgol.modify_cells(tpgol.RED, [(cx-5, 5), (cx-4, 5), (cx-3, 5),
                               (cx-2, 5), (cx-1, 5), (cx, 5), (cx+1, 5),
                               (cx+2, 5), (cx+3, 5), (cx+4, 5), (cx-5, my-6),
                               (cx-4, my-6), (cx-3, my-6), (cx-2, my-6),
                               (cx-1, my-6), (cx, my-6), (cx+1, my-6),
                               (cx+2, my-6), (cx+3, my-6), (cx+4, my-6),
                               (5, cy-5), (5, cy-4), (5, cy-3), (5, cy-2),
                               (5, cy-1), (5, cy), (5, cy+1), (5, cy+2),
                               (5, cy+3), (5, cy+4), (mx-6, cy-5), (mx-6,cy-4),
                               (mx-6, cy-3), (mx-6, cy-2), (mx-6, cy-1),
                               (mx-6, cy), (mx-6, cy+1), (mx-6, cy+2),
                               (mx-6, cy+3), (mx-6, cy+4)])
        elif level == 6:  # Pi-heptomino
            self.starting_births = 3
            self.max_births = 2
            tpgol.modify_cells(tpgol.RED, [(4, cy-1), (5, cy-1), (6, cy-1),
                               (6, cy), (4, cy+1), (5, cy+1), (6, cy+1),
                               (mx-7, cy-1), (mx-6, cy-1), (mx-5, cy-1),
                               (mx-7, cy), (mx-7, cy+1), (mx-6, cy+1),
                               (mx-5, cy+1), (cx-1, 6), (cx, 6), (cx+1, 6),
                               (cx-1, 5), (cx+1, 5), (cx-1, 4), (cx+1, 4),
                               (cx-1, my-7), (cx, my-7), (cx+1, my-7),
                               (cx-1, my-6), (cx+1, my-6), (cx-1, my-5),
                               (cx+1, my-5)])

    def start(self, level) -> None:
        """Begin the main game loop."""
        self.gr.draw_grid()
        self.gr.draw_bar()

        generation = 0
        status_font = pygame.font.SysFont('Arial', 20)
        back = False
        red_on_board = False
        win = False

        pause = False  # Pause GOL ticks or not
        clock = pygame.time.Clock()  # Clock for managing framerate
        GOLTICK = pygame.USEREVENT  # Event indicating to update GOL board
        FREQUENCY = 1000  # How often to update GOL board, in milliseconds

        pygame.time.set_timer(GOLTICK, FREQUENCY)

        self.apply_level(level)

        while True:
            events = pygame.event.get()
            mouse_buttons = pygame.mouse.get_pressed()

            for event in events:
                self.check_quit(event)
                if event.type == pygame.KEYDOWN:  # Key presses
                    if event.key == pygame.K_SPACE:  # Pause game
                        pause = not pause
                elif event.type == GOLTICK and not pause:  # Update GOL board
                    if self.starting_births < self.max_births:
                        self.starting_births += 1
                    tpgol.tick()
                    if not win:
                        generation += 1

            if self.m1_pressed(mouse_buttons):
                mouse_pos = pygame.mouse.get_pos()
                coordinates = (mouse_pos[0]//20, mouse_pos[1]//20)
                if (self.starting_births >= 1 and
                   (coordinates[0] < len(tpgol.grid) and
                    coordinates[1] < len(tpgol.grid[0])) and not win):
                    if (tpgol.grid[coordinates[0]][coordinates[1]].state ==
                        tpgol.DEAD):
                            tpgol.grid[coordinates[0]]\
                                      [coordinates[1]].state = tpgol.GREEN
                            self.starting_births -= 1
                # Back button
                elif (mouse_pos[0] in range(0, gr.x_pixels//3) and
                      mouse_pos[1] in range(gr.y_pixels-40, gr.y_pixels)):
                    break
                m1_ready = False


            # Update colours of all cells
            for x in range(tpgol.columns):
                for y in range(tpgol.rows):
                    state = tpgol.grid[x][y].state
                    if state == tpgol.DEAD:
                        colour = gr.BLACK
                    elif state == tpgol.RED:
                        colour = gr.RED
                        red_on_board = True
                    elif state == tpgol.GREEN:
                        colour = gr.GREEN
                    gr.colour_cell(colour, (x*20, y*20))

            if not red_on_board:
                win = True
            else:
                red_on_board = False

            self.gr.draw_bar()
            self.gr.draw_text(status_font, 'Availible Births: '
                               + str(self.starting_births),
                               self.gr.WHITE, (2, 3), ((gr.y_pixels-1)//40,
                               gr.y_pixels//40))
            self.gr.draw_text(status_font, 'Back', self.gr.WHITE, (1, 3),
                              ((gr.y_pixels-1)//40, gr.y_pixels//40))
            if win:
                self.gr.draw_text(status_font, 'Generation: '
                                  + str(generation), self.gr.GREEN, (3, 3),
                                  ((gr.y_pixels-1)//40, gr.y_pixels//40))
            else:
                self.gr.draw_text(status_font, 'Generation: '
                                  + str(generation), self.gr.WHITE, (3, 3),
                                  ((gr.y_pixels-1)//40, gr.y_pixels//40))

            clock.tick(60)
            pygame.display.flip()


if __name__ == '__main__':
    tpgol = TPGameOfLife(51, 39)
    gr = Graphics((1021, 821))
    m = MainMenu(tpgol, gr)
    m.start()
