from Apps.match.models import Match, Match_Castling_Options

class Piece():
	def __init__(self, color, source, target, board, match_id = None):
		self.color = color
		self.source = source
		self.target = target
		self.cols = 'abcdefgh'
		self.board = board
		if (match_id != None):
			self.match = Match.objects.get(id = match_id)
		else:
			self.match = None

	def get_attack_by_piece(self, colin, rowin, pos):
		column = pos[0]
		row = pos[1]
		icol = self.cols.index(column) + colin
		irow = int(row) + rowin

		attack_zone = []

		if (icol > -1 and irow > -1):
			try:
				attack_zone.append("{}{}".format(self.cols[icol],irow))
			except:
				pass

		return attack_zone

	def is_valid_move(self):
		posible = self.get_attacks('source')
		for i in posible:
			if (self.target in i):
				return True
		return False

	def get_attacks(self, pos):
		pass

class Pawn(Piece):
	def is_valid_move(self):
		board = list(self.board.keys())
		board.sort()
		board.remove(self.source)

		cond1 = self.target[0] == self.source[0]
		if (self.color == 'w'):
			factor = 1
			valid_for_2 = 2
		else:
			factor = -1
			valid_for_2 = 7

		cond2 = int(self.target[1]) == int(self.source[1]) + factor
		cond3 = int(self.source[1]) == valid_for_2 and int(self.target[1]) == int(self.source[1]) + (2*factor)
		cond4 = "{}{}".format(self.target[0],int(self.target[1])-factor) not in board

		return cond1 and (cond2 or (cond3 and cond4))

	def get_attacks(self):
		attack_zone = []
		if (self.color == 'w'):
			if (int(self.target[1]) == 8):
				return 'Promote'
			else:
				attack_zone.append(self.get_attack_by_piece(-1, 1, self.target))
				attack_zone.append(self.get_attack_by_piece( 1, 1, self.target))
		else:
			if (int(self.target[1]) == 1):
				return 'Promote'
			else:
				attack_zone.append(self.get_attack_by_piece(-1, -1, self.target))
				attack_zone.append(self.get_attack_by_piece( 1, -1, self.target))

		return attack_zone	

class Knight(Piece):
	def get_attacks(self, pos = 'target'):
		attack_zone = []
		if (pos == 'target'):
			pos = self.target
		else:
			pos = self.source
		attack_zone.append(self.get_attack_by_piece(-1, 2, pos))
		attack_zone.append(self.get_attack_by_piece( 1, 2, pos))
		attack_zone.append(self.get_attack_by_piece(-2, 1, pos))
		attack_zone.append(self.get_attack_by_piece( 2, 1, pos))

		attack_zone.append(self.get_attack_by_piece(-1, -2, pos))
		attack_zone.append(self.get_attack_by_piece( 1, -2, pos))
		attack_zone.append(self.get_attack_by_piece(-2, -1, pos))
		attack_zone.append(self.get_attack_by_piece( 2, -1, pos))

		return attack_zone	

class Rock(Piece):
	def get_attack_by_piece(self, pos):
		board = list(self.board.keys())
		board.sort()
		board.remove(self.source)
		
		cols = self.cols.index(pos[0])
		rows = int(pos[1])

		attack_zone = []

		rangesv = [range(rows+1, 9), range(1, rows)[::-1]]
		for r in rangesv:
			l = []
			for i in r:
				aux = "{}{}".format(pos[0],i)
				l.append(aux)
				if (aux in board):
					break
			if (len(l) > 0):
				attack_zone.append(l)

		rangesh = [range(cols+1, 8), range(0, cols)[::-1]]
		for r in rangesh:
			l = []
			for i in r:
				aux = "{}{}".format(self.cols[i], rows)
				l.append(aux)
				if (aux in board):
					break
			if (len(l) > 0):
				attack_zone.append(l)
		
		return attack_zone
	
	def get_attacks(self, pos = 'target'):
		if (pos == 'target'):
			pos = self.target
		else:
			pos = self.source
		
		attack_zone = self.get_attack_by_piece(pos)
		return attack_zone

