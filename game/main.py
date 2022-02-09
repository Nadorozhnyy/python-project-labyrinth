import random

import pygame as pg
import sys
from pygame.locals import KEYDOWN, K_q

SCREENSIZE = WIDTH_SCR, HEIGHT_SCR = 1200, 800
GAME_AREA_MULTIPLE = 0.98
LABYRINTH_MULTIPLE = 0.98
GRID_SIZE = [30, 30]
GAME_AREA_BORDER_THICKNESS = 1
CELL_BORDER_THICKNESS = 2
player_speed = 75 / max(GRID_SIZE)
clock = pg.time.Clock()

COLORS = {
    'screen_color': (0, 0, 0),
    'player_color': (255, 200, 0),
    'center_point_color': (255, 99, 71),
    'exit_color': (255, 105, 180),
}

walls = []
center_points = []


class CenterPoints(object):

    def __init__(self, pos):
        center_points.append(self)
        self.rect = pg.Rect(pos[0], pos[1], 1, 1)


class Wall(object):

    def __init__(self, pos, width, height):
        walls.append(self)
        self.rect = pg.Rect(pos[0], pos[1], width, height)

    def kill(self):
        walls.remove(self)


class Exit(object):

    def __init__(self, pos, width, height):
        walls.append(self)
        self.rect = pg.Rect(pos[0], pos[1], width, height)


class Player(object):

    def __init__(self, start_coordinates, size):
        self.rect = pg.Rect(start_coordinates[0], start_coordinates[1], size, size)

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


