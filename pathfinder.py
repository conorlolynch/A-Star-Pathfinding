
import pygame as pg
import numpy as np
import math

pg.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
clock = pg.time.Clock()

# Handling all the font stuff
myfont = pg.font.SysFont('didot.ttc', 30, bold=False)

wall_text = myfont.render('wall', True, (0,0,0))
start_text = myfont.render('start', True, (0,0,0))
end_text = myfont.render('end', True, (0,0,0))
clear_screen_text = myfont.render('clear', True, (0,0,0))
findpath_text = myfont.render('find path', True, (0,0,0))




class Node():
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.g = -1
        self.h = -1
        self.f = -1
        self.parent = None

    def updateParent(self, parent):
        self.parent = parent

    def updateG(self, val):
        self.g = val

    def updateH(self, val):
        self.h = val

    def updateF(self, val):
        self.f = val

    def calculateF(self):
        self.f = self.h + self.g

    def getG(self):
        return self.g

    def getH(self):
        return self.h

    def getF(self):
        return self.f



class Button():
    def __init__(self, screen, id, xpos, ypos, width, height, button_colour, text, text_colour, text_x_padding, text_y_padding):
        self.screen = screen
        self.id = id
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.button_colour = button_colour
        self.text = text
        self.text_colour = text_colour
        self.text_x_padding = text_x_padding
        self.text_y_padding = text_y_padding
        self.highlight = False


    def highlightButton(self):
        self.highlight = True

    def unhighlightButton(self):
        self.highlight = False


    def checkClicked(self, mouse_x, mouse_y):
        if (mouse_x > self.xpos and mouse_x < (self.xpos + self.width)):
            if (mouse_y > self.ypos and mouse_y < (self.ypos + self.height)):
                return True

        return False


    def draw(self):
        # Draw the button
        pg.draw.rect(self.screen, self.button_colour, (self.xpos, self.ypos, self.width, self.height))

        # Draw outline if we are highlighting the button
        if (self.highlight):
            pg.draw.rect(self.screen, (0, 0, 0), (self.xpos, self.ypos, self.width, self.height), 3)  # width = 3

        # Write text on button
        screen.blit(self.text,(self.text_x_padding + self.xpos, self.text_y_padding + self.ypos))



