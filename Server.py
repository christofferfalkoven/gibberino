import socket
from threading import Thread

class Server:

    def __init__(self, peers, host, port):
        self.peers = peers
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("", port))
        self.my_ip = host
        self.my_port = port

    
    def send_messages(self, message, sender):
        print("Im here!")
        for peer in self.peers:
            #if (peer != sender):
            print("Peer found")
            peer.send("Server says: " + message)
    
    def update_peers(self):
        "Update peers"

    def start_running(self,):
        if len(self.peers) != 0:
            print("Should not be the case!!")
            for peer in self.peers:
                thread = Thread(target = self.handle_user, args = (peer, ))
                thread.start()

        self.server.listen(5)
        print("Started client server with ip: " + str(self.my_ip) + " and port: " + str(self.my_port))        
        while True:
            user, address = self.server.accept() # Blocking call
            self.peers.append(user)
            print(address[0] + " has connected!")
            print(user)

            t = Thread(target = self.handle_user, args = (user, ))
            t.start()


    def handle_user(self, user, ):

        while True:
            try:
                message = user.recv(4096) # Blocking call
                if not message: #Client is dead
                    break
                else:
                    #send_messages(message, user)
                    for peer in self.peers:
                        try:
                            if peer is not user:
                                peer.send(message)

                        except:
                            self.peers.remove(peer)
            except:
                break