from dataclasses import dataclass

@dataclass
class Point:
	x: float
	y: float
	z: float = 0
	def __init__(self, x: float, y: float, z: float = 0):
		self.x = x
		self.y = y 
		self.z = z


@dataclass
class Segment:
	start: Point
	end: Point
	def __init__(self, start: Point, end: Point):
		if(end.x < start.x):
			self.start = end 
			self.end = start 
		elif(start.x == end.x):
			if(end.y < start.y):
				self.start = end 
				self.end = start 
			else:
				self.start = start
				self.end = end 
		else:
			self.start = start
			self.end = end 


@dataclass
class Triangle:
	A: Point
	B: Point
	C: Point

	def __init__(self, A: Point, B: Point, C: Point):
		self.A = A
		self.B = B 
		self.C = C 



# funkcija koja vraca True ako je A < B 
def order_of_points(A: Point, B: Point):
	if(A.x < B.x):
		return True 
	elif(A.x == B.x):
		return A.y < B.y 
	else:
		return False 


def equal_points(A: Point, B: Point):
	if(A.x == B.x and A.y == B.y):
		return True 
	return False 