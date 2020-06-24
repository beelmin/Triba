from tkinter import *
import tkinter.messagebox as alert_box
import random
from computational_geometry_functions import *
from training import *


class Game:
	def __init__(self,num_of_rows: int, num_of_columns: int, player = None, difficult = None, player_turn = False,a_turn = False):
		self.rows = num_of_rows
		self.columns = num_of_columns
		self.player = player
		self.difficult = difficult
		self.points = []
		self.forbidden_points = []
		self.triangles = []
		self.current_board = np.zeros((self.rows*self.columns))

		self.first_point_index = None
		self.second_point_index = None
		self.counter = 0
		self.player_turn = player_turn
		self.a_turn = a_turn
		self.is_game_over = False

	def number_of_free_points(self):
		count = 0
		for i in range(len(self.forbidden_points)):
			if(self.orbidden_points[i] == True):
				count += 1

		return count

	def find_point(self,x,y):
		found = False
		for i in range(len(self.points)):
			if(x >= self.points[i].x-8 and x <= self.points[i].x+8 and y >= self.points[i].y-8 and y <= self.points[i].y+8):
				found = True
				return i

		if(not found):
			return -1

	def find_intersection_for_triangle(self,triangle: Triangle):

		for i in range(len(self.triangles)):
			if(intersect_triangles(triangle,self.triangles[i])):
				return True 

		return False 

	def clear_wrong_move(self,first_point: int, second_point: int, third_point: int):
		gui.create_oval(self.points[first_point].x-8, self.points[first_point].y-8, self.points[first_point].x+8, self.points[first_point].y+8,fill="grey")
		self.forbidden_points[first_point] = False 

		gui.create_oval(self.points[second_point].x-8,self.points[second_point].y-8, self.points[second_point].x+8, self.points[second_point].y+8,fill="grey")
		self.forbidden_points[second_point] = False 

		gui.create_oval(self.points[third_point].x-8,self.points[third_point].y-8, self.points[third_point].x+8, self.points[third_point].y+8,fill="grey")
		self.forbidden_points[third_point] = False


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
			for i in range(first+self.columns,second,self.columns):
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

	def get_all_available_positions(self):

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

	def play_computer_random(self):

		"""
		positions = self.get_all_available_positions()
		if(len(positions) <= 150):
			self.play_computer_minmax()
			return
		"""

		if(gui.counter >= 4):
			self.play_computer_minmax()
			return


		while(True):

			point_one_index = random.randint(0,len(self.points)-1)
			while(self.forbidden_points[point_one_index]):
				point_one_index = random.randint(0,len(self.points)-1)

			
			point_two_index = random.randint(0,len(self.points)-1)
			while(self.forbidden_points[point_two_index] or point_two_index == point_one_index):
				point_two_index = random.randint(0,len(self.points)-1)

			
			point_three_index = random.randint(0,len(self.points)-1)
			while(self.forbidden_points[point_three_index] or point_three_index == point_two_index or point_three_index == point_one_index or orientation_of_points(self.points[point_one_index],self.points[point_two_index],self.points[point_three_index]) == 0):
				point_three_index = random.randint(0,len(self.points)-1)

			if(self.find_intersection_for_triangle(Triangle(self.points[point_one_index],self.points[point_two_index],self.points[point_three_index]))):
				continue
			else:
				
				x = self.points[point_one_index].x
				y = self.points[point_one_index].y 
				gui.canvas.create_oval(x-8, y-8, x+8, y+8,fill="red")
				self.forbidden_points[point_one_index] = True 

				x = self.points[point_two_index].x
				y = self.points[point_two_index].y 
				gui.canvas.create_oval(x-8, y-8, x+8, y+8,fill="red")
				self.forbidden_points[point_two_index] = True

				x = self.points[point_three_index].x
				y = self.points[point_three_index].y 
				gui.canvas.create_oval(x-8, y-8, x+8, y+8,fill="red")
				self.forbidden_points[point_three_index] = True 

				triangle = Triangle(self.points[point_one_index],self.points[point_two_index],self.points[point_three_index])
				self.triangles.append(triangle)
				gui.canvas.create_line(triangle.A.x, triangle.A.y, triangle.B.x, triangle.B.y,fill="red",width=3)
				gui.canvas.create_line(triangle.B.x, triangle.B.y, triangle.C.x, triangle.C.y,fill="red",width=3)
				gui.canvas.create_line(triangle.C.x, triangle.C.y, triangle.A.x, triangle.A.y,fill="red",width=3)

				forbidden_indexes = self.find_new_forbidden_points(point_one_index,point_two_index,point_three_index)
				for i in range(len(forbidden_indexes)):
					x = self.points[forbidden_indexes[i]].x
					y = self.points[forbidden_indexes[i]].y
					gui.canvas.create_oval(x-8, y-8, x+8, y+8,fill="black")
					self.forbidden_points[forbidden_indexes[i]] = True 
				
				self.player_turn = not self.player_turn
				gui.counter += 1
				if(self.game_over()):
					self.is_game_over = True 
					alert_box.showinfo("INFO","AI Player won!!!")
					gui.status_text.set("AI Player won!!!")
				else:
					gui.status_text.set("AI played the move, now the Player is on the move")
					gui.canvas.create_line(25,50,25,270,fill="green",width=4)
					gui.canvas.create_line(300,50,300,270,fill="green",width=4)

				break;

	def play_computer(self):


		if(self.difficult == "easy"):
			if(random.uniform(0.0,1.0)  < 0.5):
				self.play_computer_random()
				return


		if(gui.counter >= 4):
			self.play_computer_minmax()
			return

		
		positions = self.get_all_available_positions()
		print(len(positions))
		"""
		if(len(positions) <= 150):
			self.play_computer_minmax()
			return
		"""
		#print(len(positions))
		#print("Nasao pozicije")
		ai_position = self.player.choose_position(positions,self.current_board,1)
		#print("Pozicije: ",ai_position)
		for i in range(3):
			self.current_board[ai_position[i]] = 1
			self.forbidden_points[ai_position[i]] = True
			gui.canvas.create_oval(self.points[ai_position[i]].x-8,self.points[ai_position[i]].y-8, self.points[ai_position[i]].x+8, self.points[ai_position[i]].y+8,fill="red")


		triangle = Triangle(self.points[ai_position[0]],self.points[ai_position[1]],self.points[ai_position[2]])
		self.triangles.append(triangle)
		gui.canvas.create_line(triangle.A.x, triangle.A.y, triangle.B.x, triangle.B.y,fill="red",width=3)
		gui.canvas.create_line(triangle.B.x, triangle.B.y, triangle.C.x, triangle.C.y,fill="red",width=3)
		gui.canvas.create_line(triangle.C.x, triangle.C.y, triangle.A.x, triangle.A.y,fill="red",width=3)

		forbidden_indexes = self.find_new_forbidden_points(ai_position[0],ai_position[1],ai_position[2])
		
		for i in range(len(forbidden_indexes)):
			x = self.points[forbidden_indexes[i]].x
			y = self.points[forbidden_indexes[i]].y
			gui.canvas.create_oval(x-8, y-8, x+8, y+8,fill="black")
			self.forbidden_points[forbidden_indexes[i]] = True

		self.player_turn = not self.player_turn
		gui.counter += 1
		if(self.game_over()):
			self.is_game_over = True 
			alert_box.showinfo("INFO","AI Player won!!!")
			gui.status_text.set("AI Player won!!!")
			return 
		else:
			gui.status_text.set("AI played the move, now the Player is on the move")
			gui.canvas.create_line(25,50,25,270,fill="green",width=4)
			gui.canvas.create_line(300,50,300,270,fill="green",width=4)

	def play_computer_minmax(self):
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


		#sada kada smo nasli najbolja 3 indeksa tacaka, odigramo potez sa tim
		triangle = Triangle(self.points[best_first],self.points[best_second],self.points[best_third])
		self.triangles.append(triangle)
		gui.canvas.create_line(triangle.A.x, triangle.A.y, triangle.B.x, triangle.B.y,width=3)
		gui.canvas.create_line(triangle.B.x, triangle.B.y, triangle.C.x, triangle.C.y,width=3)
		gui.canvas.create_line(triangle.C.x, triangle.C.y, triangle.A.x, triangle.A.y,width=3)


		self.forbidden_points[best_first] = True
		gui.canvas.create_oval(self.points[best_first].x-8,self.points[best_first].y-8, self.points[best_first].x+8, self.points[best_first].y+8,fill="black")
		self.forbidden_points[best_second] = True
		gui.canvas.create_oval(self.points[best_second].x-8,self.points[best_second].y-8, self.points[best_second].x+8, self.points[best_second].y+8,fill="black")
		self.forbidden_points[best_third] = True
		gui.canvas.create_oval(self.points[best_third].x-8,self.points[best_third].y-8, self.points[best_third].x+8, self.points[best_third].y+8,fill="black")


		forbidden_indexes = self.find_new_forbidden_points(best_first,best_second,best_third)
		
		for i in range(len(forbidden_indexes)):
			x = self.points[forbidden_indexes[i]].x
			y = self.points[forbidden_indexes[i]].y
			gui.canvas.create_oval(x-8, y-8, x+8, y+8,fill="black")
			self.forbidden_points[forbidden_indexes[i]] = True

		self.player_turn = not self.player_turn
		print("Minmax: ",best_value)

		if(self.game_over()):
			self.is_game_over = True 
			alert_box.showinfo("INFO","AI Player won!!!")
			return 


	def minmax(self,depth: int, alpha: int, beta: int):

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




