import math
from data_structures import *


def orientation_of_points(A: Point, B: Point, C: Point):

	a1 = B.x - A.x
	a2 = B.y - A.y
	b1 = C.x - A.x
	b2 = C.y - A.y

	result = a1*b2 - a2*b1 
	# conter-clockwise
	if(result < 0):
		return 1
	elif(result == 0):	#colinear
		return 0
	else:
		return -1	#clockwise


def point_on_segment(S: Segment, X: Point):
	segment_length = (S.end.x-S.start.x)*(S.end.x-S.start.x) + (S.end.y-S.start.y)* (S.end.y-S.start.y)
	start_to_point_length = abs((X.x-S.start.x)*(X.x-S.start.x) + (X.y-S.start.y)* (X.y-S.start.y))
	point_to_end_length = abs((S.end.x-X.x)*(S.end.x-X.x) + (S.end.y-X.y)* (S.end.y-X.y));

	return start_to_point_length + point_to_end_length == segment_length

def intersect_segments(A: Segment, B: Segment):
	result1 = orientation_of_points(A.start,A.end,B.start)
	result2 = orientation_of_points(A.start,A.end,B.end)
	result3 = orientation_of_points(B.start,B.end,A.start)
	result4 = orientation_of_points(B.start,B.end,A.end)


	if(result1 != result2 and result3 != result4):
		return True 
	elif(result1 == 0 and point_on_segment(A,B.start)):
		return True
	elif(result2 == 0 and point_on_segment(A,B.end)):
		return True
	elif(result3 == 0 and point_on_segment(B,A.start)):
		return True
	elif(result4 == 0 and point_on_segment(B,A.end)):
		return True
	else:
		return False 


def intersect_triangles(triangle_one: Triangle, triangle_two: Triangle):
	
	if(intersect_segments(Segment(triangle_one.A,triangle_one.B),Segment(triangle_two.A,triangle_two.B))):
		return True
	elif(intersect_segments(Segment(triangle_one.A,triangle_one.B),Segment(triangle_two.B,triangle_two.C))):
		return True
	elif(intersect_segments(Segment(triangle_one.A,triangle_one.B),Segment(triangle_two.C,triangle_two.A))):
		return True
	elif(intersect_segments(Segment(triangle_one.B,triangle_one.C),Segment(triangle_two.A,triangle_two.B))):
		return True
	elif(intersect_segments(Segment(triangle_one.B,triangle_one.C),Segment(triangle_two.B,triangle_two.C))):
		return True
	elif(intersect_segments(Segment(triangle_one.B,triangle_one.C),Segment(triangle_two.C,triangle_two.A))):
		return True
	elif(intersect_segments(Segment(triangle_one.C,triangle_one.A),Segment(triangle_two.A,triangle_two.B))):
		return True
	elif(intersect_segments(Segment(triangle_one.C,triangle_one.A),Segment(triangle_two.B,triangle_two.C))):
		return True
	elif(intersect_segments(Segment(triangle_one.C,triangle_one.A),Segment(triangle_two.C,triangle_two.A))):
		return True
	

	return False



def intersect_segment_and_circle(a: int, b: int, c: int, x: int, y: int):
	
	h = (abs(a * x + b * y + c)) / math.sqrt(a * a + b * b)
	if(h <= 8):
		return True
	
	return False


def find_parameter_for_line_segment(S: Segment):
	k = (S.end.y - S.start.y) / (S.end.x - S.start.x)
	a = -k
	# b = 1
	c = k * S.start.x - S.start.y

	return a,1,c