class Grid():
    def __init__(self, screen, grid_length, grid_line_thickness, side_edge_thickness, bottom_edge_thickness, number_rows, number_cols, line_colour):
        self.screen = screen
        self.grid_length = grid_length
        self.grid_line_thickness = grid_line_thickness
        self.total_grid_size = self.grid_length + self.grid_line_thickness

        self.side_edge_thickness = side_edge_thickness
        self.bottom_edge_thickness = bottom_edge_thickness
        self.number_rows = int(number_rows) - 2
        self.number_cols = int(number_cols) - 2
        self.line_colour = line_colour

        self.wall_colour = (0, 0, 0)
        self.walls = []
        self.startPos = []
        self.endPos = []

        self.startPos = []
        self.startPos_colour = (0,0,155)

        self.endPos = []
        self.endPos_colour = (255,0,255)
        #self.endPos_colour = (255,255,0)

        self.open_list = []
        self.closed_list = []

        self.lastNode = None
        self.path = []
        self.pathColour = (0,255,255)


    def addWall(self, xpos, ypos):
        if [xpos, ypos] in self.walls:
            #print("Wall already added")
            return
        elif [xpos, ypos] in self.startPos:
            return
        elif [xpos, ypos] in self.endPos:
            return
        else:
            self.walls.append([xpos, ypos])


    def removeWall(self, xpos, ypos):
        for x, pos in enumerate(self.walls):
            if (pos == [xpos, ypos]):
                self.walls.pop(x)


    def addStartPos(self, xpos, ypos):
        self.startPos = [xpos, ypos]


    def removeStartPos(self):
        self.startPos = []


    def addEndPos(self, xpos, ypos):
        self.endPos = [xpos, ypos]


    def removeEndPos(self):
        self.endPos = []


    def convertPixelToIndex(self, x_pixel, y_pixel):
        # Round it to the closest multiple of 25 or (grid_length + grid_line_thickness)
        actual_x = math.floor((x_pixel - self.side_edge_thickness) / self.total_grid_size)
        actual_y = math.floor((y_pixel - self.side_edge_thickness) / self.total_grid_size)
        return actual_x, actual_y


    def drawEdges(self):
        # Draw all the edges along top and bottom of screen
        bottom_y = SCREEN_HEIGHT - self.bottom_edge_thickness - self.grid_length - self.grid_line_thickness
        for i in range(self.number_cols+2):
            pg.draw.rect(self.screen, (0,0,0), (i * 25, 0, self.grid_length+1, self.grid_length+1))
            pg.draw.rect(self.screen, (0,0,0), (i * 25, bottom_y, self.grid_length+1, self.grid_length+1))

        # Draw all the edges along left and right hand side of screen
        right_x = SCREEN_WIDTH - self.side_edge_thickness
        for i in range(self.number_rows+2):
            pg.draw.rect(self.screen, (0,0,0), (0, i * 25, self.grid_length+1, self.grid_length+1))
            pg.draw.rect(self.screen, (0,0,0), (right_x, i * 25, self.grid_length+1, self.grid_length+1))


    def drawGridLines(self):
        # Draw all the columns
        current_x = self.total_grid_size
        for x in range(0, int(self.number_cols)):
            pg.draw.rect(self.screen, self.line_colour, (current_x, 0, self.grid_line_thickness, SCREEN_HEIGHT-self.bottom_edge_thickness))
            current_x = current_x + self.grid_length + self.grid_line_thickness

        # Draw all the rows
        current_y = self.grid_length
        for y in range(0, int(self.number_rows)):
            pg.draw.rect(self.screen, self.line_colour, (self.total_grid_size, current_y, SCREEN_WIDTH, self.grid_line_thickness))
            current_y = current_y + self.grid_length + self.grid_line_thickness


    def drawWalls(self):
        if (len(self.walls) > 0):
            for pos in self.walls:
                adjusted_xpos = self.side_edge_thickness + 1 + (self.grid_length + self.grid_line_thickness) * pos[0]
                adjusted_ypos = self.side_edge_thickness + (self.grid_length + self.grid_line_thickness) * pos[1]

                #print("xpos: ",adjusted_xpos)

                pg.draw.rect(self.screen, self.wall_colour, (adjusted_xpos, adjusted_ypos, self.grid_length, self.grid_length))


    def drawStartPos(self):
        if self.startPos != []:
            x_pos = self.side_edge_thickness + 1 + (self.grid_length + self.grid_line_thickness) * self.startPos[0]
            y_pos = self.side_edge_thickness + (self.grid_length + self.grid_line_thickness) * self.startPos[1]

            pg.draw.rect(self.screen, self.startPos_colour, (x_pos, y_pos, self.grid_length, self.grid_length))


    def drawEndPos(self):
        if self.endPos != []:
            x_pos = self.side_edge_thickness + 1 + (self.grid_length + self.grid_line_thickness) * self.endPos[0]
            y_pos = self.side_edge_thickness + (self.grid_length + self.grid_line_thickness) * self.endPos[1]

            pg.draw.rect(self.screen, self.endPos_colour, (x_pos, y_pos, self.grid_length, self.grid_length))


    def drawOpenList(self):
        if (len(self.open_list) > 0):
            for pos in self.open_list:
                x_pos = self.side_edge_thickness + 1 + (self.grid_length + self.grid_line_thickness) * pos[0]
                y_pos = self.side_edge_thickness + (self.grid_length + self.grid_line_thickness) * pos[1]
                pg.draw.rect(self.screen, (0,255,0), (x_pos, y_pos, self.grid_length, self.grid_length))


    def drawClosedList(self):
        if (len(self.closed_list) > 0):
            for pos in self.closed_list:
                if (pos == self.startPos):
                    pass
                else:
                    x_pos = self.side_edge_thickness + 1 + (self.grid_length + self.grid_line_thickness) * pos[0]
                    y_pos = self.side_edge_thickness + (self.grid_length + self.grid_line_thickness) * pos[1]
                    pg.draw.rect(self.screen, (255,0,0), (x_pos, y_pos, self.grid_length, self.grid_length))


    def unpackNodes(self):
        while self.lastNode.parent != None:
            self.path.append([self.lastNode.xpos, self.lastNode.ypos])
            self.lastNode = self.lastNode.parent


    def drawPath(self):
        if (len(self.path) > 0):
            for pos in self.path:
                x_pos = self.side_edge_thickness + 1 + (self.grid_length + self.grid_line_thickness) * pos[0]
                y_pos = self.side_edge_thickness + (self.grid_length + self.grid_line_thickness) * pos[1]
                pg.draw.rect(self.screen, self.pathColour, (x_pos, y_pos, self.grid_length, self.grid_length))


    def drawTaskBar(self):
        pg.draw.rect(self.screen, (180,180,180), (0, SCREEN_HEIGHT-self.bottom_edge_thickness, SCREEN_WIDTH, self.bottom_edge_thickness))