class GUI:

	def __init__(self,master):

		master.title("TRIBA")

		self.game = None
		self.is_start_game = False 
		self.number_of_rounds_player_vs_player = 0
		self.counter = 0

		self.menu = Menu(master)
		master.config(menu=self.menu)
		self.menu.add_cascade(label="New Game",command=self.reset)
		self.menu.add_cascade(label="Instructions",command=self.game_instructions)

		self.sub_menu_project = Menu(self.menu,tearoff=0)
		self.menu.add_cascade(label="Project",menu=self.sub_menu_project)
		self.sub_menu_subject = Menu(self.sub_menu_project,tearoff=0)
		self.sub_menu_project.add_cascade(label="Subject",menu=self.sub_menu_subject)
		self.sub_menu_subject.add_command(label="Professor",command=self.get_professor)
		self.sub_menu_subject.add_command(label="Assistant",command=self.get_assistant)

		self.sub_menu_project.add_command(label="Study",command=self.get_study)
		self.sub_menu_project.add_command(label="Faculty",command=self.get_faculty)
		self.sub_menu_project.add_command(label="Name",command=self.get_project_name)

		self.sub_menu_author = Menu(self.sub_menu_project,tearoff=0)
		self.sub_menu_project.add_cascade(label="Author",menu=self.sub_menu_author)
		self.sub_menu_author.add_command(label="Belmin Ruhotina")
		self.sub_menu_author.add_command(label="Contact",command=self.get_author_contact)


		self.status_text = StringVar()
		self.status_text.set("The game has not started yet...")
		self.status = Label(master,textvariable=self.status_text, bd=1, relief=SUNKEN)
		self.status.pack(side=BOTTOM, fill=X)

		self.canvas = Canvas(master, bg="white", height=300, width=400)
		self.canvas.bind("<Button-1>",self.on_click)
		self.canvas.pack(side=LEFT)



		self.frame = Frame(master,height=300,width=300)
		# pack_propagate(0) znaci da se frame nece prilagodit sirini elemenata, jer po defaultu on to radi
		self.frame.pack_propagate(0)
		self.frame.pack(side=LEFT)

		
		self.label_one = Label(self.frame,text="Select board size")
		self.label_one.pack()

		self.frame_one = Frame(self.frame,height=25,width=300)
		self.frame_one.pack_propagate(0)
		self.frame_one.pack()

		self.label_num_of_rows = Label(self.frame_one,text="Enter the number of rows: ")
		self.label_num_of_rows.pack(side=LEFT,anchor="n")

		self.entry_rows = StringVar()
		self.entry_rows.set("")
		self.entry_num_or_rows = Entry(self.frame_one,textvariable=self.entry_rows)
		self.entry_num_or_rows.pack(side=LEFT,anchor="n")


		self.frame_two = Frame(self.frame,height=40,width=300)
		self.frame_two.pack_propagate(0)
		self.frame_two.pack()


		self.label_num_of_cols = Label(self.frame_two,text="Enter the number of columns: ")
		self.label_num_of_cols.pack(side=LEFT,anchor="n")

		self.entry_cols = StringVar()
		self.entry_cols.set("")
		self.entry_num_or_cols = Entry(self.frame_two,textvariable=self.entry_cols)
		self.entry_num_or_cols.pack(side=LEFT,anchor="n")


		self.frame_three = Frame(self.frame,height=200,width=300)
		self.frame_three.pack_propagate(0)
		self.frame_three.pack()

		self.label_two = Label(self.frame_three,text="Select a game mode: ")
		self.label_two.pack()

		self.radio_type_play = IntVar() 
		self.radio_type_play.set(0)
		self.radio_one = Radiobutton(self.frame_three, text="Player vs Player", variable=self.radio_type_play, value=1)  
		self.radio_one.pack(anchor="w")  
		  
		self.radio_two = Radiobutton(self.frame_three, text="Player vs AI", variable=self.radio_type_play, value=2)  
		self.radio_two.pack(anchor="w")  

		self.label_three = Label(self.frame_three,text="Select a difficult for AI Player: ")
		self.label_three.pack()


		self.radio_ai = StringVar()
		self.radio_ai.set("none")

		self.radio_three = Radiobutton(self.frame_three, text="Easy", variable=self.radio_ai, value="easy",tristatevalue=0)  
		self.radio_three.pack(anchor="w")  
		self.radio_three.deselect()
		  
		self.radio_four = Radiobutton(self.frame_three, text="Medium", variable=self.radio_ai, value="medium",tristatevalue=0) 
		self.radio_four.pack(anchor="w")
		self.radio_four.deselect() 

		self.button_start_game = Button(self.frame_three,text = "START GAME",command=self.start_game)
		self.button_start_game.pack()


	def get_professor(self):
		alert_box.showinfo("INFO","Professor: doc. dr. Adis Alihodzic")

	def get_assistant(self):
		alert_box.showinfo("INFO","Assistant: MA Sead Delalic")

	def get_project_name(self):
		alert_box.showinfo("INFO","TRIBA")

	def get_study(self):
		alert_box.showinfo("INFO","Graduate/Computer Science")

	def get_faculty(self):
		alert_box.showinfo("INFO","Faculty of Natural Sciences and Mathematics Sarajevo")

	def get_author_contact(self):
		alert_box.showinfo("INFO","E-mail: belmin.ruhotina@gmail.com")

	def game_instructions(self):
		text = "The game consists of a board of points. The dimension of board is mxn, where m and n are even numbers."
		text += "Two players play alternately."
		text += "Each player selects a triangle in his move by picking three points from the board that are not collinear."
		text += "Triangles must not intersect and two triangles must not have a common vertex."
		text += "Triangles can be located inside each other."
		text += "The game is over when one player runs out of moves."
		text += "The player who is left without a move loses the game."
		text += "The side lines represent the color of the player on the move."
		alert_box.showinfo("INFO", text)


	def reset(self):
		self.entry_rows.set("")
		self.entry_cols.set("")
		self.radio_type_play.set(0)
		self.radio_ai.set("none")
		self.status_text.set("The game has not started yet...")
		self.is_start_game = False
		self.game.is_game_over = False 
		self.canvas.delete(ALL) 
		self.counter = 0






	def on_click(self,event):
		if(not self.is_start_game):
			alert_box.showinfo("INFO","The game has not started yet...")

		if(self.game.is_game_over):
			alert_box.showinfo("Info","The game is over!")
			return

		if(self.radio_type_play.get() == 2 and not self.game.player_turn):
			alert_box.showinfo("INFO","Is not a Player move")
			return



		if(self.radio_type_play.get() == 1 or self.radio_type_play.get() == 2):
			if(self.game.counter == 0):
				index = self.game.find_point(event.x,event.y)
				if(index == -1 or self.game.forbidden_points[index] == True):
					alert_box.showinfo("INFO","Choose the grey point")
				else:
					self.game.first_point_index = index
					if(self.game.a_turn):
						self.canvas.create_oval(self.game.points[index].x-8, self.game.points[index].y-8, self.game.points[index].x+8, self.game.points[index].y+8,fill="red")
					else:
						self.canvas.create_oval(self.game.points[index].x-8, self.game.points[index].y-8, self.game.points[index].x+8, self.game.points[index].y+8,fill="green")
					self.game.forbidden_points[index] = True
					self.game.counter += 1
			elif(self.game.counter == 1):
				index = self.game.find_point(event.x,event.y)
				if(index == -1 or self.game.forbidden_points[index] == True):
					alert_box.showinfo("INFO","Choose the grey point")
				else:
					self.game.second_point_index = index
					if(self.game.a_turn):	
						self.canvas.create_oval(self.game.points[index].x-8,self.game.points[index].y-8, self.game.points[index].x+8, self.game.points[index].y+8,fill="red")
					else:
						self.canvas.create_oval(self.game.points[index].x-8, self.game.points[index].y-8, self.game.points[index].x+8, self.game.points[index].y+8,fill="green")

					self.game.forbidden_points[index] = True 
					self.game.counter += 1
			elif(self.game.counter == 2):
				index = self.game.find_point(event.x,event.y)
				if(index == -1 or self.game.forbidden_points[index] == True):
					alert_box.showinfo("INFO","Choose the grey point")
				elif(orientation_of_points(self.game.points[self.game.first_point_index],self.game.points[self.game.second_point_index],self.game.points[index]) == 0):
					alert_box.showinfo("INFO","Points are collinear, select the third point again")
				else:
					if(self.game.a_turn):
						self.canvas.create_oval(self.game.points[index].x-8,self.game.points[index].y-8, self.game.points[index].x+8, self.game.points[index].y+8,fill="red")
					else:
						self.canvas.create_oval(self.game.points[index].x-8, self.game.points[index].y-8, self.game.points[index].x+8, self.game.points[index].y+8,fill="green")

					self.game.forbidden_points[index] = True 
					if(self.game.find_intersection_for_triangle(Triangle(self.game.points[self.game.first_point_index],self.game.points[self.game.second_point_index],self.game.points[index]))):
						alert_box.showinfo("Info","Triangle cuts some of the existing triangles, select three new points again")
						self.game.clear_wrong_move(self.game.first_point_index,self.game.second_point_index,index)
						self.game.counter = 0
					else:
						triangle = Triangle(self.game.points[self.game.first_point_index],self.game.points[self.game.second_point_index],self.game.points[index])
						self.game.current_board[self.game.first_point_index] = -1
						self.game.current_board[self.game.second_point_index] = -1
						self.game.current_board[index] = -1
						self.game.triangles.append(triangle)
						if(self.game.a_turn):
							self.canvas.create_line(triangle.A.x, triangle.A.y, triangle.B.x, triangle.B.y,fill="red",width=3)
							self.canvas.create_line(triangle.B.x, triangle.B.y, triangle.C.x, triangle.C.y,fill="red",width=3)
							self.canvas.create_line(triangle.C.x, triangle.C.y, triangle.A.x, triangle.A.y,fill="red",width=3)
						else:
							self.canvas.create_line(triangle.A.x, triangle.A.y, triangle.B.x, triangle.B.y,fill="green",width=3)
							self.canvas.create_line(triangle.B.x, triangle.B.y, triangle.C.x, triangle.C.y,fill="green",width=3)
							self.canvas.create_line(triangle.C.x, triangle.C.y, triangle.A.x, triangle.A.y,fill="green",width=3)

						#find new forbidden points
						forbidden_indexes = self.game.find_new_forbidden_points(self.game.first_point_index,self.game.second_point_index,index)
						for i in range(len(forbidden_indexes)):
							x = self.game.points[forbidden_indexes[i]].x
							y = self.game.points[forbidden_indexes[i]].y
							self.canvas.create_oval(x-8, y-8, x+8, y+8,fill="black")
							self.game.forbidden_points[forbidden_indexes[i]] = True 
						self.game.counter = 0
						self.counter += 1
						if(self.game.game_over()):
							self.game.is_game_over = True 
							if(self.game.player_turn):
								alert_box.showinfo("INFO","Player won!!!")
								self.status_text.set("Player won!!!")
							elif(self.game.a_turn):
								alert_box.showinfo("INFO","Player A won!!!")
								self.status_text.set("Player A won!!!")
							else:
								alert_box.showinfo("INFO","Player B won!!!")
								self.status_text.set("Player B won!!!")
							return 
						if(self.radio_type_play.get() == 2 and not self.game.is_game_over):
							self.game.player_turn = not self.game.player_turn
							self.status_text.set("Player played the move, now the AI Player is on the move")
							self.canvas.create_line(25,50,25,270,fill="red",width=4)
							self.canvas.create_line(300,50,300,270,fill="red",width=4)
							if(self.game.rows == 6 and self.game.columns == 8):
								self.game.play_computer_random()
							# ovaj elif je za 4x4, 4x6, 4x8 i 6x6
							# da se ne bi uslo u ovaj elif kad je 6x8 zato je stavljen iznad if
							elif(self.game.rows <= 6 and self.game.columns <= 8):
								self.game.play_computer()
							else:
								self.game.play_computer_random()
						else:
							if(self.game.a_turn):
								self.game.a_turn = not self.game.a_turn
								self.status_text.set("Player A played the move, now the Player B is on the move")
								self.canvas.create_line(25,50,25,270,fill="green",width=4)
								self.canvas.create_line(300,50,300,270,fill="green",width=4)
							else:
								self.game.a_turn = not self.game.a_turn
								self.status_text.set("Player B played the move, now the Player A is on the move")
								self.canvas.create_line(25,50,25,270,fill="red",width=4)
								self.canvas.create_line(300,50,300,270,fill="red",width=4)







	


	def start_game(self):
		if(self.is_start_game):
			alert_box.showinfo("INFO", "The game is on!!!")
			return

		rows = int(self.entry_num_or_rows.get())
		cols = int(self.entry_num_or_cols.get())
		if(rows % 2 != 0 or cols % 2 != 0):
			alert_box.showinfo("INFO","You must enter even numbers")
			return
		
		# ako je Player vs Player	
		if(self.radio_type_play.get() == 1):
			self.game = Game(num_of_rows=rows,num_of_columns=cols)
			self.draw_board(rows,cols)
		# ako je Player vs AI
		elif(self.radio_type_play.get() == 2):
			difficult = None 
			if(self.radio_ai.get() == "easy"):
				difficult = "easy"
			elif(self.radio_ai.get() == "medium"):
				difficult = "medium"
			else:
				alert_box.showinfo("INFO","Select a difficult for AI Player!!!")
				return

			ai_player = Player("Computer",exp_rate = 0)
			if(rows == 4 and cols == 4):
				ai_player.load_policy("training_data/policy_p1_4_4")
			elif(rows == 4 and cols == 6):
				ai_player.load_policy("training_data/policy_p1_4_6")
			elif(rows == 4 and cols == 8):
				ai_player.load_policy("training_data/policy_p1_4_8")
			elif(rows == 6 and cols == 6):
				ai_player.load_policy("training_data/policy_p1_6_6")

			# ako je game mode AI vs Player, uvijek AI prvi igra
			self.game = Game(num_of_rows = rows,num_of_columns=cols,player=ai_player,difficult=difficult,player_turn = False, a_turn=False)
			self.draw_board(rows,cols)

		else:
			alert_box.showinfo("INFO","Select a game mode!!!")


	def draw_board(self,rows,cols):
		for i in range(rows):
			for j in range(cols):
				x = 50+j*30
				y = 50+i*30
				self.canvas.create_oval(x-8, y-8, x+8, y+8,fill="grey")
				self.game.points.append(Point(50+j*30,50+i*30))
				self.game.forbidden_points.append(False)

		
		self.is_start_game = True

		# ako je odabrano player vs AI pri cemu AI igra prvi uvijek
		if(self.radio_type_play.get() == 2):
			self.status_text.set("The game has begun. AI Player has the first move")
			self.canvas.create_line(25,50,25,270,fill="red",width=4)
			self.canvas.create_line(300,50,300,270,fill="red",width=4)
			if(rows == 6 and cols == 8):
				self.game.play_computer_random()
			# ovaj elif je za 4x4, 4x6, 4x8 i 6x6
			# da se ne bi uslo u ovaj elif kad je 6x8 zato je stavljen iznad if
			elif(rows <= 6 and cols <= 8):
				self.game.play_computer()
			else:
				self.game.play_computer_random()
		else:
			self.number_of_rounds_player_vs_player += 1
			if(self.number_of_rounds_player_vs_player % 2 != 0):
				self.game.a_turn = True
				self.status_text.set("The game has begun. Player A has the first move.")
				self.canvas.create_line(25,50,25,270,fill="red",width=4)
				self.canvas.create_line(300,50,300,270,fill="red",width=4) 
			else:
				self.game.a_turn = False
				self.status_text.set("The game has begun. Player B has the first move.")
				self.canvas.create_line(25,50,25,270,fill="green",width=4)
				self.canvas.create_line(300,50,300,270,fill="green",width=4) 

			









# kreiramo prozor
root = Tk()
# sve njegove komponente i funkcionalnosti se nalaze u klasi GUI
gui = GUI(root)
# da nema mainloop() prozor bi se otvorio i zatvorio tj korisnik cak ne bi primjetio ni da se otvorio
# da bi prozor bio vidljiv dokle god to korisnik zeli, pokrece se beskonacna petlja mainloop()
# kada korisnik klikne na "X" ona se prekida,prozor se zatvara i program zavrsava svoj rad
root.mainloop()










