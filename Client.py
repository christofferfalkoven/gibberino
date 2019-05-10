import socket
from threading import Thread
import Server
import json
import time
import gibberishGUI
from Tkinter import *
import sys
import multiprocessing
import ctypes

bootstrap_ip = sys.argv[1]

server_list = []
peers = {}
my_ip = None
server = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((bootstrap_ip, 3000))

def start_GUI(message, lock_message, switch_message, answer, lock_answer, switch_answer):
    root = Tk()
    ip = str(socket.gethostbyname(socket.gethostname()))
    gibberishGUI.Gibberish(root, ip, message, lock_message, switch_message, answer, lock_answer, switch_answer)
    root.mainloop()

message = multiprocessing.Value(ctypes.c_char_p, "")
switch_message = multiprocessing.Value(ctypes.c_bool, False)
lock_message = multiprocessing.Lock()
answer = multiprocessing.Value(ctypes.c_char_p, "")
switch_answer = multiprocessing.Value(ctypes.c_bool, False)
lock_answer = multiprocessing.Lock()
gui = Thread(target = start_GUI, args = (message, lock_message, switch_message, answer, lock_answer, switch_answer))
gui.start()

init1 = s.recv(4096)
(ip_adress, server_port, decided_server, peer_servers) = json.loads(init1)
my_ip = str(ip_adress)
print(my_ip)
server = decided_server
server_list = peer_servers

print("Starting server with server port: " + str(server_port))
my_server = Server.Server([], my_ip, server_port, )
thread = Thread(target = my_server.start_running, args = ())
thread.start()

def track_peers(listener, servers, peers): #Listens to the bootstraper for peer updates
    while True:
        try:
            update = listener.recv(4096)
            if update == "Status":
                pong = listener.send("Alive")
            else:
                update = json.loads(update)
                servers.append(update)
                t = Thread(target = message_handler, args = (str(update[0]), update[1], peers, ))
                t.start()   
                print("New peer update")
                print(update)
                print(servers)
                print(peers)
        except:
            pass

bootstrap_listener = Thread(target= track_peers, args = (s, server_list, peers, ))
bootstrap_listener.start()
time.sleep(1)

def update_peer_list(key, p, peers):
    peers[str(key)] = p

def message_handler(ip, portnum, peers):
    m = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(ip)
    print(portnum)
    while True:
        try:
            m.connect((ip, portnum))
            break
        except:
            #print("Something strange happebnd")
            continue
    print("Adding new socket")
    update_peer_list(portnum, m, peers)
    while True:
        try:
            socket_answer = m.recv(1024)
            if not socket_answer:
                m.close()
                break
            else:
                print(socket_answer)
                lock_answer.acquire()
                answer.value = socket_answer
                switch_answer.value = True
                lock_answer.release()

        except:
            print("ERROR, server is dead")
            m.close()
            break
        
print(server_list)
for t in server_list:
    (ip, portnum) = t
    user_listener = Thread(target = message_handler, args = (str(ip), portnum, peers, ))
    user_listener.start()

print(peers)

while True:
    try:
        messenger = peers[str(server)]
        print("Connected!")
        break
    except:
        continue

while True:
    #text = sys.stdin.readline()
    #messenger.send(text)
    try:
        #text = sys.stdin.readline()
        if switch_message.value:
            text = message.value
            messenger.send(text)
            switch_message.value = False
    except socket.error:
        while True:
            try:
                print("The server crashed")
                del peers[str(server)]
                del server_list[0]
                server = (server_list[0])[1]
                print("NEW SERVER: " + str(server))
                messenger = peers[str(server)]
                print(peers)
                print(messenger)
                print("Server crashed new host is: " + str(server))
                messenger.send(text)
                break
            except:
                pass


