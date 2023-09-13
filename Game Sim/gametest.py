from collections import defaultdict
from math import pi
import pygame, sys, random
from pygame.locals import *
import math 



pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)
 
# Game Setup
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')
 # \


def rotate(origin, point, angle):
		"""
		Rotate a point counterclockwise by a given angle around a given origin.

		The angle should be given in radians.
		"""
		ox, oy = origin
		px, py = point

		qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
		qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
		return (qx, qy)



def pin(l,w):
	p1 = (0,0)
	p2 = (l,0)
	p3 = (l,w)
	p4 = (0,w)

	return [p1,p2,p3,p4]


def translate(delta,pts):
	npts = []
	for p in pts:
		npts.append((p[0] + delta[0],p[1] + delta[1]))
	return npts


def mrotate(theta,pts,origin = (0,0)):
	npts = [];
	# print(theta)
	# print(pi)
	# print(theta)
	nt = theta*pi/180.;
	for p in pts:
		np2 = rotate(origin,p,nt)
		npts.append(np2)
	return npts


def rlink(l,w):
	pin_width = 5;

	# AABB
	# AA
	aNear = mrotate(90.0,pin(w,pin_width))
	aFar = translate((l,0),mrotate(90.0,pin(w,pin_width)))
	# BB

	bBottom = pin(l,pin_width)
	bTop =  translate((0,w),pin(l,pin_width))

	return [aNear,bBottom,aFar,bTop]


def linkjoint(alpha = 0):
	a = 50;
	b = 100
	original = rlink(b,a);
	j1 = (0,0)
	j2 = (0,b)
	j3 = (a,b)
	j4 = (a,0)

	aNear,bBottom,aFar,bTop = original

	bBottom = mrotate(alpha,bBottom,j1);
	bTop = translate((-0,0),(mrotate(alpha,translate((0,0),bTop),(0,0))));

	bTopAbs = (b,0);

	bDelta = mrotate(alpha,[bTopAbs])
	delta = (-bTopAbs[0] + bDelta[0][0],- bTopAbs[1] + bDelta[0][1])
	print(bDelta);
	print(delta);
	print(aFar)
	aFar = translate(delta,aFar);
	print(aFar)

	return [aNear,bBottom,aFar,bTop]


def renderlinks():
	WINDOW.fill(BACKGROUND)
	alp = (1 + math.sin(pygame.time.get_ticks()/1000))*40;
	links = linkjoint(alp);
	for l in links:
		pygame.draw.polygon(WINDOW,(155,230,100),l,width = 6)


def main():
	looping = True
	
	# The main game loop
	while looping :
		# Get inputs
		for event in pygame.event.get() :
			if event.type == QUIT :
				pygame.quit()
				sys.exit()
		

		# Processing
		# This section will be built out later
		# r = 


		# Render elements of the game
		# WINDOW.fill(BACKGROUND)
		pygame.display.update()
		fpsClock.tick(FPS)
		renderlinks()
main()