def returnHeuristic(start_x, start_y, end_x, end_y):
    return (abs(start_x - end_x) + abs(start_y - end_y))



def a_star_algorithm(startPos, endPos, wallPositions, number_rows, number_cols, grid):

    open_list = []       # The set of nodes to be evaluated
    closed_list = []     # The set of nodes already evaluated
    node_array = np.zeros((number_cols, number_rows), dtype=object)

    # We want to populate the open_list with the starting node
    start_node = Node(startPos[0], startPos[1])
    end_node = Node(endPos[0], endPos[1])

    start_node.updateH(returnHeuristic(start_node.xpos, start_node.ypos, end_node.xpos, end_node.ypos))
    start_node.updateG(0)
    start_node.calculateF()

    open_list.append([start_node.xpos, start_node.ypos])
    node_array[start_node.xpos][start_node.ypos] = start_node

    end_node.updateH(0)
    end_node.updateG(returnHeuristic(end_node.xpos, end_node.ypos, start_node.xpos, start_node.ypos))
    end_node.calculateF()
    node_array[end_node.xpos][end_node.ypos] = end_node

    path_found = False

    while (not path_found):
        lowest_f = 9999
        current_node = None

        # Consider the node with the lowest f score in the open list
        index = 0
        for x, node_pos in enumerate(open_list):
            node = node_array[node_pos[0], node_pos[1]]

            if (node != 0):
                if (node.getF() < lowest_f):
                    lowest_f = node.getF()
                    current_node = node
                    index = x


        # Remove current node from open list
        try:
            open_list.pop(index)
        except IndexError:
            print("Path to end point could not be found")
            path_found = True
            return None
            break


        # Draw our progress
        grid.open_list = open_list
        grid.closed_list = closed_list
        grid.drawOpenList()
        grid.drawClosedList()
        pg.display.update()

        # If this node is our destination node
        if (current_node.getH() == 0):
            path_found = True
            return current_node

        else:
            # Put the current node in the closed list
            closed_list.append([current_node.xpos, current_node.ypos])

            # Look at all of its neighbors (up, below, left, right) and turn them into nodes
            neighbors = []

            # Up neighbor [x][y-1]
            if (current_node.ypos > 0):
                # Make sure there isnt a wall there
                if ( [current_node.xpos, current_node.ypos - 1] not in wallPositions):
                    neighbors.append([current_node.xpos, current_node.ypos - 1])

            # Right neighbor [x+1][y]
            if (current_node.xpos < number_cols-1):
                if ( [current_node.xpos + 1, current_node.ypos ] not in wallPositions):
                    neighbors.append([current_node.xpos + 1, current_node.ypos])

            # Below neighbor [x][y+1]
            if (current_node.ypos < number_rows-1):
                if ( [current_node.xpos, current_node.ypos + 1 ] not in wallPositions):
                    neighbors.append([current_node.xpos, current_node.ypos + 1])

            # Left neighbor [x-1][y]
            if (current_node.xpos > 0):
                if ( [current_node.xpos - 1, current_node.ypos] not in wallPositions):
                    neighbors.append([current_node.xpos - 1, current_node.ypos])


            #print("Neighbors to current node ->",[current_node.xpos, current_node.ypos],": ",neighbors)

            if (len(neighbors) > 0):
                # for each neighbor of the current node
                for neigh in neighbors:
                    # if neighbor is in closed list skip to next neighbour
                    if (neigh in closed_list):
                        continue

                    # We want to get the g distance for neighbor but first check if it exists as a node
                    g = -1
                    node = node_array[neigh[0]][neigh[1]]

                    if (node == 0):
                        # Node doesnt exist so we have to create it
                        temp_node = Node(neigh[0], neigh[1])
                        temp_node.updateH(returnHeuristic(temp_node.xpos, temp_node.ypos, end_node.xpos, end_node.ypos))
                        temp_node.updateG(current_node.getG() + 1)
                        temp_node.calculateF()
                        node_array[neigh[0]][neigh[1]] = temp_node

                        node = temp_node

                    g = node.getG()
                    # if new path to neighbor is shorter (lower g) OR neighbor is not in open:
                    if (node.getG() > (current_node.getG() + 1)  or (neigh not in open_list)):
                        node.updateG(current_node.getG() + 1)
                        node.calculateF()
                        node.updateParent(current_node)

                        # Add neighbor to open_list if its not already there
                        if (neigh not in open_list):
                            open_list.append(neigh)



