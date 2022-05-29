from tkinter import *
from tkinter import simpledialog
import socket


def setPlayer2Server() -> (str, int): 

    hostNameAnswer = simpledialog.askstring("HostName", "Enter host name/IP address of Player 2")
    portAnswer = simpledialog.askinteger("Player 2 Port", "Enter Player 2's Port")

    return (hostNameAnswer, portAnswer)


def setPlayer2Name() -> str: 
    name = simpledialog.askstring("Player 2 Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Player 2 Username", "Username must be alphanumeric, please try again!")
    return name


def clearFrame(root: Tk): 
    for widget in root.winfo_children():
        widget.destroy()


def waitingScreen(root: Tk): 
    canvas = Canvas(root)    
    canvas.pack()
    canvas_text = canvas.create_text(140, 150, text='')

    staticStr = "Waiting"
    animatedStr = "......"

    #Time delay between chars, in milliseconds
    delta = 200 
    delay = 0
    for i in range(len(animatedStr) + 1):
        s = animatedStr[:i]
        update_text = lambda s=s: canvas.itemconfigure(canvas_text, text=staticStr+s)
        canvas.after(delay, update_text)
        delay += delta
    

def diplayPlayer1Name(root: Tk, name: str): 
    l = Label(root, text = "Player1 Name: "+name)
    l.config(font =("Courier", 14))
    l.pack()


def connectToPlayer1(root: Tk): 
    clearFrame(root)
    
    # Player 2 provides host information including: 
    # host name, port number, thier username 
    server = setPlayer2Server() 
    gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gameSocket.bind((server[0], server[1]))

    # Wait for Player 1 connection
    gameSocket.listen(1024)
    clientSocket, clientAddress = gameSocket.accept()

    # Receive player1 username 
    player1Name = clientSocket.recv(1024).decode('ascii')
    diplayPlayer1Name(root, player1Name)

    # Create and send player2 username 
    player2Username = setPlayer2Name() 
    clientSocket.sendall(player2Username.encode())


def setupPlayer2GUI(): 
    frame = Tk()
    frame.title("Player 2")
    frame.geometry('500x500')

    connectToPlayer1(frame) 
    # waitingScreen(frame)

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer2GUI()