import numpy as np
import pickle
from computational_geometry_functions import *

BOARD_ROWS = 4
BOARD_COLS = 8


class State:
	def __init__(self,p1,p2):
		self.board = np.zeros((BOARD_ROWS*BOARD_COLS))
		self.p1 = p1
		self.p2 = p2 
		self.points = []
		self.forbidden_points = []
		for i in range(BOARD_ROWS):
			for j in range(BOARD_COLS):
				self.points.append(Point(100+j*30,100+i*30))
				self.forbidden_points.append(False)
		self.triangles = []
		self.is_end = False 
		self.board_hash = None 
		self.player_symbol = 1
		self.counter = 0
		self.player_turn = False

	def get_hash(self):
		self.board_hash = str(self.board)
		return self.board_hash

	def find_intersection_for_triangle(self, triangle: Triangle):

		for i in range(len(self.triangles)):
			if(intersect_triangles(triangle,self.triangles[i])):
				return True 

		return False

	def find_forbidden_points(self,first_point: int, second_point: int):
		first, second = None,None
		if(first_point < second_point):
			first = first_point
			second = second_point
		else:
			first = second_point
			second = first_point

		list_of_forbidden_points = []

		#prvo gledamo da li leze na istoj horizontali
		if(self.points[first_point].y == self.points[second_point].y):
			for i in range(first+1,second):
				list_of_forbidden_points.append(i)

			return list_of_forbidden_points


		# da li leze na istoj vertikali
		if(self.points[first_point].x == self.points[second_point].x):
			for i in range(first+BOARD_COLS,second,BOARD_COLS):
				list_of_forbidden_points.append(i)

			return list_of_forbidden_points


		
		# hocu da je first_point po 'x' prije second_point
		if(order_of_points(self.points[second_point],self.points[first_point])):
			temp = first_point
			first_point = second_point
			second_point = temp 
		
		for i in range(len(self.points)):
			if(equal_points(self.points[i],self.points[first_point]) or equal_points(self.points[i],self.points[second_point])):
				continue

			x = self.points[i].x
			y = self.points[i].y 

			# second_point ima veci 'y' od first_point
			if(self.points[first_point].y < self.points[second_point].y):
				if(x >= self.points[first_point].x and x <= self.points[second_point].x and y >= self.points[first_point].y and y <= self.points[second_point].y):
					a,b,c = find_parameter_for_line_segment(Segment(self.points[first_point],self.points[second_point]))
					if(intersect_segment_and_circle(a,b,c,x,y)):
						list_of_forbidden_points.append(i)
			else:
				if(x >= self.points[first_point].x and x <= self.points[second_point].x and y >= self.points[second_point].y and y <= self.points[first_point].y):
					a,b,c = find_parameter_for_line_segment(Segment(self.points[first_point],self.points[second_point]))
					if(intersect_segment_and_circle(a,b,c,x,y)):
						list_of_forbidden_points.append(i)	
		

		return list_of_forbidden_points
	

	def find_new_forbidden_points(self,first_point: int, second_point: int, third_point: int):
		return self.find_forbidden_points(first_point,second_point) + self.find_forbidden_points(second_point,third_point) + self.find_forbidden_points(third_point,first_point)

	def update_state(self,position):
		self.board[position[0]] = self.player_symbol
		self.board[position[1]] = self.player_symbol
		self.board[position[2]] = self.player_symbol

		self.forbidden_points[position[0]] = True
		self.forbidden_points[position[1]] = True
		self.forbidden_points[position[2]] = True
		self.triangles.append(Triangle(self.points[position[0]],self.points[position[1]],self.points[position[2]]))

		
		forbidden_indexes = self.find_new_forbidden_points(position[0],position[1],position[2])
		for i in range(len(forbidden_indexes)):
			self.forbidden_points[forbidden_indexes[i]] = True


		self.player_symbol = -1 if self.player_symbol == 1 else 1

	def reset(self):
		self.board = np.zeros((BOARD_ROWS*BOARD_COLS))
		self.board_hash = None
		self.is_end = False
		self.player_symbol = 1
		self.triangles = []
		self.counter = 0
		self.player_turn = False
		for i in range(len(self.forbidden_points)):
			self.forbidden_points[i] = False 

	def get_available_positions(self):

		positions = []
		for i in range(0,len(self.points)-2):
			if(self.forbidden_points[i]):
				continue
			for j in range(i+1,len(self.points)-1):
				if(self.forbidden_points[j]):
					continue
				for k in range(j+1,len(self.points)):
					if(self.forbidden_points[k] or orientation_of_points(self.points[i],self.points[j],self.points[k]) == 0):
						continue
					if(not self.find_intersection_for_triangle(Triangle(self.points[i],self.points[j],self.points[k]))):
						positions.append((i,j,k))
		return positions


	def game_over(self):
		for i in range(0,len(self.points)-2):
			if(self.forbidden_points[i]):
				continue
			for j in range(i+1,len(self.points)-1):
				if(self.forbidden_points[j]):
					continue
				for k in range(j+1,len(self.points)):
					if(self.forbidden_points[k] or orientation_of_points(self.points[i],self.points[j],self.points[k]) == 0):
						continue
					if(not self.find_intersection_for_triangle(Triangle(self.points[i],self.points[j],self.points[k]))):
						return False 
		return True 




	def training(self, rounds: int):

		for i in range(1,rounds+5):

			if(i%500 == 0):
				self.p1.save_policy()
				self.p1.decrease_exp_rate(0.05)


			while(not self.is_end):
				
				positions = self.get_available_positions()
				p1_position = self.p1.choose_position(positions,self.board,self.player_symbol)
				#print("P1: ",p1_position)
				self.update_state(p1_position)
				board_hash = self.get_hash()
				self.p1.add_state(board_hash)
				if(self.game_over()):
					print(str(i) + " P1")
					self.p1.increase_num_of_wins()
					self.p1.feed_reward(1)
					self.p2.feed_reward(0)
					self.p1.reset()
					self.p2.reset()
					self.reset()
					break
				else:
					positions = self.get_available_positions()
					p2_position = self.p2.choose_position(positions,self.board,self.player_symbol)
					#print("P2: ", p2_position)
					self.update_state(p2_position)
					board_hash = self.get_hash()
					self.p2.add_state(board_hash)
					if(self.game_over()):
						print(str(i) + " P2")
						self.p2.increase_num_of_wins()
						self.p1.feed_reward(0)
						self.p2.feed_reward(1)
						self.p1.reset()
						self.p2.reset()
						self.reset()
						break

	def play_minmax(self):
		best_value = 9999
		best_first,best_second,best_third = None, None, None

		for i in range(0,len(self.points)-2):
			if(self.forbidden_points[i]):
				continue
			for j in range(i+1,len(self.points)-1):
				if(self.forbidden_points[j]):
					continue
				for k in range(j+1,len(self.points)):
					if(self.forbidden_points[k] or orientation_of_points(self.points[i],self.points[j],self.points[k]) == 0):
						continue
					if(not self.find_intersection_for_triangle(Triangle(self.points[i],self.points[j],self.points[k]))):

						self.triangles.append(Triangle(self.points[i],self.points[j],self.points[k]))
						forbidden_indexes = self.find_new_forbidden_points(i,j,k)
						for z in range(len(forbidden_indexes)):
							self.forbidden_points[forbidden_indexes[z]] = True

						self.player_turn = not self.player_turn

						value = self.minmax(0,-9999,9999)
						if(value < best_value):
							best_value = value 
							best_first = i 
							best_second = j 
							best_third = k 


						last_element = self.triangles.pop()
						for z in range(len(forbidden_indexes)):
							self.forbidden_points[forbidden_indexes[z]] = False 

						self.player_turn = not self.player_turn

		#print("mm: ",best_value)
		return (best_first,best_second,best_third)


	def minmax(self,depth,alpha,beta):
		if(self.game_over()):
			if(self.player_turn):
				return -100+depth
			else:
				return 100-depth

		if(depth == 4):
			return 0


		if(self.player_turn):
			best_value = -9999

			for i in range(0,len(self.points)-2):
				if(self.forbidden_points[i]):
					continue
				for j in range(i+1,len(self.points)-1):
					if(self.forbidden_points[j]):
						continue
					for k in range(j+1,len(self.points)):
						if(self.forbidden_points[k] or orientation_of_points(self.points[i],self.points[j],self.points[k]) == 0):
							continue
						if(not self.find_intersection_for_triangle(Triangle(self.points[i],self.points[j],self.points[k]))):

							self.triangles.append(Triangle(self.points[i],self.points[j],self.points[k]))
							forbidden_indexes = self.find_new_forbidden_points(i,j,k)
							for z in range(len(forbidden_indexes)):
								self.forbidden_points[forbidden_indexes[z]] = True

							self.player_turn = not self.player_turn

							value = self.minmax(depth+1,alpha,beta)
							if(value > best_value):
								best_value = value 

							alpha = max(alpha,best_value)
							if(beta <= alpha):
								last_element = self.triangles.pop()
								for z in range(len(forbidden_indexes)):
									self.forbidden_points[forbidden_indexes[z]] = False 

								self.player_turn = not self.player_turn
								return value 



							last_element = self.triangles.pop()
							for z in range(len(forbidden_indexes)):
								self.forbidden_points[forbidden_indexes[z]] = False 

							self.player_turn = not self.player_turn

			return best_value
		else:

			best_value = 9999
			for i in range(0,len(self.points)-2):
				if(self.forbidden_points[i]):
					continue
				for j in range(i+1,len(self.points)-1):
					if(self.forbidden_points[j]):
						continue
					for k in range(j+1,len(self.points)):
						if(self.forbidden_points[k] or orientation_of_points(self.points[i],self.points[j],self.points[k]) == 0):
							continue
						if(not self.find_intersection_for_triangle(Triangle(self.points[i],self.points[j],self.points[k]))):

							self.triangles.append(Triangle(self.points[i],self.points[j],self.points[k]))
							forbidden_indexes = self.find_new_forbidden_points(i,j,k)
							for z in range(len(forbidden_indexes)):
								self.forbidden_points[forbidden_indexes[z]] = True

							self.player_turn = not self.player_turn

							value = self.minmax(depth+1,alpha,beta)
							if(value < best_value):
								best_value = value 

							beta = min(beta,best_value)
							if(beta <= alpha):
								last_element = self.triangles.pop()
								for z in range(len(forbidden_indexes)):
									self.forbidden_points[forbidden_indexes[z]] = False 

								self.player_turn = not self.player_turn 
								return value 



							last_element = self.triangles.pop()
							for z in range(len(forbidden_indexes)):
								self.forbidden_points[forbidden_indexes[z]] = False 

							self.player_turn = not self.player_turn

			return best_value
			


	def play(self,rounds):
		for i in range(rounds):
			while(not self.is_end):	

				if(self.player_symbol == 1 and self.counter < 0):
					position = self.play_minmax()
					#print("minmax: ", position)
					self.update_state(position)
					self.counter += 1
					if(self.game_over()):
						self.p1.increase_num_of_wins()
						print(i,": AI")
						self.reset()
						break
				else:
					positions = self.get_available_positions()
					p1_position = self.p1.choose_position(positions,self.board,self.player_symbol)
					#print("AI: ", p1_position)
					self.update_state(p1_position)
					self.counter += 1
					if(self.game_over()):
						self.p1.increase_num_of_wins()
						print(i,": AI")
						self.reset()
						break


				positions = self.get_available_positions()
				p2_position = self.p2.choose_position(positions,self.board,self.player_symbol)
				#print("Random: ",p2_position)
				self.update_state(p2_position)
				self.counter += 1
				if(self.game_over()):
					self.p2.increase_num_of_wins()
					print(i, ": Random")
					self.reset()
					break












