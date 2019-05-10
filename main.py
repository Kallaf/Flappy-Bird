import pygame
import socket
import _thread
import random
from roundrects import round_rect
from random import randint





import pygame
import socket
import _thread
import random
from roundrects import round_rect

black = (0,0,0)
green = (17, 224, 114)
red = (229, 69, 20)
white = (255,255,255)
yellow = (244, 191, 76)

pygame.init()
pygame.mixer.pre_init(44100,16,2,4096)

backgroundImage = pygame.image.load("assets/images/background.png")
birdImage = []
birdImage.append(pygame.image.load("assets/images/bird0.png"))
birdImage.append(pygame.image.load("assets/images/bird1.png"))
birdImage.append(pygame.image.load("assets/images/bird2.png"))
birdChange = 0
down_obstcale = pygame.image.load("assets/images/down_column.png")
up_obstcale = pygame.transform.flip(down_obstcale,False,True)

pass_sound = pygame.mixer.Sound("assets/sounds/pass.wav")
gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")
backgroundImage = pygame.transform.scale(backgroundImage, (700, 500))

size = 700,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

Ext = False

def write(x,y,w,h,msg,fnt,fntSize,color):
    font = pygame.font.SysFont(fnt,fntSize)
    text = font.render(msg,True,color)
    textRect = text.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(text, textRect)


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

		write(x,y-10,w,h,msg,"comicsansms",70,white)

clock = pygame.time.Clock()



#---------------------------------------------------------------------------------------------------------------#

connected = False
ready2 = False
ready1 = False
gameover1 = False
gameover2 = False
def parser(code):
    if code == "y":
        return 1
    return
#%%
def UDPlisten(server_port,hah):
    global flag,connected
    flag=0            
    broadcast_recv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    broadcast_recv.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    broadcast_recv.bind(("",8080))
    TCP_portnum=0
    TCP_IP = 0
    broadcast_recv.settimeout(10)
    while True:
        try:
            data= broadcast_recv.recvfrom(1024)
            message, addr = data
            message = message.decode()
            TCP_IP ,_ = addr
            check=parser(message[0])
            TCP_portnum = int(message[2:])
            if check==1:
                break
        except Exception:
            print('timed out udp :(')
            print("flag: ",flag)
            if flag==1:
                broadcast_recv.close()
                print("exit udp listen")
                return 
    flag=1
    broadcast_recv.close()
    print("exit udp listen")
    P2P = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("TCP_ip: ",TCP_IP,"Port: ",TCP_portnum)
    P2P.connect((TCP_IP,TCP_portnum))
    message=bytes("y startgame","utf-8")
    P2P.sendall(message)
    message_recieved = P2P.recv(1024).decode()
    print("message recieved: ",message_recieved)
    def wait_ready(ha,haha):
        global ready2
        nonlocal P2P
        P2P.recv(1024)
        ready2 = True
    def wait_gameover(ha,haha):
    	global gameover2
    	nonlocal P2P
    	P2P.recv(1024)
    	gameover2 = True
    if message_recieved == "y startgame":
    	connected = True
    	_thread.start_new_thread(wait_ready,("",""))
    	while not ready1:
    		continue
    	message=bytes("I'm ready","utf-8")
    	P2P.sendall(message)
    	_thread.start_new_thread(wait_gameover,("",""))
    	while not gameover1:
    		continue
    	message=bytes("gameover","utf-8")
    	P2P.sendall(message)
    	return
    
    return

def TCPlisten(server_port,ha):
    global flag,connected
    P2P =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    P2P.bind(("",server_port))
    P2P.settimeout(10)
    while True:
        try:
            P2P.listen(1)
            conn, addr = P2P.accept()
            message_recieved = conn.recv(1024).decode()
            message = b"y startgame"
            conn.sendall(message)
            print(message_recieved)
            print(addr)
            check = parser(message_recieved[0])
            if check == 1:
                print("yes")
                break
        except:
            print('timed out tcp :(')
            if flag==1 :
                P2P.close()
                print("exit tcp listen")
                return 
    flag=1
    print("message: ",message_recieved)
    def wait_ready(ha,haha):
        global ready2
        nonlocal conn
        conn.recv(1024)
        ready2 = True
    def wait_gameover(ha,haha):
    	global gameover2
    	nonlocal conn
    	conn.recv(1024)
    	gameover2 = True
    if message_recieved == "y startgame":
    	connected = True
    	_thread.start_new_thread(wait_ready,("",""))
    	while not ready1:
    		continue
    	message=bytes("I'm ready","utf-8")
    	conn.sendall(message)
    	_thread.start_new_thread(wait_gameover,("",""))
    	while not gameover1:
    		continue
    	message=bytes("gameover","utf-8")
    	conn.sendall(message)
    	return
    return



#---------------------------------------------------------------------------------------------------------------#


