""" Implementing a Pygame visuilization of the Robot simulation program """
# run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
#                   robot_type)
# print ('avg time steps: ' + str(run_simulation(3, 0.5, 1, 10, 10, 1, 0.9, 100, StandardRobot)))



import pygame
from sim import Position
import sim
pygame.init()
import math
clock = pygame.time.Clock()
# from pygame.locals import*
from pygame.math import Vector2

try:
    image = pygame.image.load('/Users/theprince/Projects/MIT_6.0001/Introduction_to_programming_MIT_6.0001-/problem_set_8/r1.png')
except:
    text = pygame.font.SysFont('Times New Roman', 50).render('image', False, (255, 255, 0))
    image = pygame.Surface((text.get_width()+1, text.get_height()+1))
    pygame.draw.rect(image, (0, 0, 255), (1, 1, *text.get_size()))
    image.blit(text, (1, 1))

w, h = image.get_size()


class Tile:
    """ Each box in a grid represents a Tile in a Room"""
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width 
        self.y = col * width
        self.color = RobotVisualization.WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Checking the state of a tile
    def get_pos(self):
        return self.row, self.col

    def is_clean(self):
        return self.color == RobotVisualization.WHITE #RED

    def is_dirty(self):
        return self.color == RobotVisualization.GREEN

    def is_furnished(self):
        return self.color == RobotVisualization.BLACK

    def is_occupied(self):
        return self.color == RobotVisualization.ORANGE

    # Setters
    def reset(self):
        self.color = RobotVisualization.WHITE

    def make_clean(self):
        self.color = RobotVisualization.WHITE 

    def make_dirty(self):
        self.color = RobotVisualization.BLACK

    def make_furnished(self):
        self.color = RobotVisualization.ORANGE

    def make_occupied(self):
        self.color = RobotVisualization.GREEN

    def set_color(self, dirt_amount):
        dirt_inverse = 100 - dirt_amount
        color_value = int((dirt_inverse/100) * 255)
        # print(color_value)
        # r, g, b = 0,0,0
        self.color= (color_value, color_value, color_value)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False

# "🚀"

