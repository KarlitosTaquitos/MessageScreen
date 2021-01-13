#!/usr/bin/env python3

import sys, pygame, threading, random, socket, gspread, time
from pygame.locals import *
pygame.init()

#==================================================================================================

def display(text, textRect, width, height):
	while 1:
		global stopThread
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		if textRect.left < 0:
			speed[0] *= -1
			textRect.left = 0
		if textRect.right > width:
			speed[0] *= -1
			textRect.right = width
		if textRect.top < 0:
			speed[1] *= -1
			textRect.top = 0
		if textRect.bottom > height:
			speed[1] *= -1
			textRect.bottom = height

		textRect = textRect.move(speed)

		screen.fill((0, 0, 0))
		screen.blit(text, textRect)
		pygame.display.flip()
	
		if stopThread: break

#==================================================================================================

#Pygame screen stuff
speed = [5, 5]

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

font = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)

pygame.mouse.set_visible(False)

width = screen.get_width()
height = screen.get_height()

#Thread stuff
stopThread = False
threads = []

#Gspread stuff
gc = gspread.oauth()
source_sheet = gc.open("MessageScreen")
source_wsheet = source_sheet.get_worksheet(0)
message1 = source_wsheet.acell('A1').value


while 1:
	#read from gspread
	message2 = source_wsheet.acell('A1').value

	#if it's different kill the old thread and make a new one
	if (message1 != message2):
		print(message2)

		text = font.render(message2, True, (255, 0, 0))
		textRect = text.get_rect()
		randSpot = (random.randint(0, width), random.randint(0, height))
		textRect.center = randSpot

		outy = threading.Thread(target=display, args=(text, textRect, width, height))
		outy.daemon = True
		
		for thr in threads:
			stopThread = True
			thr.join()
			stopThread = False

		threads = []
		outy.start()
		threads.append(outy)

		message1 = message2

	time.sleep(1)