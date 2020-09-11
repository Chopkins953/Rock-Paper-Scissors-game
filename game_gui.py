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
import tkinter
import threading
import socket
from tkinter import *
from tkinter import messagebox
from tkinter import Entry
from functools import partial

'''
Global variables:
    user_socket is what stores the socket object
    window is to allow access to the main frame
    yes, no, result, and prompt are widgets that
    are stored to allow them to be removed and replced
'''
#global user_msg
global user_socket
global window
global yes
global no
global result
global prompt

#gui Class stores the function of the GUI
class GUI:
    #globals
    global window
    global yes
    global no
    global result
    global prompt
    
    #this function gets the port and ip then calls the public connection method
    #to initialize a socket connection
    def conn(port,ip):
        p = int(port.get())
        i = ip.get()
        connect(p,i)
    #this method removes labels and buttons made visible after the 
    #results are sent by server
    def reset():
        yes.grid_remove()
        no.grid_remove()
        result.set("")
        replay_prompt.set("")
    
    
    
    
    #this starts the gui thread
    def start(self):
        window.mainloop()
    
    #this passes the message to the server depending on what button is pressed
    def set_comm(user_in):
        global user_socket
        print("From Client: the contents are {}".format(user_in))
        if user_in == 'quit':
            end_comm()
        elif user_socket:
            user_socket.sendall(user_in.encode('utf-8'))

        
    #initialize frame
    window = tkinter.Tk()

    #set frame size
    window.geometry('300x300')
    
    #iterate over columns and rows to non-zero weight 
    #this preserves size
    for i in range(5):
        window.grid_columnconfigure(i, weight=1)

    for i in range(5):
        window.grid_rowconfigure(i, weight=1)

    
    #quit button
    w = Button(window, text = "quit", command = partial(set_comm, 'quit'))
    w.grid(row=0 ,column=4)
    #yes button
    y = Button(window, text = "yes", command = partial(set_comm, 'reset'))
    y.grid(row=2 ,column=3 )
    yes = y
    #no button
    n = Button(window, text = "no", command = partial(set_comm, 'quit'))
    n.grid(row=2 ,column=4 )
    no = n
    #ip entry
    ip = Entry(window)
    ip.grid(row=3,column=4)
    ip.insert(0, "IP address")
    #port entry
    port = Entry(window)
    port.grid(row=4,column=4)
    port.insert(0, "Port")
    #connect button
    w = Button(window, text = "connect", command = partial(conn, port, ip))
    w.grid(row=0 ,column=0)
    #label for selection area
    w = Label(window,  text = "select").grid(row=1 ,column=0 )
    #rock button
    w = Button(window, text = "rock", command = partial(set_comm, 'rock'))
    w.grid(row=2 ,column=0 )
    #paper button
    w = Button(window, text = "paper", command = partial(set_comm, 'paper'))
    w.grid(row=3 ,column=0 )
    #scissors button
    w = Button(window, text = "scissors", command = partial(set_comm, 'scissors'))
    w.grid(row=4 ,column=0 )
    #results label
    w = Label(window, text="")
    w.grid(row=5 ,column=2 )
    result = w
    #replay label
    w = Label(window, text="")
    w.grid(row=1 ,column=3 )
    prompt = w

    #removes yes and no  buttons from frame
    yes.grid_remove()
    no.grid_remove()
    
#this method sets labels and buttons to the state they were in before
#results sent from server
def reset():
    global yes
    global no
    global result
    global prompt
    
    yes.grid_remove()
    no.grid_remove()
    result['text'] = ""
    prompt['text'] = ""   

#this method displays the win condition 
def win():
    global yes
    global no
    global result
    global prompt
    
    yes.grid()
    no.grid()
    result['text'] = "You win!"
    prompt['text'] = "Play again?"

#this method displays the lose condition  
def lose():
    global yes
    global no
    global result
    global prompt
        
    yes.grid()
    no.grid()
    result['text'] = "You lose!"
    prompt['text'] = "Play again?"

#this method displays the tie condition 
def tie():
    global yes
    global no
    global result
    global prompt
    
    yes.grid()
    no.grid()
    result['text'] = "It's a Tie!"
    prompt['text'] = "Play again?"
    
#this method generates the socket and connects it to the server     
def connect(port, ip):
    
    global user_socket
   
    try:
        #creates socket and attempts connection
        player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        player.connect((ip, port))
        #sends confirmation message
        player.sendall(b'client connected')
        #sets global variable
        user_socket = player
    except Exception as e:
        print(e)
    
    #spins up thread if connection was successful
    if player:    
        threading._start_new_thread(communicate,(player,))
    else:
        print("socket failed to connect")
        
#this method handles the communication between server and client
def communicate(s):       
    
    #globals
    global user_in
    global flag
    
    #infinite loop to send/recieve messages
    while True:
        data = s.recv(1024)
        print("From Client: message is {}".format(repr(data)))
        #checks if the server sends quit message
        if repr(data) == "b'quit'":
            print("From Client: quitting")
            end_comm()
            break
        #determines what the condition is and calls appropriate method
        elif repr(data) == "b'win'":
            win()         
        elif repr(data) == "b'lose'":
            lose()
        elif repr(data) == "b'tie'":
            tie()
        elif repr(data) == "b'reset'":
            reset()
        

        
#this method handles closing the communication socket and window
def end_comm():
    #globals
    global window
    global user_socket
    print("closing communications socket")
    #sends quit message to server
    user_socket.sendall(b'quit')
    #closes socket
    user_socket.close()
    print("closing window")
    #closes window
    window.destroy()

        


    
      

  

#creates a gui object
gui = GUI()
#runs start method
gui.start()

