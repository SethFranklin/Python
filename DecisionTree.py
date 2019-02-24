
import enum
import math

class piece(enum.Enum):
	empty = 0
	red = 1
	black = 2

width = 7
height = 6

empty_board = []

for i in range(width * height):
	empty_board.append(piece.empty)

def print_board(b):
	a = 0
	for y in range(height):
		line = ""
		for x in range(width):
			a = b[(width * y) + x]
			if (a == piece.empty): line += " "
			elif (a == piece.red): line += "X"
			else: line += "0"
		print(line)

	line = ""
	for x in range(width):
		line += str(x + 1)
	print(line)

def check_win(b, x, y):

	check = b[(width * y) + x]

	# horizontal

	s = 1
	nx = x - 1
	ny = y

	while (s < 4 and nx >= 0 and b[(width * ny) + nx] == check):
		s += 1
		nx -= 1

	nx = x + 1

	while (s < 4 and nx < width and b[(width * ny) + nx] == check):
		s += 1
		nx += 1

	if (s >= 4): return check

	# vertical

	s = 1
	nx = x
	ny = y - 1

	while (s < 4 and ny >= 0 and b[(width * ny) + nx] == check):
		s += 1
		ny -= 1

	ny = y + 1

	while (s < 4 and ny < height and b[(width * ny) + nx] == check):
		s += 1
		ny += 1

	if (s >= 4): return check

	# y = x

	s = 1
	nx = x - 1
	ny = y - 1

	while (s < 4 and nx >= 0 and ny >= 0 and b[(width * ny) + nx] == check):
		s += 1
		nx -= 1
		ny -= 1

	nx = x + 1
	ny = y + 1

	while (s < 4 and nx < width and ny < height and b[(width * ny) + nx] == check):
		s += 1
		nx += 1
		ny += 1

	if (s >= 4): return check

	# y = -x

	s = 1
	nx = x + 1
	ny = y - 1

	while (s < 4 and nx < width and ny >= 0 and b[(width * ny) + nx] == check):
		s += 1
		nx += 1
		ny -= 1

	nx = x - 1
	ny = y + 1

	while (s < 4 and nx >= 0 and ny < height and b[(width * ny) + nx] == check):
		s += 1
		nx -= 1
		ny += 1

	if (s >= 4): return check

	return piece.empty

def check_full(b):
	for i in range(width * height):
		if (b[i] == piece.empty): return False
	return True

def place_piece(b, x):
	y = -1

	while (y + 1 < height and b[(width * (y + 1)) + x] == piece.empty): y += 1

	return y

class node:

	def __init__(self, board, depth, turnn):
		self.winner = piece.empty
		self.children = []
		if (depth > 0):
			for x in range(width):
				self.children.append(None)
				nb = board.copy()
				ny = place_piece(nb, x)
				nt = turnn
				if (ny >= 0):
					nb[(width * ny) + x] = turnn
					if (check_win(nb, x, ny) == turnn):
						if (depth == 5): print("win1", turnn)
						nnode = node(nb, -1, turnn)
						nnode.winner = turnn
						if (depth == 5): print("win2", turnn)
						self.children[x] = nnode
					else:
						if (nt == piece.red): nt = piece.black
						else: nt = piece.red
						if (depth == 5): print("switched:", nt)
						nnode = node(nb, depth - 1, nt)
						self.children[x] = nnode
		else:
			for x in range(width): self.children.append(None)

	def min(self, turnn, initial):
		def sub_min(nodee, iters):
			if (nodee.winner == turnn):
				return 22 - math.floor(iters / 2)
			elif (nodee.winner != piece.empty):
				return math.ceil(iters / 2) - 22
			else:
				mini = 999999
				for x in range(width):
					if (nodee.children[x] != None):
						nm = sub_min(nodee.children[x], iters + 1)
						if (nm < mini): mini = nm
				return mini
		moves = []
		for x in range(width):
			if (self.children[x] != None):
				print(x + 1, self.children[x].winner)
				moves.append(sub_min(self.children[x], initial + 1))
			else: moves.append(0)
		imin = 0
		cmin = moves[0]
		print("Mins:")
		print(1, moves[0])
		for x in range(1, width):
			print(x + 1, moves[x])
			if moves[x] < cmin:
				imin = x
				cmin = moves[x]
		return imin

print_board(empty_board)

game_on = True
turn = piece.red
x = 0
num_pieces = 1

while (game_on):
	if (turn == piece.red): # player red
		x = int(input("Place a piece: ")) - 1
	else: # decision tree black
		print("bot:", turn)
		tree = node(empty_board, 5, turn)
		x = tree.min(turn, num_pieces)
		print("Tree placed:", x)

	y = place_piece(empty_board, x)
	if (y >= 0 and x >= 0 and x < width):
			if (y >= 0): empty_board[(width * y) + x] = turn
			num_pieces += 1
			print_board(empty_board)
			if (turn == piece.red): turn = piece.black
			else: turn = piece.red
			if (check_win(empty_board, x, y) != piece.empty): game_on = False

print("Game over!")

# want while loop of finding mins and taking user input. user moves first