class Bishop(Piece):
	def get_attack_by_piece(self, pos):
		board = list(self.board.keys())
		board.sort()
		board.remove(self.source)
		
		cols = self.cols.index(pos[0])
		rows = int(pos[1])

		attack_zone = []

		l1 = []
		index = rows + 1
		for i in range(cols+1, 8):
			if (index <= 8):
				aux = '{}{}'.format(self.cols[i],index)
				l1.append(aux)
				if (aux in board):
					break
			index += 1

		if (len(l1) > 0):
			attack_zone.append(l1)

		l2 = []
		index2 = rows - 1
		for i in range(cols+1, 8):
			if (index2 >= 1):
				aux = '{}{}'.format(self.cols[i],index2)
				l2.append(aux)
				if (aux in board):
					break
			index2 -= 1
			
		if (len(l2) > 0):
			attack_zone.append(l2)

		l3 =[]
		index3 = rows + 1
		for i in range(0, cols)[::-1]:
			if (index3 <= 8):
				aux = '{}{}'.format(self.cols[i],index3)
				l3.append(aux)
				if (aux in board):
					break
			index3 += 1

		if (len(l3) > 0):
			attack_zone.append(l3)

		l4 =[]
		index4 = rows - 1
		for i in range(0, cols)[::-1]:
			if (index4 >= 1):
				aux = '{}{}'.format(self.cols[i],index4)
				l4.append(aux)
				if (aux in board):
					break
			index4 -= 1

		if (len(l4) > 0):
			attack_zone.append(l4)

		return attack_zone

	def get_attacks(self, pos = 'target'):
		if (pos == 'target'):
			pos = self.target
		else:
			pos = self.source
		attack_zone = self.get_attack_by_piece(pos)
		return attack_zone

class Queen(Piece):
	def is_valid_move(self):
		self.b = Bishop(self.color, self.source, self.target, self.board)
		self.r = Rock(self.color, self.source, self.target, self.board)
		
		b = False
		posible = self.b.get_attacks('source')
		for i in posible:
			if (self.target in i):
				b = True

		r = False
		posible = self.r.get_attacks('source')
		for i in posible:
			if (self.target in i):
				r = True

		return (b or r)
	
	def get_attacks(self, pos = 'target'):
		return self.b.get_attacks() + self.r.get_attacks()

class King(Piece):

	def is_valid_move(self):
		board = list(self.board.keys())
		board.sort()
		board.remove(self.source)
		self.castling_try = False
		self.rock_castling_source = False
		self.rock_castling_target = False

		posible = self.get_attacks('source')
		for i in posible:
			if (self.target in i):
				return True

		castling_type = {'w':['g1','c1'], 'b':['g8','c8']}
		castling_try = self.target in castling_type[self.color]

		if (castling_try):
			self.castling_try = True
			initial_pos   = {'w':['e1'], 'b':['e8']}
			empty_require = {'g1':['f1'],'c1':['d1', 'b1'],'g8':['f8'],'c8':['d8', 'b8']}
			rock_require =  {'g1':'h1','c1':'a1','g8':'h8','c8':'a8'}

			king_inital = self.source in initial_pos[self.color]
			self.rock_castling_target = empty_require[self.target][0]
			
			empty_squares = not (empty_require[self.target][0] in board or empty_require[self.target][-1] in board)
			rock_square = False
			
			if (rock_require[self.target] in board):
				rock_square = self.board[rock_require[self.target]] == self.color + 'R'
				self.rock_castling_source = rock_require[self.target]

			if (self.target[0] == 'g'):
				type_castl = 'sort'
			else:
				type_castl = 'large'

			castling = Match_Castling_Options.objects.filter(
				match_id = self.match
			)

			if (castling.exists()):
				for e in castling:
					if (self.color == 'b' and type_castl == 'large' and e.black_large == False):
						#print ("Enroque {} {}".format(type_castl, 'black'),e.black_large)
						#if (e.black_large == False):
						return False
					elif (self.color == 'b' and type_castl == 'sort' and e.black_sort == False):
						#print ("Enroque {} {}".format(type_castl, 'black'),e.black_sort)
						#if (e.black_sort == False):
						return False
					if (self.color == 'w' and type_castl == 'large' and e.white_large == False):
						#print ("Enroque {} {}".format(type_castl, 'white'),e.white_large)
						#if (e.white_large == False):
						return False
					elif (self.color == 'w' and type_castl == 'sort' and e.white_sort == False):
						#print ("Enroque {} {}".format(type_castl, 'white'),e.white_sort)
						#if (e.white_sort == False):
						return False	
			else:
				if (self.color == 'b'):
					castling = Match_Castling_Options.objects.create(
						match_id = self.match,
						black_large = False,
						black_sort  = False
					)
				else:
					castling = Match_Castling_Options.objects.create(
						match_id = self.match,
						white_large = False,
						white_sort  = False
					)
			
			if (king_inital and empty_squares and rock_square):
				#print ("Intento de Enroque de {} a {}".format(self.source, self.target))
				return True
			#else:
			#	print ("Enroque Fallido")

		return False

	def get_attacks(self, pos = 'target'):
		attack_zone = []
		if (pos == 'target'):
			pos = self.target
		else:
			pos = self.source
		attack_zone = self.get_attack_by_piece(pos)
		return attack_zone

	def get_attack_by_piece(self, pos):
		board = list(self.board.keys())
		board.sort()
		board.remove(self.source)
		
		cols = self.cols.index(pos[0])
		rows = int(pos[1])

		attack_zone = []

		posibles = [
			[cols+1, rows+1], [cols+1, rows], [cols+1, rows-1],
			[cols-1, rows+1], [cols-1, rows], [cols-1, rows-1],
			[cols, rows+1], [cols, rows-1],
		]

		for i in posibles:
			try:
				if (i[1] in range(1,9)):
					aux = "{}{}".format(self.cols[i[0]], i[1])
					attack_zone.append([aux])
			except:
				None
		''' PRINT '''

		if (self.castling_try == True and self.rock_castling_target != False and self.rock_castling_source != False):
			rock = Rock(self.color, self.rock_castling_source, self.rock_castling_target, self.board)
			rock_attack = rock.get_attacks()
			attack_zone += rock_attack
			#print ("Ataque de la torre ", rock_attack)

		#print ("Rey ataca las casillas: ", attack_zone)
		return attack_zone

