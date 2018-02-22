#
# Code by Footleg and under GNU GPL3 license
#

#
# Create Rooms
#

from mine import *
import mcpi.block as mcb
import sys, time, mazegen

def createRoomShell(x,y,z,block):
	#mc.postToChat("Creating room at {}, {}, {}".format(x,y,z) )

	#Fill Room area
	mc.setBlocks(x, y, z, x+12, y+4, z-12, block)
	
	#Clear inside space
	mc.setBlocks(x+1, y+1, z-1, x+11, y+3, z-11, mcb.AIR)
	
	#Mark corners and edges
	markEdges(x,y,z)
	markEdges(x,y+4,z)
	

def markEdges(x,y,z):
	#Corners
	mc.setBlock(x, y, z, 35, 1)
	mc.setBlock(x, y, z-12, 35, 1)
	mc.setBlock(x+12, y, z, 35, 1)
	mc.setBlock(x+12, y, z-12, 35, 1)
	
	#Mid-Edges
	mc.setBlock(x+6, y, z, 35, 2)
	mc.setBlock(x+6, y, z-12, 35, 2)
	mc.setBlock(x, y, z-6, 35, 2)
	mc.setBlock(x+12, y, z-6, 35, 2)
	
	#Edges
	for i in range(1,7):
		mc.setBlock(x, y, z-2*i+1, 35, 3)
		mc.setBlock(x+12, y, z-2*i+1, 35, 3)
		mc.setBlock(x+2*i-1, y, z, 35, 3)
		mc.setBlock(x+2*i-1, y, z-12, 35, 3)


def createRoomTypeN9S3(x,y,z,walls):
	createRoomShell(x,y,z,walls)
	#Create doorways (z-12 = N wall; z = S wall)
	mc.setBlock(x+9, y+1, z-12, mcb.AIR)
	mc.setBlock(x+9, y+2, z-12, mcb.AIR)
	mc.setBlock(x+3, y+1, z, mcb.AIR)
	mc.setBlock(x+3, y+2, z, mcb.AIR)
	
	
def removeWallN(x,y,z):
	#Create doorways (z-12 = N wall; z = S wall)
	mc.setBlocks(x+1, y+1, z-12, x+11, y+3, z-12, mcb.AIR)
	
	
def removeWallS(x,y,z):
	#Create doorways (z-12 = N wall; z = S wall)
	mc.setBlocks(x+1, y+1, z, x+11, y+3, z, mcb.AIR)
	
	
def removeWallE(x,y,z):
	#Create doorways (x = W wall; x+12 = E wall)
	mc.setBlocks(x+12, y+1, z-1, x+12, y+3, z-11, mcb.AIR)
	
	
def removeWallW(x,y,z):
	#Create doorways (x = W wall; x+12 = E wall)
	mc.setBlocks(x, y+1, z-1, x, y+3, z-11, mcb.AIR)
	
	
def decorateRoomTorches(x,y,z):
	#Place torches
	mc.setBlock(x+6, y+2, z-1, 50, 4)
	mc.setBlock(x+6, y+2, z-11, 50, 3)
	mc.setBlock(x+1, y+2, z-6, 50, 1)
	mc.setBlock(x+11, y+2, z-6, 50, 2)
	

def showMazeInChat(mz):
	# the upper wall first
	outtable = '.'+mz.cols*'_.'
	mc.postToChat(outtable)
	for i in range(mz.rows):
		outtable = '|'

		for j in range(mz.cols):
			if mz.cells[i][j][mz.BOTTOM]:
				outtable += '_'
			else:
				outtable += '  '
			if mz.cells[i][j][mz.RIGHT]:
				outtable += '|'
			else:
				outtable += '.'

		mc.postToChat(outtable)


#Main script starts here
mc = Minecraft()

#Get dimensions from command line arguments, or use defaults
totE = 5
totN = 7
totH = 1

if len(sys.argv) > 1:
	totE = int(sys.argv[1])
	if len(sys.argv) > 2:
		totN = int(sys.argv[2])
		if len(sys.argv) > 2:
			totH = int(sys.argv[3])


#Start creating rooms
mc.postToChat("Creating East x North x Height: {} x {} x {} rooms...".format(totE,totN,totH) )

#Set start point
pos = mc.player.getTilePos()
x = pos.x
y = pos.y - 15
z = pos.z - 6

#Clear space
rmsp = 12
mc.setBlocks(x-5, y, z+5, x+rmsp*totE+5, y+4*totH+5, z-rmsp*totN-5, mcb.AIR)
#time.sleep(5)

#Create rooms grid
for n in range(totN):
	zp = z-n*rmsp
	for e in range(totE):
		xp = x+e*rmsp
		for h in range(totH):
			yp = y+h*4
			createRoomShell(xp,yp,zp,mcb.WOOD_PLANKS)
			#debug: remove roof
			mc.setBlocks(xp, yp+4, zp, xp+12, yp+4, zp-12, mcb.AIR)


#Generate maze for each level
mazes = []
for h in range(totH):
        maze = mazegen.maze(totE,totN)
        maze.generate(1,1)
        mazes.append( maze )
        showMazeInChat(mazes[h])

#Decorate the rooms
for n in range(totN):
	zp = z-n*rmsp
	for e in range(totE):
		xp = x+e*rmsp
		for h in range(totH):
			yp = y+h*4
			mz = mazes[h]
			if mz.cells[totN-1-n][e][mz.BOTTOM] == False:
				removeWallS(xp,yp,zp)
			if mz.cells[totN-1-n][e][mz.RIGHT] == False:
				removeWallE(xp,yp,zp)
			


mc.postToChat("All done.")
