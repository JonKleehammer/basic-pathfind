import pygame
import Tile as t
import time
import random
import Plotter

# Program by Jonathan Kleehammer
# ------------------------------
# Program is designed to randomly generate a grid of open space and walls
# Generates a random place for a start tile and goal tile
# uses A* search algorithm to find the quickest path to the goal
# visualised using pygame (tiles shaded red based on distance from goal, start is green, goal is yellow
# tiles searched, tiles being considered are red, path is green when found at the end

# after 'simulation_limit' simulations are run, display the data as a 3d graph using matplotlib
# xyz axis = (goal

# IF YOU ARE MORE INTERESTED IN THE DATA YOU CAN COMMENT OUT THE LINE FOR DISPLAY AND SLEEP (the call for display and the sleep timer)
# THIS MAKES THE PROGRAM RUN MUCH QUICKER BY DISABLING THE DISPLAY AND SLEEP

# set up variables and pygame
####################################################################################
# the amount of simulations wanted and the current simulation #
simulation_limit = 100
simulation_count = 1

# recording how many tiles have been checked, and how far the quickest path to the goal is
check_count = 0
path_count = 0

# declaring an empty list for storing test data
efficiency_data = []

# basic grid dimensions
grid_width = 25
grid_height = 25
tile_size = 25


path = []

# initiallizing pygame and setting up the screen
pygame.init()
screen = pygame.display.set_mode((grid_width * tile_size,
                                  grid_height * tile_size))

# methods
####################################################################################
# method to call for displaying the screen
def display():
    for tile in grid:
        tile = grid[tile]
        pygame.draw.rect(screen, tile.color, (tile.x * tile_size, tile.y * tile_size,
                                              tile_size, tile_size))
    pygame.display.flip()


# setting heuristics (estimate values) for each tile to give the ai a general idea of a direction
def set_heuristics():
    goal_x = t.Tile.goal_tile.x
    goal_y = t.Tile.goal_tile.y

    for tile in grid:
        tile = grid[tile]
        tile.h = abs(goal_x - tile.x) + abs(goal_y - tile.y)

        # setting up a gradient showing distance from the goal
        if tile != tile.start_tile:
            tile.adjust_color((0,   -100 * (float(tile.h) / (grid_height + grid_width)),
                                    -100 * (float(tile.h) / (grid_height + grid_width))))


# Given a tile, returns a list of neighbors
def neighbours(tile):
    neighbour_list = []
    if tile.x - 1 >= 0:
        neighbour_list.append(grid[tile.x - 1, tile.y])
    if tile.x + 1 < grid_width:
        neighbour_list.append(grid[tile.x + 1, tile.y])

    if tile.y - 1 >= 0:
        neighbour_list.append(grid[tile.x, tile.y - 1])
    if tile.y + 1 < grid_height:
        neighbour_list.append(grid[tile.x, tile.y + 1])
    return neighbour_list


# Checks the list of neighbors of the currently selected tile choosing the closest to the goal
def pathfind():
    global current_tile
    global searching
    candidates = neighbours(current_tile)

    # calculating candidate scores
    for tile in candidates:
        global check_count
        check_count += 1

        tile.g = current_tile.g + 1
        calculated_f = tile.g + tile.h

        # not in the open list yet
        if tile in closed_list:
            pass
        elif tile.obstacle is True or tile is t.Tile.start_tile:
            closed_list.append(tile)
        elif tile.f is None:
            tile.f = calculated_f
            tile.parent = current_tile
            tile.set_color()
            tile.adjust_color((100, -150, -150))
            open_list.append(tile)
        # if the newly calculated f is lower
        elif tile.f < calculated_f:
            tile.f = calculated_f
            tile.g = current_tile.g + 1
            tile.parent = current_tile

    if len(open_list) <= 0:
        searching = False

    # ensuring that there are available tiles to move to
    # then choosing the lowest cost
    if len(open_list) > 0:
        lowest_f = open_list[0]
        for tile in open_list:
            if tile.f < lowest_f.f:
                lowest_f = tile

        # switching the selction to the lowest_f
        open_list.remove(lowest_f)
        closed_list.append(lowest_f)
        lowest_f.set_color()
        lowest_f.adjust_color((-100, -100, 100))
        current_tile = lowest_f
    # if the open_list is empty then we've run out of paths to reach
    else:
        print('NO PATH')


    # checking if the goal has been reached
    if current_tile.h == 0:
        searching = False
        global connecting
        connecting = True


# after we find the optimal path to the goal, we start at the end and move back towards our start
def connect():
    global path_count
    path_count += 1
    global current_tile

    # when the goal tile is searched it turns blue, we want to change this tile back to yellow
    if current_tile == t.Tile.goal_tile:
        current_tile.set_color((255, 255, 0))


    # creating a gradient of colors starting from yellow and moving to green
    lastColor = current_tile.get_color()
    current_tile = current_tile.parent
    current_tile.set_color((lastColor[0] - 10, lastColor[1] + 0, lastColor[2] + 0))


    if current_tile == t.Tile.start_tile:
        global connecting
        connecting = False


# program looping until simulation limit is reached or ESC is pressed (while not in sleep)
program_looping = True
while program_looping:
    # creating a dictionary where the key is the coordinates and the value is the tile itself
    grid = dict()

    # iterating to create each grid starting from 0,0 to grid_width-1, grid_height-1
    for x in range(0, grid_width):
        for y in range(0, grid_width):
            grid[(x, y)] = t.Tile(x, y)

    # placing the start tile and the goal tile in random positions
    # randomly generated x and y
    # if the x and y are the same for the start, generate new xy for goal until both are filled
    objective_placing = True
    while objective_placing:
        rand_x = random.randint(0, grid_width - 1)
        rand_y = random.randint(0, grid_height - 1)

        if t.Tile.start_tile is None:
            grid[(rand_x, rand_y)].set_start()
        elif t.Tile.goal_tile is None and t.Tile.start_tile != grid[rand_x, rand_y]:
            grid[(rand_x, rand_y)].set_goal()
        elif t.Tile.start_tile and t.Tile.goal_tile:
            objective_placing = False
            current_tile = t.Tile.start_tile

    # after objectives and tiles are placed calculate heuristic values
    set_heuristics()

    # creating a list of tiles being checked and tiles done checking
    open_list = []
    closed_list = []

    # stages of pathfinding: run(
    searching = True
    connecting = False

    # running the pathfinding loop
    running = True
    while running:

        # checking for the escape key press
        for event in pygame.event.get():
                pressed = pygame.key.get_pressed()

                if pressed[pygame.K_ESCAPE]:
                    program_looping = False
                    running = False

        # going through the stages of pathfinding, searching and connecting
        if searching:
            pathfind()
        elif connecting:
            connect()

        # displaying the new visuals for pygame
        display()


        # if we're not searching and not pathfinding the means we are done
        if searching is False and connecting is False:
            running = False
            # resetting the start tile and goal tile back to null
            t.Tile.start_tile = t.Tile.goal_tile = None

            # printing the data recorded that's recorded into efficiency_data []
            print ('(sim #{}) (checked {}) (distance {}) (stored {})'\
                .format(simulation_count, check_count, path_count, len(closed_list) + len(open_list)))

            efficiency_data.append((check_count, path_count, len(closed_list) + len(open_list)))

            # moving sim count up and setting the data back to 0
            simulation_count += 1
            check_count = 0
            path_count = 0

            # checking if we're done running simulations
            if simulation_count > simulation_limit:
                program_looping = False
                Plotter.plot(efficiency_data)

            # sleeping for .5 seconds to admire the beauty of the pathfind when it's done
            time.sleep(0.5)