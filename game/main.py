import pygame as pg
import sys
from pygame.locals import KEYDOWN, K_q

SCREENSIZE = WIDTH_SCR, HEIGHT_SCR = 1200, 800
GAME_AREA_MULTIPLE = 0.9
LABYRINTH_MULTIPLE = 0.98

walls = []


class Wall(object):

    def __init__(self, pos, width, height):
        walls.append(self)
        self.line = pg.Rect(pos[0], pos[1], width, height)


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

    def __init__(self):
        self.screen_size = [1200, 800]

    def wall(self):
        pass

    def create_grid_coordinates(self, start_width, start_height, width, height, grid_size):
        coordinates = []
        padding_width = width - (width * LABYRINTH_MULTIPLE)
        padding_height = height - (height * LABYRINTH_MULTIPLE)
        width_size = (width - (padding_width * 2)) / grid_size[0]
        height_size = (height - (padding_height * 2)) / grid_size[1]
        start_width += padding_width
        start_height += padding_height
        start_width_y = start_width
        start_height_x = start_height

        for _ in range(grid_size[0]):
            vertical_line = []
            for y in range(grid_size[1]):
                coordinate_y = int(y * height_size)
                vertical_line.append([start_width_y, start_height + coordinate_y])
            start_width_y += width_size
            coordinates.append(vertical_line)

        for _ in range(grid_size[1]):
            horizontal_line = []
            for x in range(grid_size[0]):
                coordinate_x = int(x * width_size)
                horizontal_line.append([start_width + coordinate_x, start_height_x])
            start_height_x += height_size
            coordinates.append(horizontal_line)

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
    labyrinth = Labyrinth()
    screen = pg.display.set_mode(SCREENSIZE)
    game_area = pg.Rect(set_game_area(screen))
    coordinates_for_walls = labyrinth.create_grid_coordinates(game_area.topleft[0],
                                                              game_area.topleft[1],
                                                              game_area.width,
                                                              game_area.height,
                                                              [25, 25])

    for line in coordinates_for_walls:
        for point in line:
            Wall()


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
        pg.draw.rect(screen, game_area_color, game_area, 2)
        screen.fill((0, 0, 0))
        for line in labyrinth.create_grid_coordinates(game_area.topleft[0],
                                                      game_area.topleft[1],
                                                      game_area.width,
                                                      game_area.height,
                                                      [25, 25]):
            pg.draw.lines(screen, lines_color, False, line, 1)
        pg.draw.rect(screen, (255, 200, 0), player.rect)
        pg.display.flip()


if __name__ == '__main__':
    main()
