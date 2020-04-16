import tkinter as tk
import pygame
import re
import time


class Board():
	def __init__(self, row, col):
		self.grid = []

		self.row = row
		self.col = col

		self.initGrid()

	def initGrid(self):
		for r in range(self.row):
			self.grid.append([])
			for c in range(self.col):
				self.grid[r].append(0)

	def adjust(self, pos, feature):

		if feature == "empty":
			self.grid[pos[0]][pos[1]] = 0

		elif feature == "blocked":
			self.grid[pos[0]][pos[1]] = 1

		elif feature == "start":
			self.grid[pos[0]][pos[1]] = 2

		elif feature == "end":
			self.grid[pos[0]][pos[1]] = 3

		elif feature == "open_list":
			self.grid[pos[0]][pos[1]] = 4

		elif feature == "closed_list":
			self.grid[pos[0]][pos[1]] = 5

		elif feature == "path":
			self.grid[pos[0]][pos[1]] = 6




class UserInput(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self, None)
		self.initialize()

	def initialize(self):
		self.label1 = tk.Label(self, text="Start Position : ").grid(row=0)
		self.label2 = tk.Label(self, text="End Position : ").grid(row=1)

		self.e1 = tk.Entry(self)
		self.e2 = tk.Entry(self)

		self.e1.grid(row = 0, column = 1)
		self.e2.grid(row = 1, column = 1)

		self.start = None
		self.end = None


		self.button = tk.Button(self, text='Go', command=self.submit).grid(row=3, column=0, sticky=tk.W, pady=4)

	def submit(self):
		self.start = self.e1.get()
		self.end = self.e2.get()

		self.quit()

class Node():
	def __init__(self, position, parent = None):
		self.position = position
		self.parent = parent

		self.f = 0
		self.g = 0#distance between the parent and current_node
		self.h = 0#distance between the end_node and current_node	


def gameLoop():
	board = Board(row = 10, col= 10)

	ui = UserInput()
	ui.mainloop()

	start = re.split(',', ui.start)
	end = re.split(',', ui.end)

	start = [int(start[0]), int(start[1])]
	end = [int(end[0]), int(end[1])]



	#-------Colors
	white = (255,255,255)
	black = (0,0,0)
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	yellow = (255,255,0)
	brown = (139,69,19)


	#------GRID CONSTANTS
	WIDTH = 30
	HEIGHT = 30
	AMOUNT = 30
	MARGIN = 1
	
	#separate by comma
	board = Board(AMOUNT,AMOUNT)


	board.adjust(start, "start")
	board.adjust(end, "end")


	open_list = []
	closed_list = []

	start_node = Node(start)
	end_node = Node(end)

	open_list.append(start_node)

	pygame.init()
	clock = pygame.time.Clock()


	screen = pygame.display.set_mode((WIDTH * AMOUNT + (AMOUNT + 1) * MARGIN, HEIGHT * AMOUNT + (AMOUNT + 1) * MARGIN))

	counter = 0
	execute = False
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0] == 1:
				xPos = pygame.mouse.get_pos()[0] // (MARGIN+WIDTH)
				yPos = pygame.mouse.get_pos()[1] // (MARGIN+HEIGHT)

				board.adjust((xPos, yPos), "blocked")

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if execute == False:
						execute = True



#-----------------------------WHEN USER WANTS TO EXECUTE A* ALGORITHM----------------------------------------------
		if execute:
			current_node = open_list[0]
			current_index = 0
			for index, node in enumerate(open_list):
				if node.f < current_node.f:
					current_node = node
					current_index = index


			open_list.pop(current_index)
			closed_list.append(current_node)

			board.adjust(current_node.position, "closed_list")



			if current_node.position[0] == end_node.position[0] and current_node.position[1] == end_node.position[1] :
				
				while current_node != None:
					board.adjust(current_node.position, "path")

					current_node = current_node.parent

				execute = False
					


			children = []
			#start creating childs
			
		if execute:
		
			for direction in [[0,1], [0,-1], [1,0], [-1,0], [1,1], [-1,-1], [1,-1], [-1,1]]:
				new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])


				test = 0
				for open_node in open_list:
					if open_node.position == new_position:
						test = 1
						break
				if test == 1:
					continue


				#if out of range
				if new_position[0] > len(board.grid) - 1 or new_position[0] < 0 or new_position[1] > len(board.grid[0]) -1 or new_position[1] < 0:
					continue

				#if it is blocked
				if board.grid[new_position[0]][new_position[1]] == 1:
					continue


				#if the position is in the closed node
				test = 0
				for closed_node in closed_list:
					if new_position == closed_node.position:
						test = 1
						break

				if test == 1:
					continue


				new_node = Node(new_position, current_node)
				children.append(new_node)


			


			for child in children:
				#if it is in the open list and has a lower g cost


				child.g = ((child.position[0] - current_node.position[0])**2   +    (child.position[1] - current_node.position[1])**2) *10
				child.h = ((child.position[0] - end_node.position[0])**2   +    (child.position[1] - end_node.position[1])**2) *10

				child.f = child.g + child.h


				open_list.append(child)

				board.adjust(child.position, "open_list")


#------------------------------------------------------------------------------------------



		color = white
		for row in range(AMOUNT):
			for column in range(AMOUNT):
				color = white

				if board.grid[column][row] == 1:
					color = black
				elif board.grid[column][row] == 2:
					color = green
				elif board.grid[column][row] == 3:
					color = red
				elif board.grid[column][row] == 4:
					color = yellow
				elif board.grid[column][row] == 5:
					color = brown
				elif board.grid[column][row] == 6:
					color = blue 


				pygame.draw.rect(screen, color, ((MARGIN+WIDTH)*column + MARGIN, (MARGIN + HEIGHT)*row + MARGIN, WIDTH, HEIGHT))

		pygame.display.update()
		clock.tick(1000)



	pygame.quit()



if __name__ == "__main__":
	
	gameLoop()