import pygame
from random import randint
from roundrects import round_rect

black = (0,0,0)
green = (89, 165, 77)
red = (255,0,0)

pygame.init()
pygame.mixer.pre_init(44100,16,2,4096)

backgroundImage = pygame.image.load("assets/images/background.png")
birdImage = pygame.image.load("assets/images/bird.png")
up_obstcale = pygame.image.load("assets/images/up_column.png")
down_obstcale = pygame.image.load("assets/images/down_column.png")

pass_sound = pygame.mixer.Sound("assets/sounds/pass.wav")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")
backgroundImage = pygame.transform.scale(backgroundImage, (700, 500))

size = 700,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

Ext = False


def button(x,y,w,h,ic,ac,action=None,msg=None,img=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if msg != None:
		if x+w > mouse[0] > x and y+h > mouse[1] > y:
		    round_rect(screen, (x,y,w,h),ac)

		    if click[0] == 1 and action != None:
		        action()         
		else:
		    round_rect(screen, (x,y,w,h),ic)


		font = pygame.font.SysFont("comicsansms",110)
		text = font.render(msg,True,(255,255,255))
		textRect = text.get_rect()
		textRect.center = ( (x+(w/2)), (y+(h/2)) )
		screen.blit(text, textRect)

	if img != None:
		screen.blit(img,(x,y))
		if x+w > mouse[0] > x and y+h > mouse[1] > y and click[0] == 1 and action != None:
			action()
