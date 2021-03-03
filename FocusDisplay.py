#Focus the game!

import FocusGame
import pygame
from pygame.locals import *


class FocusDisplay():

    def __init__(self):
        """

        """
        # initialize
        pygame.init()
        self.create_board()

    def run_game(self, screen):
        #Run unitl user quits
        running = True


        while running:

            #update board:

            #Did the user click close?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    print(event)
                elif event.type == MOUSEBUTTONUP:
                    print(event)


        pygame.quit()

    def draw_grid_vert(self, start_pos, end_pos, width, screen, color):
        """
        Draws the vertical lines of the game board separating spaces
        :param start_pos:
        :param end_pos:
        :param width:
        :param height:
        :return:
        """

        pygame.draw.line(screen, color, start_pos, end_pos, width)
        i = 0
        temp_start = start_pos[0]
        temp_end = end_pos[0]

        while i <= 6:
            pygame.draw.line(screen, color, (temp_start,start_pos[1]), (temp_end, end_pos[1]), width)
            temp_start += 75
            temp_end += 75
            i += 1

        return


    def draw_grid_horizontal(self, start_pos, end_pos, width, screen, color):
        """
        Draws a horizontal set of lines
        :param start_pos:
        :param end_pos:
        :param width:
        :param screen:
        :param color:
        :return:
        """
        pygame.draw.line(screen, color, start_pos, end_pos, width)
        i = 0
        temp_start = start_pos[1]
        temp_end = end_pos[1]

        while i <= 6:
            pygame.draw.line(screen, color, (start_pos[0],temp_start), (end_pos[0], temp_end), width)
            temp_start += 75
            temp_end += 75
            i += 1

        return

    def create_board(self):
        """

        :return:
        """
        # define colors
        BLACK = (0, 0, 0)
        GRAY = (127, 127, 127)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        # make a window
        screen = pygame.display.set_mode((550, 500))
        screen.fill(WHITE)

        #window caption
        pygame.display.set_caption("Focus the game!")

        #make the board
        pygame.draw.rect(screen, BLACK, (50, 20, 450, 450))

        #draw vertical lines
        self.draw_grid_vert((50, 20), (50, 470), 2, screen, BLUE)

        #draw horizontal lines
        self.draw_grid_horizontal((50, 20), (500, 20), 2, screen, BLUE)

        #display
        pygame.display.flip()
        self.run_game(screen)

    def fill_pieces(self, screen, RED, GREEN):
        """
        """
        pass


if __name__ == '__main__':
    game = FocusDisplay()
