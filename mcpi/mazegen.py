#!/usr/bin/env python3

# Copyright (c) 2018 Paul Fretwell
# Author: @drfootleg

import random


class maze:
    """ Class to generate a 2D maze. The maze consists of a 2D grid of cells which
        can have walls on any of their 4 sides. As they are in a grid, we only actually
        need to store the wall information for two of the sides of each cell to capture
        all the information to define the grid. In this implementation, the right and bottom
        wall is stored. In order to generate the maze we also need to track whether a cell
        has been visited or not.
    """
    
    #Constants to define positions of items in the cells array
    RIGHT  = 0
    BOTTOM = 1
    
    def __init__(self, cols, rows):
        """ Constructor requires the number of rows and columns in the maze to be specified
        """
        self.rows = rows
        self.cols = cols
        self.cells = []
        
        #Create initial 2D array of cells with all walls defined
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append([True,True])
            self.cells.append(row)
            
            
    def generate(self,startCol,startRow):
        """ Create a maze using a depth first search algorithm.
            Starting from the specified start coordinates it randomly knocks down walls
            between the active cell and one of the unvisited neighbouring cells. The cell
            through the removed wall then becomes the active cell. The path traversed is stored
            in a stack as the grid of cells is traversed. Each cell is flagged as visited as it
            becomes the active cell. This process continues until there are no unvisited cells
            neighbouring the active cell. Then the algorithm back tracks along the traversed path
            looking for any neighbouring unvisited cells as it goes. Whenever an unvisited cell is
            found then the path can extend again through that cell. This continues until there are no
            remaining cells in the stored path (at which point every cell has been visited and the maze
            is complete.
        """
        
        #Start by creating a 2D array to track which cells have been visited
        visited = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(False)
            visited.append(row)
        
        #Start path with specified start cell
        path = [[startCol-1,startRow-1]]
        
        #Set active cell to last cell in path and mark it as visited
        activeCell = path[len(path)-1]
        visited[activeCell[1]][activeCell[0]] = True
        
        #Set random order to select walls to test
        order = [0]
        for i in range(1,4):
            pos = random.randint(0,i)
            order.insert(pos,i)
                
        #Check neighbouring cells in random order to find an unvisited neighbour
        nextCell = -1
        for i in range(4):
            row = activeCell[1]
            col = activeCell[0]
            #Get position of neighbour to test
            if order[i] == 0:
                row -=1
            elif order[i] == 1:
                col +=1
            elif order[i] == 2:
                row +=1
            else:
                col -=1
                
            #Check neighbour is in bounds of grid and not visited
            if (0 <= row < self.rows) and (0 <= col <= self.cols):
                if visited[row][col] == False:
                    nextCell = order[i]
                    break
        
        if nextCell >= 0:
            #Remove wall
            if nextCell == 0:
                self.cells[row][col][self.BOTTOM] = False
            elif nextCell == 1:
                self.cells[activeCell[1]][activeCell[0]][self.RIGHT] = False
            elif nextCell == 2:
                self.cells[activeCell[1]][activeCell[0]][self.BOTTOM] = False
            else:
                self.cells[row][col][self.RIGHT] = False
            #Add next cell to end of the path
            path.append([col,row])
        else:
            #Dead end reached, so backtrack down path
            path.remove[len(path)-1]
            

    def print(self):
        for r in range(-1,self.rows):
            if r == -1:
                row = "."
            else:
                row = "|"
            for c in range(self.cols):
                if r == -1:
                    row += "_."
                else:
                    if self.cells[r][c][self.BOTTOM]:
                        row += "_"
                    else:
                        row += " "
                    if self.cells[r][c][self.RIGHT]:
                        row += "|"
                    else:
                        row += "."
                        
            print(row)


mz = maze(3,3)
mz.generate(2,2)
mz.print()
