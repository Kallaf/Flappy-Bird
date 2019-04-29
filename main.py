from start_page import *


class Obstcale:

	def __init__(self,x,y):
		self.x = x
		self.y = y

def play_game():
	global Ext, birdImage,up_obstcale,down_obstcale,pass_sound,gameover_sound
	bird_height = birdImage.get_height()
	bird_width = birdImage.get_width()
	x_size = 70
	y_size = 350
	up_obstcale = pygame.transform.scale(up_obstcale, (70,y_size))
	down_obstcale = pygame.transform.scale(down_obstcale, (70,y_size))
	gameEnd = False
	def ball(x,y):
		screen.blit(birdImage, (x,y))

	def gameover():
		font = pygame.font.SysFont(None,75)
		text = font.render("Game over",True,red)
		textRect = text.get_rect()
		textRect.center = (350,250)
		screen.blit(text, textRect)

		font = pygame.font.SysFont(None,30)
		text = font.render("click space to start a new game",True,black)
		textRect = text.get_rect()
		textRect.center = (350,290)
		screen.blit(text, textRect)

	def draw_obstacle(obstacle):
		global up_obstcale, down_obstcale
		screen.blit(up_obstcale, (obstacle.x,obstacle.y))
		screen.blit(down_obstcale, (obstacle.x,obstacle.y+space+y_size))


	def Score(score):
		font = pygame.font.SysFont(None,50)
		text = font.render("Score: "+str(score),True,black)
		screen.blit(text, [0,0])


	def collision(obstacle):
		if  (x+bird_width > obstacle.x and y < obstacle.y+y_size and x-15 < x_size+obstacle.x) or (x+bird_width > obstacle.x and y+bird_height > obstacle.y+y_size+space and x-15 < x_size+obstacle.x):
			return True
		return False
				


	done = False
	x = 200
	y= 350
	x_speed = 0
	y_speed = 0
	ground = 477

	obstacles = []

	diff = 160

	for i in range(4):
		obstacles.append(Obstcale(700+i*200,randint(-y_size+diff,-diff)))

	space = 150
	obspeed = 0
	score = 0

	clock = pygame.time.Clock()

	while (not Ext) and (not done):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Ext = True

			if gameEnd and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					done = True

			if (not gameEnd) and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					y_speed = -6
					obspeed = 2.5
					

			if (not gameEnd) and event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					y_speed = 3


		if (not gameEnd):
			y += y_speed
			if y < 0:
				y = 0

			for obstacle in obstacles:
				obstacle.x -= obspeed

				if y > ground or collision(obstacle):
					gameover()
					y_speed = 0
					obspeed = 0
					gameEnd = True
					gameover_sound.play()


				if obstacle.x < -80:
					obstacle.x = 700
					obstacle.y = randint(-y_size+diff,-diff)

				if x > obstacle.x and x < obstacle.x+3:
					score += 1
					pass_sound.play()
					if score%5 == 0:
						obspeed += 0.5
						if diff > 0:
							diff -= 20
						
						

				

		screen.blit(backgroundImage,(0,0))
		for obstacle in obstacles:
			draw_obstacle(obstacle)
		ball(x,y)
		Score(score)
		if gameEnd:
			gameover()
		pygame.display.flip()
		clock.tick(60)

i = True
while not Ext:
	if i:
		i = False
		Ext = startPage()
	else:
		i = True
		play_game()

pygame.quit()