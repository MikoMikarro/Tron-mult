import socket
import sys
import pygame,sys
from pygame.locals import *
from pygame.draw import line
from string import split

width = 500
height = 500

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE = (255,165,0)

unitary = {0:[1,0],1:[0,1],2:[-1,0],3:[0,-1]}
vel = 2

pygame.init()
windowSurface = pygame.display.set_mode((width,height))
windowSurface.fill(BLACK)

clock = pygame.time.Clock()

class Moto():
    def __init__(self,x,y,d,c):
        self.x = x
        self.y = y
        self.d = d
        self.c = c
        self.vel = vel
    def move(self):
        incrx = unitary[self.d][0]*self.vel
        incry = unitary[self.d][1]*self.vel
        try:
            if self.d == 0:
                if windowSurface.get_at((self.x + incrx,self.y + incry)) != BLACK:
                    return True

            elif self.d == 1:

                if windowSurface.get_at((self.x + incrx,self.y + incry)) != BLACK:
                    return True
            else:

                if windowSurface.get_at((self.x + incrx,self.y + incry)) != BLACK:
                    return True
        except IndexError:
            return True


        line(windowSurface,self.c,(self.x,self.y),(self.x + incrx,self.y + incry),1)
        self.x+= incrx
        self.y+= incry
        return False
    def rotate(self,incr):
        self.d+=incr
        if self.d == 4:
            self.d = 0
        if self.d == -1:
            self.d = 3

# a = Moto(100,100,0,BLUE)
# b = Moto(400,400,2,RED)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888
try:
    soc.connect((host, port))
except:
    print("Connection error")
    sys.exit()
index = soc.recv(5120)
if index == '0':
    a = Moto(100,100,0,BLUE)
    b = Moto(400,400,2,RED)
else:
    b = Moto(100,100,0,BLUE)
    a = Moto(400,400,2,RED)

input("Press enter to start")
soc.send(".")
while soc.recv(1400)[-1] == "-":
    soc.sendall("-")
while True:
    clock.tick(60)
    b.move()
    if a.move() :
        if index == '0':
            a = Moto(100,100,0,BLUE)
            b = Moto(400,400,2,RED)
        else:
            b = Moto(100,100,0,BLUE)
            a = Moto(400,400,2,RED)
        windowSurface.fill(BLACK)
        soc.sendall("r")
    for event in pygame.event.get():
        if event == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                a.rotate(-1)
            if event.key == K_RIGHT:
                a.rotate(1)

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        a.vel = vel*2
    else:
        a.vel = vel
    message = a.x,a.y,a.vel,a.d
    txt = ""
    for i in message:
        txt+= str(i)+" "
    soc.sendall(txt)
    changes = soc.recv(5120)
    print(changes)
    if changes[-1] == "r":

        if index == '0':
            a = Moto(100,100,0,BLUE)
            b = Moto(400,400,2,RED)
        else:
            b = Moto(100,100,0,BLUE)
            a = Moto(400,400,2,RED)
        windowSurface.fill(BLACK)
    n_changes = []

    try:
        for i in changes.split(" ")[:-1]:
            n_changes.append(int(i))

        if index =='0':
            a.x,a.y,a.vel,a.d,b.x,b.y,b.vel,b.d = n_changes
        else:
            b.x,b.y,b.vel,b.d,a.x,a.y,a.vel,a.d = n_changes
    except ValueError:
        pass

    pygame.display.update()
