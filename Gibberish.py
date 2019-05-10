from Tkinter import *
import socket
from threading import Thread
import Client
import gibberishGUI
import sys
import multiprocessing
import ctypes

# def start_Client(connection, message, lock):
#     c = Client.Client(connection, message, lock)
#
# def start_GUI(message, lock):
#     root = Tk()
#     ip = str(socket.gethostbyname(socket.gethostname()))
#     gibberishGUI.Gibberish(root, ip, message, lock)
#     # root.resizable(False, False)
#     root.mainloop()

if __name__ == "__main__":
    # message = multiprocessing.Value(ctypes.c_char_p, "")
    # lock = multiprocessing.Lock()
    # client = Thread(target = start_Client, args = (sys.argv[1], message, lock, ))
    # gui = Thread(target = start_GUI, args = (message, lock, ))
    # gui.start()
    # client.start()
    c = Client.Client(sys.argv[1])