# TODO rename, it's more about grid then about Labyrinth
class Labyrinth:

    def __init__(self, area_width, area_height, grid_number):
        self.width = area_width
        self.height = area_height
        self.grid_size = self.grid_numbers_on_x_axis, self.grid_numbers_on_y_axis = grid_number[0], grid_number[1]
        self.padding_x_axis = self.width - (self.width * LABYRINTH_MULTIPLE)
        self.padding_y_axis = self.height - (self.height * LABYRINTH_MULTIPLE)
        self.cell_width_size = (self.width - (self.padding_x_axis * 2)) / self.grid_numbers_on_x_axis
        self.cell_height_size = (self.height - (self.padding_y_axis * 2)) / self.grid_numbers_on_y_axis
        self.cell_border_thickness = CELL_BORDER_THICKNESS

    def set_center_points(self, start_x_coordinates, start_y_coordinates):
        """
        Create list of coordinates of cell centers
        :param start_x_coordinates: first coordinate on x-axis
        :param start_y_coordinates: first coordinate on y-axis
        :return: list of lists with x and y coordinates
        """
        points_center = []
        start_x_coordinates += self.padding_x_axis
        start_y_coordinates += self.padding_y_axis
        y_axis_bias = start_y_coordinates
        for _ in range(self.grid_numbers_on_y_axis):
            y_coordinate = y_axis_bias + self.cell_height_size / 2
            y_axis_bias += self.cell_height_size
            x_axis_bias = start_x_coordinates
            for _ in range(self.grid_numbers_on_x_axis):
                x_coordinate = x_axis_bias + self.cell_width_size / 2
                points_center.append([x_coordinate, y_coordinate])
                x_axis_bias += self.cell_width_size
        return points_center

    def create_grid_coordinates(self, start_x_coordinates, start_y_coordinates):
        """
        Create dict of coordinates vertical and horizontal lines to make grid
        :param start_x_coordinates:
        :param start_y_coordinates:
        :return: return dict with keys 'horizontal_line' and 'vertical_line' (list) and value lists of dict with keys
        for 'horizontal_line' dict 'point' and 'width' and keys for 'vertical_line' dict 'point' and 'height'
        """
        coordinates = {
            'horizontal_line': [],
            'vertical_line': [],
        }
        start_x_coordinates += self.padding_x_axis
        start_y_coordinates += self.padding_y_axis
        x_coordinates = start_x_coordinates
        y_coordinates = start_y_coordinates

        # add 1 to width and height to get rid of gap between walls
        # add horizontal line
        for _ in range(self.grid_numbers_on_x_axis):
            for y_grid in range(self.grid_numbers_on_y_axis + 1):
                coordinate_y = int(y_grid * self.cell_height_size)
                coordinates['horizontal_line'].append(
                    {
                        'point': [int(x_coordinates), int(start_y_coordinates + coordinate_y)],
                        'width': [int(self.cell_width_size) + 1]
                    }
                )
            x_coordinates += self.cell_width_size
        # add vertical line
        for _ in range(self.grid_numbers_on_y_axis):
            for x_grid in range(self.grid_numbers_on_x_axis + 1):
                coordinate_x = int(x_grid * self.cell_width_size)
                coordinates['vertical_line'].append(
                    {
                        'point': [int(start_x_coordinates + coordinate_x), int(y_coordinates)],
                        'height': [int(self.cell_height_size) + 1]
                    }
                )
            y_coordinates += self.cell_height_size

        return coordinates

    def coordinates_of_exit_point(self, points):
        """
        Choose random point from last half of bottom horizontal line of labyrinth
        :param points: list of CenterPoints object
        :return: return CenterPoints object
        """
        list_len = len(points)
        start_slice = int(list_len - self.grid_numbers_on_x_axis)
        end_slice = list_len - int(self.grid_numbers_on_x_axis / 2)
        return random.choice(points[start_slice:end_slice])

    def make_list_of_chunks(self, list_to_chunk):
        result = []
        lengths_list = self.list_of_lengths_chunks(random.randint(1, self.grid_numbers_on_x_axis))

        for count, value in enumerate(lengths_list):
            result.append([])
            for _ in range(value):
                pop_element = list_to_chunk.pop(0)
                result[count].append(pop_element)
        return result

    def list_of_lengths_chunks(self, numbers_of_chunks):
        """
        Create a list with random lengths to divide lines of labyrinth
        :param numbers_of_chunks: numbers of chunks to divide line
        :return: list of int
        """
        if numbers_of_chunks <= 1:
            return [self.grid_numbers_on_x_axis]
        elif numbers_of_chunks >= self.grid_numbers_on_x_axis:
            return [1] * self.grid_numbers_on_x_axis
        else:
            list_of_chunks_length = []
            # find max possible length of chunk
            # divide by two to avoid empty corridors
            max_partition_length = int((self.grid_numbers_on_x_axis - (numbers_of_chunks - 1)) / 2)
            for _ in range(numbers_of_chunks):
                if _ != numbers_of_chunks - 1:
                    # append random length of chunk from 1 to max possible
                    list_of_chunks_length.append(random.randint(1, max_partition_length))
                    # new max possible length of chunk after append random one
                    max_partition_length = int(
                        ((self.grid_numbers_on_x_axis - sum(list_of_chunks_length)) - (numbers_of_chunks - _ - 2)) / 2)
                else:
                    list_of_chunks_length.append(self.grid_numbers_on_x_axis - sum(list_of_chunks_length))
        # shuffle to maximize randomnicity of lengths
        random.shuffle(list_of_chunks_length)
        return list_of_chunks_length


def get_max_horizontal_coordinate():
    """
    :return: return max value of coordinates on x-axis (int)
    """
    horizontal_points_coordinate = []
    for point in center_points:
        horizontal_points_coordinate.append(point.rect.center[0])
    return max(horizontal_points_coordinate)


