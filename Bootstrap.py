import socket
import json
import sys

host_name = sys.argv[1]
peers = []
server_list = []
"""
user_port_1 = 4011
user_port_2 = 4012

server_list.append(user_port_1)
server_list.append(user_port_2)
server_list.append(4013)
"""
user_port = 4000
server_port = None # Temp

bootstrap = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bootstrap.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
bootstrap.bind((host_name, 3000))
bootstrap.listen(5)

def peer_update(server_port, peers, server_list):
    updated_peer_list = []
    updated_server_list = []

    for p in range(0, len(peers)):
        peer = (peers[p])[0]
        peer.send("Status")
        answer = peer.recv(4096)

        if answer == "Alive":
            updated_peer_list.append(peers[p])
            updated_server_list.append(((server_list[p])[0], (server_list[p])[1]))
        else:
            if (peers[p])[1] == server_port:  
                server_port = None
    
    peers = updated_peer_list
    print("PEERS")
    print(peers)
    server_list = updated_server_list
    print("SERVERS")
    print(server_list)
    
    if server_port is None and len(server_list) > 0:
        server_port = server_list[0]

    return (server_port, peers, server_list)
    

def server_update(data):
    update = str(data)  

while True:
    user, address = bootstrap.accept()
    ip = address[0]
    ip = ip[0:].encode('utf-8')  #IP-ADDRESS
    print(ip)

    if len(peers) >= 2:
        (sp, p, sl) = peer_update(server_port, peers, server_list)
        peers = p
        server_list = sl
        server_port = sp
        print(peers)
        print(server_list)

    if len(peers) == 0:
        peers.append((user, user_port))
        server_list.append((ip, user_port))
        user_port = user_port + 1
        
    elif len(peers) == 1:
        if server_port is not None:
          print("One connection is alive")
          (sp, p, sl) = peer_update(server_port, peers, server_list)
          peers = p
          server_list = sl
          server_port = sp
          print("New server port is: " + str(server_port))

        if len(peers) == 0:
            server_port = user_port

        peers.append((user, user_port))
        server_list.append((ip, user_port))
        #user_port = user_port + 1

    if len(peers) >= 2:
        if server_port is None:
            server_port = (peers[0])[1]
            user_port1 = (peers[0])[1]
            print("CLIENT 1: USRPORT =  " + str(user_port1) + " SERVERPORT = " + str(server_port))
            smsg = json.dumps(((server_list[0])[1], user_port1, server_port, server_list))
            peer1 = (peers[0])[0]
            peer1.sendall(smsg)

            user_port2 = (peers[1])[1]
            print("CLIENT 2: USRPORT =  " + str(user_port2) + " SERVERPORT = " + str(server_port))
            peermsg = json.dumps(((server_list[1])[1], user_port2, server_port, server_list))
            peer2 = (peers[1])[0]
            peer2.sendall(peermsg)

            user_port = user_port + 1 #TEST
        else:
            #(p, s, sp) = peer_update(server_port, peers, server_list)
            #peers = p
            #server_list = s

            if len(peers) is not 0:
            #server_update(user_port)
                for peer in peers:
                    update = json.dumps((ip, user_port))
                    print("IN PEER LOOP")
                    print(peers)
                    print(peer[0])
                    peer[0].sendall(update)
            else:
                server_port = user_port

            print("Server is: " + str(server_port))
            print(server_list)

            if user_port in server_list:
                print("SHOULD BE TRUE")
                data = json.dumps((ip, user_port, server_port, server_list))
                print(data)
            else:
                peers.append((user, user_port))
                server_list.append((ip, user_port))
                data = json.dumps((ip, user_port, server_port, server_list))
                print(data)

            user_port = user_port + 1
            print(user)
            user.sendall(data)


'''
peers = []
server = None

bootstrap = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bootstrap.bind(socket.gethostbyname(socket.gethostname), 5000)
bootstrap.listen(10)

while True:
    user, adress = socket.accept()
    peers.append(user)

    if (len(peers < 2):
        # Wait for more peers
    elif server is not None:
        # Connect user to server
    else:
        server = peers[0]
        # Connect peer to other peer
    
''' 


