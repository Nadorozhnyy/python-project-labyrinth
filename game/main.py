import random

import pygame as pg
import sys
from pygame.locals import KEYDOWN, K_q

SCREENSIZE = WIDTH_SCR, HEIGHT_SCR = 1200, 800
GAME_AREA_MULTIPLE = 0.9
LABYRINTH_MULTIPLE = 0.98
GRID_SIZE = [3, 3]
GAME_AREA_BORDER_THICKNESS = 1
CELL_BORDER_THICKNESS = 2

COLORS = {
    'screen_color': (0, 0, 0),
    'player_color': (255, 200, 0),
}

walls = []


class Wall(object):

    def __init__(self, pos, width, height):
        walls.append(self)
        self.rect = pg.Rect(pos[0], pos[1], width, height)

    def kill(self):
        walls.remove(self)


class Player(object):

    def __init__(self):
        self.rect = pg.Rect(32, 32, 16, 16)

    def move(self, dx, dy):

        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


class Labyrinth:

    def __init__(self, area_width, area_height, grid_size):
        self.width = area_width
        self.height = area_height
        self.self_grid_size = self.grid_width, self.grid_height = grid_size[0], grid_size[1]
        self.padding_horizontal = self.width - (self.width * LABYRINTH_MULTIPLE)
        self.padding_vertical = self.height - (self.height * LABYRINTH_MULTIPLE)
        self.cell_width_size = (self.width - (self.padding_horizontal * 2)) / self.grid_width
        self.cell_height_size = (self.height - (self.padding_vertical * 2)) / self.grid_height
        self.cell_border_thickness = CELL_BORDER_THICKNESS

    def points_set(self):
        pass

    def set_grid_size(self):
        pass

    def create_grid_coordinates(self, start_width, start_height):
        coordinates = {
            'vertical_line': [],
            'horizontal_line': [],
        }

        start_width += self.padding_horizontal
        start_height += self.padding_vertical
        start_width_y = start_width
        start_height_x = start_height

        for _ in range(self.grid_width):
            for y in range(self.grid_height + 1):
                coordinate_y = int(y * self.cell_height_size)
                coordinates['vertical_line'].append(
                    {
                        'point': [int(start_width_y), int(start_height + coordinate_y)],
                        'width': [int(self.cell_width_size)]
                    }
                )
            start_width_y += self.cell_width_size

        for _ in range(self.grid_height):
            for x in range(self.grid_width + 1):
                coordinate_x = int(x * self.cell_width_size)
                coordinates['horizontal_line'].append(
                    {
                        'point': [int(start_width + coordinate_x), int(start_height_x)],
                        'height': [int(self.cell_height_size)]
                    }
                )
            start_height_x += self.cell_height_size

        return coordinates


def check_events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pg.quit()
            sys.exit()


def set_game_area(screen):
    width_game_area = screen.get_width() * GAME_AREA_MULTIPLE
    height_game_area = screen.get_height() * GAME_AREA_MULTIPLE
    padding_width_area = (screen.get_width() - width_game_area) / 2
    padding_height_area = (screen.get_height() - height_game_area) / 2
    return padding_width_area, padding_height_area, width_game_area, height_game_area


def main():
    pg.init()
    player = Player()
    screen = pg.display.set_mode(SCREENSIZE)
    game_area = pg.Rect(set_game_area(screen))
    labyrinth = Labyrinth(game_area.width, game_area.height, GRID_SIZE)
    border_thickness = labyrinth.cell_border_thickness
    coordinates_for_walls = labyrinth.create_grid_coordinates(game_area.topleft[0], game_area.topleft[1])

    for point in coordinates_for_walls['vertical_line']:
        Wall(point['point'], point['width'][0], border_thickness)
    for point in coordinates_for_walls['horizontal_line']:
        Wall(point['point'], border_thickness, point['height'][0])

    while True:
        check_events()
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            player.move(-2, 0)
        if key[pg.K_RIGHT]:
            player.move(2, 0)
        if key[pg.K_UP]:
            player.move(0, -2)
        if key[pg.K_DOWN]:
            player.move(0, 2)
        game_area_color = pg.Color('aquamarine2')
        lines_color = pg.Color('azure')
        screen.fill(COLORS['screen_color'])
        for wall in walls:
            pg.draw.rect(screen, lines_color, wall.rect)
        pg.draw.rect(screen, game_area_color, game_area, GAME_AREA_BORDER_THICKNESS)
        pg.draw.rect(screen, COLORS['player_color'], player.rect)
        pg.display.flip()


if __name__ == '__main__':
    main()
