# -*- coding: utf-8 -*-
'''
Author: Christian Hopkins
ID: 001244953
'''

'''
Import statements, socket is for socket communications
threading is for multithreading the application
tkinter is for the GUI development
functools is for implementing callback functions in graphic widgets
'''
import socket
import threading
import tkinter
from tkinter import *
from functools import partial

'''
Global variables:
    log to allow modification of server log
    st_button is to allow the start server button to be disabled
    win is to allow access to the main frame
    player1_choice and player2_choice store the players choice
    sockets is a list of the connected sockets
'''
global log
global st_button
global win
global player1_choice
global player2_choice
sockets = [] 


'''
start function is run when the server start button is pushed. 
it gets the port and ip from the entry widgets and passes it to the 
public start method 
'''
def start(port,ip):
    p = int(port.get())
    i = ip.get()
    start(p,i)

'''
this method is a callback method to call the end_comm method to 
close communication between clients
'''
def end():
    end_comm()

#initializes the frame
window = tkinter.Tk()
#Changes the name of the frame
window.title("Server")
# saves the window to the global variable
win = window
#initializes the server log label
l = Label(window,  text = "Server Log")
# set the position of the label
l.grid(row=4 ,column=0 )
#initializes the text box that serves as the log
t = Text(window, height = 30, width = 30)
#sets position
t.grid(row=5,column=0)
#saves global variable
log = t
#initializes entry for ip address
ip = Entry(window)
#sets position
ip.grid(row=2,column=0)
#sets intial value in field
ip.insert(0, "IP address")
#intializes entry for port
port = Entry(window)
#sets position
port.grid(row=3,column=0)
#sets intial value
port.insert(0, "Port")
#intializes start button
start = Button(window, text = "Start Server", command = partial(start, port, ip))
#Sets initial position
start.grid(row=1 ,column=0)
#saves to global variable
st_button = start
#intializes close button
b = Button(window, text = "End Server", command = partial(end,))
#sets postion
b.grid(row=0 ,column=0)


'''
This function determines the winner from the passed strings
'''
def logic(player1,player2):
    '''global player1_choice
    global player2_choice
    player1 = player1_choice
    player2 = player2_choice'''
    #this is where the results are stored based on if else chain
    winner = ""
    if player1 == player2:
        winner = "tie"
    elif player1 == 'rock' and player2 == 'scissors':
        winner = "p1"
    elif player1 == 'paper' and player2 == 'rock':
        winner = "p1"
    elif player1 == 'scissors' and player2 == 'paper':
        winner = "p1"
    else:
        winner = "p2"
    #returning winner
    return winner
'''
This function handles the communications between the server and client
'''
def communicate(client_sock, client_ip):
    global sockets
    global player1_choice
    global player2_choice
 
    #setting variables to defaults
    player1_choice = " "
    player2_choice = " "
    res = " "
    
    #flag to determine if the greeting should run
    flag = True
    #loop to run the server
    while True:
        data = client_sock.recv(1024)
        
        #determine if greeting or selection
        if flag:
            flag = False
            if sockets[0] == client_sock:
                #player1_choice = data
                log.insert(END, "welcome player1\n")
            else:
                #player2_choice = data
                log.insert(END, "welcome player2\n")
        else:
            #check if quit is passed by client
            if repr(data) == "b'quit'":
                print("From Client: quitting")
                end_comm()
                break
            #determine if this is player one or two and generates log message accordingly
            if sockets[0] == client_sock:
                player1_choice = data
                log.insert(END, "player1 chose: {}\n".format(repr(player1_choice)[2:-1]))
            else:
                player2_choice = data
                log.insert(END, "player2 chose: {}\n".format(repr(player2_choice)[2:-1]))
            #check if they want to reset
            if player1_choice == player2_choice and repr(data) == "b'reset'":
                print("Location 2")
                player1_choice = " "
                player2_choice = " "
                res = " "
                sockets[0].sendall(b'reset')
                sockets[1].sendall(b'reset')
            #determine if the players have both made choices
            elif player1_choice != " " and player2_choice != " ":
                print("Location 3")
                res = logic(player1_choice,player2_choice)
                player1_choice = " "
                player2_choice = " "
            #if else to determine result
            if res == "tie":
                player1_choice = " "
                player2_choice = " "
                res = " "
                sockets[0].sendall(b'tie')
                sockets[1].sendall(b'tie')
            elif res == "p1" and sockets[0] == client_sock:
                player1_choice = " "
                player2_choice = " "
                res = " "
                sockets[0].sendall(b'win')
                sockets[1].sendall(b'lose')
            elif res == "p2" and sockets[0] == client_sock:
                player1_choice = " "
                player2_choice = " "
                res = " "
                sockets[0].sendall(b'lose')
                sockets[1].sendall(b'win')
            elif res == "p1" and sockets[1] == client_sock:
                player1_choice = " "
                player2_choice = " "
                res = " "
                sockets[0].sendall(b'win')
                sockets[1].sendall(b'lose')
            elif res == "p2" and sockets[1] == client_sock:
                player1_choice = " "
                player2_choice = " "
                res = " "
                sockets[0].sendall(b'lose')
                sockets[1].sendall(b'win')
            

                
'''
This method closes the socket and the window
'''       
def end_comm():
    #globals to reference sockets and frame
    global win
    global sockets

    
    #iterates over the sockets list and closes all sockets
    for s in sockets:
        try:
            s.sendall(b'quit')
            s.close()
        except:
            print("socket already closed")
                
    try:
        #closes window
        win.destroy()    
    except:
        print("window already closed")

'''
This method takes the listening socket as a parameter and accepts two sockets
with said socket then spins up threads for both
'''
def recieve_clients(server):
    #the list of sockets
    global sockets
    #loop to iterate and accept connections
    while True:
        #check to make sure only two connections are accepted
        if len(sockets) < 2:
            #accepting connection
            client, addr = server.accept()
            #adding to list of sockets
            sockets.append(client)
    
            # using a thread so as not to clog the gui thread
            threading._start_new_thread(communicate, (client, addr))
            
       
'''
This method initializes the listener socket and spins a new thread 
to accept connections with the listener socket
'''
def start(port,ip):
    #global variables
    global win
    global server
    #creating the listener socket
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #setting the socket options to allow it to be reused
    #during time_wait period
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #binding socket to provided port and ip
    serv.bind((ip, port))
    #starts listening
    serv.listen(5)  # server is listening for client connection
    #saves to global varaible for reference later
    server = serv
    #generating log message
    log.insert(END, "Server Listening\n")
    #disabling the server start button
    st_button["state"] = "disabled"
    #spins up a new thread to accept connections
    threading._start_new_thread(recieve_clients, (serv,))

#starts the gui thread
window.mainloop()