class blitRotateImg(pygame.sprite.Sprite):
    vel = 5
    def __init__(self, surf, image, pos, originPos):
        super().__init__()
        self.pos = pos
        self.surf = surf
        self.originPos = originPos
        self.image = image

        # get a rotated image
    def move_left(self):
        self.pos[0] -= self.vel
        # print(self.pos[1])

    def move_right(self):
        self.pos[0] += self.vel
        # print(self.pos[0])

    def move_up(self):
        self.pos[1] -= self.vel
        # print(self.pos[1])

    def move_down(self):
        self.pos[1] += self.vel
        # print(self.pos[0])

    def draw(self, angle):
        # offset from pivot to center
        self.kill()
        image_rect = self.image.get_rect(topleft = (self.pos[0] - self.originPos[0], self.pos[1] - self.originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.pos) - image_rect.center
        
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        self.rotated_image_center = (self.pos[0] - rotated_offset.x, self.pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_image_rect = rotated_image.get_rect(center = self.rotated_image_center)

        # rotate and blit the image
        self.surf.blit(rotated_image, rotated_image_rect)


class RobotVisualization():
    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = "#191970"
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165 ,0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)

    # padding
    SIDE_PAD = 500
    TOP_PAD = 150

    pygame.display.set_caption("Robot Simulation")

    def __init__(self, num_robots, speed, capacity, rows, dirt_amount, min_coverage, robot_type, room_type):
        self.rows = rows
        self.num_robots = num_robots
        self.robot_type = robot_type
        self.room_type = room_type
        self.speed = speed
        self.capacity = capacity
        self.dirt_amount = dirt_amount
        self.min_coverage = min_coverage
        self.width = 600
        self.win = pygame.display.set_mode((self.width, self.width))
        self.angle = 0
        self.created_robots = []

        
    # Creating the grid 
    def make_grid(self):
        grid = []
        self.gap = (self.width - 0) // self.rows
        for i in range(self.rows):
            grid.append([])
            for j in range(self.rows):
                tile = Tile(i, j, self.gap, self.rows)
                grid[i].append(tile)
        return grid

    # Drawing the grid
    def draw_grid(self):
        gap = (self.width - 0) // self.rows
        # print(gap, "gap")
        for i in range(self.rows):
            pygame.draw.line(self.win, self.GREY, (0, i * gap), (self.width - 0, i * gap))
        for j in range(self.rows):
            pygame.draw.line(self.win, self.GREY, (j * gap, 0), (j * gap, self.width - 0))

    def draw(self, grid):
        self.win.fill(self.WHITE)
        for row in grid:
            for tile in row:
                tile.draw(self.win)

        self.draw_grid()
        # pygame.display.update()

    def create_robots(self, pos):
        r1 = blitRotateImg(self.win, image, pos, (w/2, h/2))
        self.created_robots.append(r1)

    # def update(self, my_room, robots):
    #     self.my_room = my_room
    #     self.robots = robots
    #     self.rob = []

    #     for robot in self.robots:
    #         robotPos = robot.get_robot_position()
    #         x, y = math.floor(robotPos.get_x()), math.floor(robotPos.get_y())
    #         print(x, y, self.gap)
    #         self.create_robots([(x * self.gap + self.gap/2), (y * self.gap + self.gap/2)])

    #     for stuf in self.rob:
    #         stuf.draw(self.angle)
    #     # print("update", self.my_room, self.robots)
    # run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
    #                   robot_type, room_type):

    def it_test(self):
        viz_generator = sim.run_simulation(self.num_robots, self.speed, self.capacity, self.rows, self.rows, self.dirt_amount, self.min_coverage, 100, sim.StandardRobot, "furnished")
        run = True
        while run:
            try:
                x = next(viz_generator)
            except StopIteration:
                run = False

    def run_sim(self):
        sim_generator = sim.run_simulation(self.num_robots, self.speed, self.capacity, self.rows, self.rows, self.dirt_amount, self.min_coverage, 100, sim.StandardRobot, self.room_type)
        sim_values = next(sim_generator)
        
        self.my_room = sim_values[0]
        self.robots = sim_values[1]

        ROWS = self.rows
        grid = self.make_grid()

        run = True

  
        # creating the robots 
        for robot in self.robots:
            robotPos = robot.get_robot_position()
            x, y = math.floor(robotPos.get_x()), math.floor(robotPos.get_y())
            self.create_robots([(x * self.gap + self.gap/2), (y * self.gap + self.gap/2)])


        while run:
            
            clock.tick(6)
            self.angle += 1  
            self.draw(grid)
            room_array = self.my_room.get_dirt_levels()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            tile_num = 0
            for row in grid:
                for tile in row:
                    # print(tile.get_pos())
                    spot = Position(tile.get_pos()[0], tile.get_pos()[1])

                    # Color tile
                    tile.set_color(room_array[tile_num])

                    # Clean tile
                    # if self.my_room.is_tile_cleaned(tile.get_pos()[0], tile.get_pos()[1]) == True:
                    #     tile.make_clean()

                    # Furnishing room
                    if self.room_type == "furnished":
                        if self.my_room.is_position_furnished(spot) == True:
                            tile.make_furnished()

                    # Adding cleaning robot
                    for robot in self.robots:
                        robotPos = robot.get_robot_position()
                        x, y = math.floor(robotPos.get_x()), math.floor(robotPos.get_y())
                        if (x == tile.get_pos()[0]) and (y == tile.get_pos()[1]):
                            tile.make_occupied()
                            ...
                    tile_num += 1
            
            # for animation in self.created_robots :
            #     animation.draw(self.angle)

            try:
                sim_values = next(sim_generator)
            except StopIteration:
                # print("Print call of duty")
                ...

            # displaying clean percent
            font = pygame.font.SysFont('Times New Roman', 20, True)
            clean_tiles = str(round(self.my_room.get_num_cleaned_tiles() / self.my_room.get_num_tiles() * 100))
            image = font.render('Tiles cleaned (%): ' + clean_tiles + "%", 1, self.BLUE )
            self.win.blit(image, (4, 4))

            pygame.display.flip() 


def it_test():
    viz_generator = sim.run_simulation(2, 0.5, 1, 10, 10, 4, 1, 100, sim.StandardRobot, "furnished")
    run = True
    while run:
        try:
            x = next(viz_generator)
        except StopIteration:
            run = False



if __name__ == "__main__":
    # Room with Furniture
    x = RobotVisualization(2, 0.5, 1, 10, 4, 1, sim.StandardRobot, "standard")
    x.run_sim()
    # RobotVisualization.run_sim(x)
    # it_test()