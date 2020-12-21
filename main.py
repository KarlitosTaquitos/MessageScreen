import sys, pygame, threading
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

speed = [5, 5]

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

font = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)

pygame.mouse.set_visible(False)
#print pygame.font.get_fonts()

width = screen.get_width()
height = screen.get_height()

stopThread = False
#inny = inputThread()
#inny.run(width, height, font)

threads = []

while 1:
    message = raw_input("Send: ")

    text = font.render(message, True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (45, 90)

    outy = threading.Thread(target=display, args=(text, textRect, width, height))
    outy.daemon = True
    for thr in threads:
	stopThread = True
	thr.join()
	stopThread = False

    threads = []
    outy.start()
    threads.append(outy)