def check_events():
    """
    check quit event
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pg.quit()
            sys.exit()


def check_move_events(key, player, end_rect):
    """
    check move events
    :param key: pressed key
    :param player: player object
    :param end_rect: exit
    """
    if key[pg.K_LEFT]:
        player.move(-player_speed, 0)
    if key[pg.K_RIGHT]:
        player.move(player_speed, 0)
    if key[pg.K_UP]:
        player.move(0, -player_speed)
    if key[pg.K_DOWN]:
        player.move(0, player_speed)

    if player.rect.colliderect(end_rect):
        pg.quit()
        sys.exit()


def set_game_area(screen):
    """
    set game area settings
    :param screen: pygame screen
    :return: paddings on x-axis and y-axis and width and height of game area
    """
    width_game_area = screen.get_width() * GAME_AREA_MULTIPLE
    height_game_area = screen.get_height() * GAME_AREA_MULTIPLE
    padding_on_x_axis = (screen.get_width() - width_game_area) / 2
    padding_on_y_axis = (screen.get_height() - height_game_area) / 2
    return padding_on_x_axis, padding_on_y_axis, width_game_area, height_game_area


def create_rect_union(labyrinth):
    """

    :param labyrinth: labyrinth object
    :return: list of lists rects
    """
    rect_union = []
    for y in range(labyrinth.grid_numbers_on_y_axis):
        rect_union.append([])
        for x in range(y * labyrinth.grid_numbers_on_x_axis,
                       labyrinth.grid_numbers_on_x_axis + (y * labyrinth.grid_numbers_on_x_axis)):
            rect_union[y].append(center_points[x].rect)
    return rect_union


def set_labyrinth(labyrinth):
    labyrinth_all_rects = create_rect_union(labyrinth)

    for rect_count, rect_value in enumerate(labyrinth_all_rects):
        # first line will be empty
        if rect_count == 0:
            rect_from_line = pg.Rect.unionall(rect_value[0], rect_value)
            line_intersection = rect_from_line.collidelistall(walls)
            # remove all edge in first line rect
            for _ in reversed(line_intersection):
                walls[_].kill()
        else:
            # other lines will be split into parts
            chunks_list = labyrinth.make_list_of_chunks(rect_value)
            for chunk_count, chunks_value in enumerate(chunks_list):
                rect_from_chunk = pg.Rect.unionall(chunks_value[0], chunks_value)
                chunk_intersection = rect_from_chunk.collidelistall(walls)
                # remove all edge in chunk rect
                for _ in reversed(chunk_intersection):
                    walls[_].kill()

                intersection_centers_point = rect_from_chunk.collidelistall(center_points)
                random_point = random.choice(intersection_centers_point)
                random_point_in_line = center_points[random_point].rect
                last_point = intersection_centers_point[-1]
                # choose what edge will be removed (top or right)
                flip_coin = random.randint(0, 1)
                if flip_coin == 0 or center_points[last_point].rect.center[0] == get_max_horizontal_coordinate():
                    rect = center_points[random_point - labyrinth.grid_numbers_on_x_axis].rect
                else:
                    rect = center_points[last_point + 1].rect
                rect_union = pg.Rect.union(random_point_in_line, rect)
                points_intersection = rect_union.collidelistall(walls)
                # remove top or right edge to create labyrinth
                for _ in reversed(points_intersection):
                    walls[_].kill()


def main():
    pg.init()
    screen = pg.display.set_mode(SCREENSIZE)
    game_area = pg.Rect(set_game_area(screen))
    labyrinth = Labyrinth(game_area.width, game_area.height, GRID_SIZE)
    coordinates_for_center = labyrinth.set_center_points(game_area.topleft[0], game_area.topleft[1])
    coordinates_for_walls = labyrinth.create_grid_coordinates(game_area.topleft[0], game_area.topleft[1])

    for point in coordinates_for_walls['vertical_line']:
        Wall(point['point'], labyrinth.cell_border_thickness, point['height'][0])

    for point in coordinates_for_walls['horizontal_line']:
        Wall(point['point'], point['width'][0], labyrinth.cell_border_thickness)

    for point in coordinates_for_center:
        CenterPoints(point)

    size_of_player = min([labyrinth.cell_width_size, labyrinth.cell_height_size]) / 2
    # get coordinates of first center point and subtract half of players size
    start_player_coordinates = [
        coordinates_for_center[0][0] - (size_of_player / 2),
        coordinates_for_center[0][1] - (size_of_player / 2)
    ]
    player = Player(start_player_coordinates, size_of_player)
    exit_rect = labyrinth.coordinates_of_exit_point(center_points).rect.inflate(size_of_player, size_of_player)
    set_labyrinth(labyrinth)

    while True:
        clock.tick(100)
        check_events()
        key = pg.key.get_pressed()
        check_move_events(key, player, exit_rect)
        screen.fill(COLORS['screen_color'])
        for wall in walls:
            pg.draw.rect(screen, pg.Color('azure'), wall.rect)
        pg.draw.rect(screen, pg.Color('aquamarine2'), game_area, GAME_AREA_BORDER_THICKNESS)
        pg.draw.rect(screen, COLORS['player_color'], player.rect)
        pg.draw.rect(screen, COLORS['exit_color'], exit_rect)
        pg.display.flip()
        clock.tick(360)


if __name__ == '__main__':
    main()
