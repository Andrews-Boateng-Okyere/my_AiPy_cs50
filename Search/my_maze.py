import sys

# Node object
class Node():
	def __init__(self, state, parent, action):
		self.state = state
		self.parent = parent
		self.action = action

# Frontier object

class Frontier():
	def __init__(self):
		self.frontier = []

	# method for adding nodes to frontier
	def add(self,node):
		self.frontier.append(node)

	# method to check if a node is in frontier is in a particular state -> Truthy
	def contains_state(self, state):
		return any(node.state == state for node in self.frontier)
	
	# method to check if frontier is empty -> Truth value
	def empty(self):
		return len(self.frontier) == 0


# note that removal of nodes or object in our container makes the difference btn
# a stack type container and a queue type


class StackFrontier(Frontier):

	def remove(self):
		if self.empty():
			raise Exception("Empty frontier")
		else:
			node = self.frontier[-1]
			self.frontier = self.frontier[:-1]
		return node

class QueueFrontier(Frontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty frontier")
		else:
			node = self.frontier[0]
			self.frontier = self.frontier[1:]
		return node


# lets define our maze object
class Maze():
	
	# Initialisation: filename shd be dir of the file
	def __init__(self, filename):
	
		# read file and close it
		with open(filename, 'r') as f:
			contents = f.read()
		
		if contents.count("A") != 1:
			raise Exception("maze must have exactly one start point")
		if contents.count("B") != 1:
			raise Exception("maze must have exactly one goal")

		# Determine height and width of maze
		contents = contents.splitlines()
		self.height = len(contents)
		self.width = max([len(line) for line in contents])

		# keep track of walls
		self.walls = []
		for i in range(self.height):
			row = []
			for j in range(self.width):
				try:
					if contents[i][j] == "A":
						self.start = (i, j)
					elif contents[i][j] == "B":
						self.goal = (i,j)
					elif contents[i][j] == " ":
						row.append(False)
					else:
						row.append(True)
				except IndexError:
					row.append(False)
			self.walls.append(row)
		
		self.solution = None

	def print(self):
		solution = self.solution[1] if self.solution is not None else None
		print()
		for i, row in enumerate(self.walls):
			for j, col in enumerate(row):
				if col:
					print(" ", end="")
				elif (i,j) == self.start:
					print("A", end="")
				elif (i,j) == self.goal:
					print("B", end="")
				elif solution is not None and (i,j) in solution:
					print('*', end="")
			print()
		print()

	
	def neighbors(self, state):
		row, col = state
		candidates = [
			("up", (row-1, col)),
			("down", (row+1, col)),
			("left", (row, col-1)),
			("right", (row, col+1))
		]

		result = []
		for action, (r, c) in candidates:
			if 0 <=r< self.height and 0 <= c < self.width and not self.walls[r][c]:
				result.append((action, (r,c)))
		return result


	def solve(self):
		"""  Finds a solution to maze, if one exists."""
		# keep track of number of states explored
		self.num_explored = 0

		# Initialize frontier to just the starting position
		start = Node(state=self.start, parent=None, action=None)
		frontier = StackFrontier()
		frontier.add(start)

		# Initialize an empty explored set
		self.explored = set()

		# Keep looping until solution found
		while True:

			# if nothing left in frontier no path
			if frontier.empty():
				raise Exception("no solution")

			# choose a node from the frontier
			node = frontier.remove()
			self.num_explored +=1

			# If node is the goal, then we have a solution
			if node.state == self.goal:
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions, cells)
				return

			# Mark node as explored
			