from tkinter import *
from tkinter import simpledialog
import socket

def setPlayer1Questions() -> (str, int): 
    hostNameAnswer = simpledialog.askstring("HostName", "Enter host name/IP address of Player 2")
    portAnswer = simpledialog.askinteger("Player 2 Port", "Enter Player 2's Port")

    return (hostNameAnswer, portAnswer)

def setPlayer1Name() -> str: 
    name = simpledialog.askstring("Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Username", "Username must be alphanumeric, please try again!")
    return name

def play(): 
    frame = Tk()
    frame.title("Player 1")
    frame.geometry('500x500')

    server = setPlayer1Questions() 
    player1Username = setPlayer1Name() 

    try:
        gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        gameSocket.connect((server[0], server[1]))
        #Try to send name and info
        gameSocket.sendall(player1Username.encode())
        # #Listen for player 2 name and create obj
        # player2Name = gameSocket.recv(1024).decode('ascii')
        # print('Opponent:', player2Name)
        # #Create BoardClass object for player1
        # #defaulted Player 2 as last so that player 1 can be next
        # player1 = BoardClass(name, player2Name, player2Name)
        # player1.incrementGame()
        # #plays game
        # play(player1, gameSocket, 1)
        # player1.printStats()
    except:
        # if tryAgain():
        #     tryConnect()
        print("hi")
    finally:
        gameSocket.close()

    frame.mainloop()


if __name__ == '__main__':
    play()