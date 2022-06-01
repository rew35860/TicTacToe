from tkinter import * 
from threading import *
from tkinter import simpledialog
from gameboard import BoardClass
import socket


class ClientClass: 
    def __init__(self, server): 
        # Creating Server 
        self.gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
    
    def connect(self):
        # Wait for Player2 connection
        self.gameSocket.connect((self.server[0], self.server[1]))
        print("Successfully Connected to Player2")

    def getData(self) -> str: 
        resp = self.gameSocket.recv(1024).decode('ascii')
        print("Receive data from Player2")
        return resp
    
    def sendData(self, data): 
        self.gameSocket.sendall(data.encode())
        print("Send data to Player2")


def player1Thread(target, args):
    t1 = Thread(target = target, args = args)
    t1.daemon = True
    t1.start() 


def askHostInfo() -> (str, int): 
    """ Ask Player1 about Player2 host information.

    Host information includes host name and port number. 
    (Player 1 Module Part 1)

    Returns:
        Tuple of host name (str) and port number (int).
    """

    hostNameAnswer = simpledialog.askstring("HostName", "Enter host name/IP address of Player 2")
    portAnswer = simpledialog.askinteger("Player 2 Port", "Enter Player 2's Port")

    return (hostNameAnswer, portAnswer)


def setupPlayer1Connection(c, root: Tk) -> (str, str):
    # Establish connection with Player2 
    c.connect()
    
    # Send Player 1 username to Player 2 
    player1Username = setPlayer1Name() 
    c.sendData(player1Username)

    # Display Player2 username 
    player2Username = c.getData()
    diplayPlayer2Name(root, player2Username)

    return (player1Username, player2Username)


def setPlayer1Name() -> str: 
    """ Prompt Player 1 for thier username.

    Username has to be alphanumeric username.

    Returns:
        String of the Player 1 username.
    """

    name = simpledialog.askstring("Player 1 Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Player 1 Username", "Username must be alphanumeric, please try again!")
    return name


def player1TryConnect(c, root: Tk): 
 
    l = Label(root, text = "Would you like to try reconecting?")
    l.config(font =("Courier", 14))
    
    yestBtn = Button(root, text = "Yes", command = lambda: setupPlayer1Connection(c, root) )
    noBtn = Button(root, text = "No", command = root.destroy)
    
    l.pack()
    yestBtn.pack()
    noBtn.pack()


def sendPlayAgain(player1, c, askView): 
    askView.destroy()
    player1.updateGamesPlayed()
    player1.resetGameBoard()
    player1.setLockMove(True)
    c.sendData("Play Again")


def sendExit(player1, c, root: Tk): 
    clearFrame(root)

    (player1Name, player2Name, gamePlayed, numWins, numLosses, numTies) = player1.computeStats()

    statView = Frame(root, bg = "yellow")
    statView.pack()

    l1 = Label(statView, bg = "yellow", text = "Player 1: "+player1Name)
    l2 = Label(statView, bg = "yellow", text = "Game Played: "+ str(gamePlayed))
    l3 = Label(statView, bg = "yellow", text = "Number of Wins: "+ str(numWins))
    l4 = Label(statView, bg = "yellow", text = "Number of Losses: "+ str(numLosses))
    l5 = Label(statView, bg = "yellow", text = "Number of Ties: "+ str(numTies))

    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    l5.pack()
    c.sendData("Fun Times")


def player1PlayAgain(player1, c, root: Tk): 
    askView = Frame(root)
    askView.pack()

    l = Label(askView, text = "Would you like to play again?")
    l.config(font =("Courier", 14))
    
    yestBtn = Button(askView, text = "Yes", command = lambda: sendPlayAgain(player1, c, askView))
    noBtn = Button(askView, text = "No", command = lambda: sendExit(player1, c, root))
    
    l.pack()
    yestBtn.pack()
    noBtn.pack()


def clearFrame(root: Tk): 
    for widget in root.winfo_children():
        widget.destroy()


def diplayPlayer2Name(root: Tk, name: str): 
    headerView = Frame(root)
    headerView.pack()

    l1 = Label(headerView, text = "Player2's username: "+name)
    l1.config(font =("Courier", 14))
    l1.pack()

    l2 = Label(headerView, text = "Turn: You")
    l2.config(font =("Courier", 14))
    l2.pack()


def checkForGameOver(player1) -> bool: 
    if player1.isWinner() or player1.boardIsFull():
        return True
    return False


def waitingForMove(player1, c, root: Tk): 
    while True: 
        Player2Move = c.getData()
        player1.updateGameBoard(Player2Move, "O")
        player1.setLockMove(False)

        if checkForGameOver(player1):
            player1.setLockMove(True)
            player1PlayAgain(player1, c, root)
            continue



def Player1Manager(root: Tk): 
    clearFrame(root)

    # try:
    # Player 1 Module Part 1 
    server = askHostInfo() 

    # Player 1 Module Part 2.0-2.1
    c = ClientClass(server)
    player1Username, player2Username = setupPlayer1Connection(c, root)

    # Player 1 Module Part 3
    # Display Board Game 
    player1 = BoardClass(root, c, "X", player1Username, player2Username, player2Username)
    player1.setupBoardGameGUI() 
    player1.updateGamesPlayed() 

    player1Thread(waitingForMove, (player1, c, root, ))

    # except:
    # # Player 1 Module Part 2.2
    #     player1TryConnect(root)

    # finally: 
    #     gameSocket.close()


def setupPlayer1GUI(): 
    frame = Tk()
    frame.title("Player 1")
    frame.geometry('500x500')

    Player1Manager(frame)

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer1GUI()