class Player:
	def __init__(self, name: str, exp_rate: float = 0.3):
		self.name = name 
		self.states = []
		self.learning_rate = 0.2
		self.exp_rate = exp_rate
		self.decay_gamma = 0.9
		self.states_value = {}
		self.wins = 0

	def get_hash(self,board):
		board_hash = str(board)
		return board_hash

	def increase_num_of_wins(self):
		self.wins += 1

	def decrease_exp_rate(self,exp_rate: float):
		if(self.exp_rate == 0):
			return
		self.exp_rate -= exp_rate

	def choose_position(self, positions, current_board, symbol):

		if(np.random.uniform(0,1) <= self.exp_rate):
			index = np.random.choice(len(positions))
			position = positions[index]
		else:
			max_value = -999
			for p in positions:
				current_board[p[0]] = symbol
				current_board[p[1]] = symbol
				current_board[p[2]] = symbol 
				board_hash = self.get_hash(current_board)
				value = 0 if self.states_value.get(board_hash) is None else self.states_value.get(board_hash)
				if(value >= max_value):
					max_value = value
					position = p 
				current_board[p[0]] = 0
				current_board[p[1]] = 0
				current_board[p[2]] = 0
			if(max_value == 0):
				position = positions[np.random.choice(len(positions))]
				
			"""
			else:
				if(symbol == 1):
					print("111: ",max_value)
				else:
					print("222: ",max_value)
			"""
		
			#print("AI : ",max_value)
		
		return position


	def add_state(self,state):
		self.states.append(state)

	def reset(self):
		self.states = []

	def feed_reward(self, reward: int):
		for state in reversed(self.states):
			if(self.states_value.get(state) is None):
				self.states_value[state] = 0
			self.states_value[state] += self.learning_rate * (self.decay_gamma * reward - self.states_value[state])
			reward = self.states_value[state]

	def save_policy(self):
		fw = open('policy_' + str(self.name), 'wb')
		pickle.dump(self.states_value, fw)
		fw.close()

	def load_policy(self, file):
		fr = open(file, 'rb')
		self.states_value = pickle.load(fr)
		fr.close()






"""
p1 = Player("p1",0)
p1.load_policy("training_data/policy_p1_4_8")
p2 = Player("p2",1)
state = State(p1, p2)

print("testing...")
state.play(100)
print("AI: ", p1.wins)
print("Random: ", p2.wins)
"""






