def main():
    grid_length = 24
    grid_line_thickness = 1
    bottom_edge_thickness = 50
    side_edge_thickness = 25
    line_colour = (0, 0, 0)

    number_cols = SCREEN_WIDTH / (grid_length + grid_line_thickness)
    number_rows = (SCREEN_HEIGHT - bottom_edge_thickness)  / (grid_length + grid_line_thickness)

    grid = Grid(screen, grid_length, grid_line_thickness, side_edge_thickness, bottom_edge_thickness, number_rows, number_cols, line_colour)

    run = True
    draging = False
    deleting = False

    adding_walls = True
    adding_startpos = False
    adding_endpos = False

    button_array = []

    # Button for selecting walls to be placed
    button1 = Button(screen, id=1, xpos=20, ypos= SCREEN_HEIGHT-40, width=50, height=30, button_colour=(134,197,218),
                        text=wall_text,text_colour=(0,0,0), text_x_padding=2, text_y_padding=3)

    # Button for choosing where start point will be placed
    button2 = Button(screen, id=2, xpos=80, ypos= SCREEN_HEIGHT-40, width=50, height=30, button_colour=(134,197,218),
                        text=start_text,text_colour=(0,0,0), text_x_padding=2, text_y_padding=3)

    # Button for choosing where end point will be placed
    button3 = Button(screen, id=3, xpos=140, ypos= SCREEN_HEIGHT-40, width=50, height=30, button_colour=(134,197,218),
                        text=end_text,text_colour=(0,0,0), text_x_padding=2, text_y_padding=3)

    # Button for clearing the screen
    button4 = Button(screen, id=4, xpos=200, ypos= SCREEN_HEIGHT-40, width=60, height=30, button_colour=(255,128,0),
                        text=clear_screen_text,text_colour=(0,0,0), text_x_padding=2, text_y_padding=3)

    #134,197,218
    # Button for beginning the path finding algorithm
    button5 = Button(screen, id=5, xpos=300, ypos= SCREEN_HEIGHT-40, width=90, height=30, button_colour=(255,128,0),
                        text=findpath_text,text_colour=(0,0,0), text_x_padding=2, text_y_padding=3)

    button1.highlightButton()
    button_array.extend([button1, button2, button3, button4, button5])



    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    # This clears the screen
                    grid = Grid(screen, grid_length, grid_line_thickness, side_edge_thickness, bottom_edge_thickness, number_rows, number_cols, line_colour)

                    run = True
                    draging = False
                    deleting = False

                    adding_walls = True
                    adding_startpos = False
                    adding_endpos = False
                    button_array[0].highlightButton()
                    button_array[1].unhighlightButton()
                    button_array[2].unhighlightButton()


                if event.key == pg.K_s:
                    # This allows us to mark the start point
                    adding_startpos = True
                    adding_walls = False
                    adding_endpos = False
                    button_array[0].unhighlightButton()
                    button_array[1].highlightButton()
                    button_array[2].unhighlightButton()


                if event.key == pg.K_e:
                    # This allows us to mark the end point
                    adding_startpos = False
                    adding_walls = False
                    adding_endpos = True
                    button_array[0].unhighlightButton()
                    button_array[1].unhighlightButton()
                    button_array[2].highlightButton()


                if event.key == pg.K_w:
                    # This allows us to mark the walls
                    adding_startpos = False
                    adding_walls = True
                    adding_endpos = False
                    button_array[0].highlightButton()
                    button_array[1].unhighlightButton()
                    button_array[2].unhighlightButton()


                if event.key == pg.K_f:
                    # This begins the path finding algorithm
                    if (grid.startPos != [] and grid.endPos != []):
                        grid.lastNode = a_star_algorithm(grid.startPos, grid.endPos, grid.walls, grid.number_rows, grid.number_cols, grid)
                        if (grid.lastNode != None):
                            grid.unpackNodes()
                            #print("path found: ",grid.path)
                        print("Path Finding Ended")

            # Code below allows us to use mouse movement to move the 3d shapes around
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Get position of mouse click
                    mouse_x = mouse_x, mouse_y = event.pos
                    actual_x, actual_y = grid.convertPixelToIndex(mouse_x, mouse_y)

                    # Want to check if we have clicked on any of the buttons
                    for button in button_array:
                        if (button.checkClicked(mouse_x, mouse_y)):
                            if (button.id == 1):
                                # We clicked the add walls button
                                adding_walls = True
                                adding_startpos = False
                                adding_endpos = False
                                button_array[0].highlightButton()
                                button_array[1].unhighlightButton()
                                button_array[2].unhighlightButton()

                            elif (button.id == 2):
                                # Clicked the add startpoint button
                                adding_startpos = True
                                adding_walls = False
                                adding_endpos = False
                                button_array[0].unhighlightButton()
                                button_array[1].highlightButton()
                                button_array[2].unhighlightButton()

                            elif (button.id == 3):
                                # Clicked the add endpoint button
                                adding_startpos = False
                                adding_walls = False
                                adding_endpos = True
                                button_array[0].unhighlightButton()
                                button_array[1].unhighlightButton()
                                button_array[2].highlightButton()

                            elif (button.id == 4):
                                # Clicked the clear screen button
                                grid = Grid(screen, grid_length, grid_line_thickness, side_edge_thickness, bottom_edge_thickness, number_rows, number_cols, line_colour)
                                run = True
                                draging = False
                                deleting = False

                                adding_walls = True
                                adding_startpos = False
                                adding_endpos = False
                                button_array[0].highlightButton()
                                button_array[1].unhighlightButton()
                                button_array[2].unhighlightButton()

                            elif (button.id == 5):
                                # Clicked the find path button
                                # This begins the path finding algorithm
                                if (grid.startPos != [] and grid.endPos != []):
                                    grid.lastNode = a_star_algorithm(grid.startPos, grid.endPos, grid.walls, grid.number_rows, grid.number_cols, grid)
                                    if (grid.lastNode != None):
                                        grid.unpackNodes()
                                        #print("path found: ",grid.path)
                                    print("Path Finding Ended")

                            break


                    # If we are in placing walls mode
                    if (adding_walls):
                        draging = True
                        if (actual_x < grid.number_cols and actual_y < grid.number_rows):
                            grid.addWall(actual_x, actual_y)

                    # If we are in placing startpoint mode
                    elif (adding_startpos):
                        if (actual_x < grid.number_cols and actual_y < grid.number_rows):
                            grid.addStartPos(actual_x, actual_y)

                    # If we are in placing endpoint mode
                    elif (adding_endpos):
                        if (actual_x < grid.number_cols and actual_y < grid.number_rows):
                            grid.addEndPos(actual_x, actual_y)


                if event.button == 3:
                    deleting = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    draging = False
                if event.button == 3:
                    deleting = False
                    mouse_x, mouse_y = event.pos
                    actual_x, actual_y = grid.convertPixelToIndex(mouse_x, mouse_y)

                    if [actual_x, actual_y] == grid.startPos:
                        grid.removeStartPos()

                    if [actual_x, actual_y] == grid.endPos:
                        grid.removeEndPos()

            elif event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                actual_x, actual_y = grid.convertPixelToIndex(mouse_x, mouse_y)

                if (actual_x < grid.number_cols and actual_y < grid.number_rows):
                    # This is how we add walls
                    if draging:
                        grid.addWall(actual_x, actual_y)

                    # This is how we remove walls
                    if deleting:
                        grid.removeWall(actual_x, actual_y)



        #screen.fill((255,255,255))
        screen.fill((211,211,211))
        grid.drawGridLines()
        grid.drawEdges()
        grid.drawWalls()
        grid.drawOpenList()
        grid.drawClosedList()
        grid.drawPath()
        grid.drawStartPos()
        grid.drawEndPos()

        # Draw the taskbar background
        grid.drawTaskBar()

        # Draw all UI buttons
        for button in button_array:
            button.draw()

        clock.tick(30)
        pg.display.update()

main()

# will use pygame
# will use pathfinding a* algorithm