class Move_Validator:
	def __init__(self, source, target, piece, board_fen):
		self.source = source
		self.target = target
		self.board_fen = board_fen
		self.piece = piece
		self.board = self.board_result = self.change_notation()

	def __repr__(self):
		#return "{} moves from {} to {}".format(self.piece,self.source,self.target)
		piece = self.piece[1]
		if (self.piece[1] == 'P'):
			piece = ''
		return "{}{}".format(piece, self.target)

	def change_notation(self):
		board = {}
		col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
		fila = 8
		for i in self.board_fen.split('/'):
			index = 0
			for p in i:
				if (p.isdigit()):
					index += int(p)
				else:
					if (p.isupper()):
						color = 'w'
					else:
						color = 'b'
					board["{}{}".format(col[index],fila)] = "{}{}".format(color,p.upper())
					index += 1
			fila -= 1
		return board

	def validate(self, promote_val = False, match_id = None):
		if (self.piece[1] == 'P'):
			piece = Pawn(self.piece[0], self.source, self.target, self.board)
		if (self.piece[1] == 'N'):
			piece = Knight(self.piece[0], self.source, self.target, self.board)
		if (self.piece[1] == 'R'):
			piece = Rock(self.piece[0], self.source, self.target, self.board)
		if (self.piece[1] == 'B'):
			piece = Bishop(self.piece[0], self.source, self.target, self.board)
		if (self.piece[1] == 'Q'):
			piece = Queen(self.piece[0], self.source, self.target, self.board)
		if (self.piece[1] == 'K'):
			piece = King(self.piece[0], self.source, self.target, self.board, match_id)

		attacks = None
		valid = piece.is_valid_move()

		if (promote_val):
			valid = True
			
		wins = False

		if (valid):
			attacks = piece.get_attacks()

			del self.board_result[self.source]
			self.board_result[self.target] = self.piece

			if (piece.match != None):
				if (piece.castling_try == True and piece.rock_castling_target != False and piece.rock_castling_source != False):
					print (piece.rock_castling_source, self.board_result)
					del self.board_result[piece.rock_castling_source]
					self.board_result[piece.rock_castling_target] = piece.color + 'R'

			if (attacks != 'Promote'):
				for i in attacks:
					for j in i:
						if (j in self.board.keys()):
							if piece.color == 'w':
								self.board_result[j] = self.board_result[j].replace('b', 'w')
								if (self.piece[1] not in ('P', 'N')):
									break
							else:
								self.board_result[j] = self.board_result[j].replace('w', 'b')
								if (self.piece[1] not in ('P', 'N')):
									break
				
		return valid, attacks, self.board_result, wins
