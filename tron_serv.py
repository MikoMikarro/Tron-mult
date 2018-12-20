import socket
import sys
import traceback
from threading import Thread
import sys
import pygame,sys
from pygame.locals import *
from pygame.draw import line

pygame.init()

is_playing = True

data = [[100,100,2,0],[400,400,2,2]]
ready = [False,False]
unitary = {0:[1,0],1:[0,1],2:[-1,0],3:[0,-1]}
restarted = [False,False]
# windowSurface = pygame.Surface((width,height))
# windowSurface.fill(BLACK)
def start_server():
    index = 0
    global is_playing
    host = "ip"
    port = puerto         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests

    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port,index,1240)).start()
            index+=1
        except:
            print("Thread did not start.")
            traceback.print_exc()
        if index == 2:
            break
    while True:

        if ready == [True,True]:
            is_playing = False

    soc.close()


def client_thread(connection, ip, port, index,max_buffer_size = 5120):
    global is_playing
    global data
    print(index)
    is_active = True
    connection.sendall(str(index))
    while True:
        a = connection.recv(1400)
        print(a)
        if a[-1] == ".":
            print("quitting")
            break
    ready[index] = True
    while is_playing:
        connection.sendall("-")
        connection.recv(1400)
    connection.sendall(".")
    while is_active:
        client_input = connection.recv(max_buffer_size).split(" ")
        if client_input[-1] == "r":
            print("WTF")
            if index == 0:
                restarted[1] = True
                continue
            else:
                restarted[0] = True
                continue
        if  index == 0 and restarted[0] == True:
            connection.sendall("r")
            restarted[0] = False
            continue
        if index == 1 and restarted[1]== True:
            connection.sendall("r")
            restarted[1] = False
            continue
        for i in range(len(client_input)-1) :
            if len(client_input)-1== 4:
                try:
                    data[index][i] = int(client_input[i])
                except ValueError:
                    print("overflow")
        txt= ""
        for i in data:
            for l in i:
                txt += str(l) + " "

        connection.sendall(txt)
start_server()
