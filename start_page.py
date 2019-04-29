from init import *

def startPage():
	global Ext
	gameStarted = False
	def start_game():
		nonlocal gameStarted
		gameStarted = True
	while (not gameStarted) and (not Ext):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Ext = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					gameStarted = True

		screen.blit(backgroundImage,(0,0))
		button(220,200,260,100,(244, 191, 76),(255, 211, 86),start_game,"play");
		pygame.display.flip()
	return Ext