def startPage():
	global Ext,ready2,connected
	gameStarted = False
	start_ticks = -1.1

	def draw():

		nonlocal gameStarted
		global Ext,ready1,ready2,connected
		nonlocal start_ticks
		while (not gameStarted) and (not Ext):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					Ext = True
				if connected and event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						ready1 = True

			screen.blit(backgroundImage,(0,0))
			if not connected:
				write(220,200,260,100,"Waiting for a connection ...",None,50,red)
			else:
				if ready1:
					if not ready2:
						write(220,200,260,100,"Waiting the other player to be ready ...",None,50,yellow)
					else:
						if start_ticks == -1.1:
							start_ticks=pygame.time.get_ticks()
						seconds=(pygame.time.get_ticks()-start_ticks)/1000 
						if seconds > 5:
							gameStarted = True
						else:
							write(220,200,260,100,str(int(6-seconds)),"comicsansms",100,yellow)
				else:
					button(220,200,260,100,yellow,(255, 211, 86),start_game,"ready");
			pygame.display.flip()
			clock.tick(60)

	def start_game():
		global ready1
		ready1 = True



	server_port = random.randint(2**10+1,2**16-1)#randomly generated
	#print("yayyyyy",socket.getaddrinfo('',server_port,socket.AF_INET,socket.SOCK_STREAM)[-1][-1])
	ip_address,lok = socket.getaddrinfo('',server_port,socket.AF_INET,socket.SOCK_STREAM)[-1][-1]
	#print("dynamic ip-add is:",ip_add)
	print("randomly generated tcp port number: ",server_port)
	#ip_address = "192.168.0.1"
	message = bytes("y"+" "+str(server_port),'utf8')
	broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	broadcast.settimeout(0.2)
	data=0
	broadcast.sendto(message, ('<broadcast>', 8080))
	broadcast.shutdown(socket.SHUT_RDWR)
	broadcast.close()
	flag=0

	_thread.start_new_thread(UDPlisten,(server_port,""))
	_thread.start_new_thread(TCPlisten,(server_port,""))

	draw()




class Obstcale:

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.scoreAdded = False

def play_game():
	global Ext, birdImage,up_obstcale,down_obstcale,pass_sound,gameover_sound,clock,gameover1,gameover2
	bird_height = birdImage[0].get_height()
	bird_width = birdImage[0].get_width()
	x_size = 70
	y_size = 350
	up_obstcale = pygame.transform.scale(up_obstcale, (70,y_size))
	down_obstcale = pygame.transform.scale(down_obstcale, (70,y_size))
	gameEnd = False


	def bird(x,y):
		global birdChange
		birdChange += 1
		birdChange %= 30
		screen.blit(birdImage[birdChange//10], (x,y))

	def gameover():
		global gameover1,gameover2
		if gameover1:
			write(350,250,0,0,"Loser",None,75,red)
		elif gameover2:
			write(350,250,0,0,"Winner",None,75,green)

	def draw_obstacle(obstacle):
		global up_obstcale, down_obstcale
		screen.blit(up_obstcale, (obstacle.x,obstacle.y))
		screen.blit(down_obstcale, (obstacle.x,obstacle.y+space+y_size))


	def collision(obstacle):
		if  (x+bird_width > obstacle.x and y < obstacle.y+y_size and x < x_size+obstacle.x) or (x+bird_width > obstacle.x and y+bird_height > obstacle.y+y_size+space and x < x_size+obstacle.x):
			return True
		return False
				

	done = False
	x = 200
	y= 250
	x_speed = 0
	y_speed = 4
	ground = 477

	obstacles = []

	diff = 140

	for i in range(4):
		obstacles.append(Obstcale(700+i*200,randint(-y_size+diff,-diff)))

	space = 150
	obspeed = 4
	score = 0


	while (not Ext) and (not done):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Ext = True

			if gameEnd and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					done = True

			if (not gameEnd) and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					y_speed = -12

					

			if (not gameEnd) and event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					y_speed = 6


		if (not gameEnd):
			y += y_speed
			if y < 0:
				y = 0
			if y > ground:
				y=ground

			for obstacle in obstacles:
				obstacle.x -= obspeed

				if collision(obstacle):
					gameover()
					y_speed = 0
					obspeed = 0
					gameEnd = True
					gameover_sound.play()
					gameover1 = True

				if gameover2:
					gameover()
					y_speed = 0
					obspeed = 0
					gameEnd = True

				if obstacle.x < -80:
					obstacle.x = 700
					obstacle.y = randint(-y_size+diff,-diff)
					obstacle.scoreAdded = False

				if x > obstacle.x and not obstacle.scoreAdded:
					obstacle.scoreAdded = True
					score += 1
					if score%10 == 0:
						if diff > 80:
							diff -= 20
						pass_sound.play()
					if score%5 == 0:
						obspeed += 0.2
						pass_sound.play()
						
						

				

		screen.blit(backgroundImage,(0,0))
		for obstacle in obstacles:
			draw_obstacle(obstacle)
		bird(x,y)
		if gameEnd:
			gameover()
		pygame.display.flip()
		clock.tick(60)


startPage()
if not Ext:
	play_game()
pygame.quit()
