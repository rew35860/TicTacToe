from tkinter import *
from threading import *
from tkinter import simpledialog
from gameboard import BoardClass
import socket

class ServerClass: 
    def __init__(self, server): 
        # Creating Server 
        self.gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameSocket.bind((server[0], server[1]))
        self.clientSocket = None
        self.clientAddress = None
    
    def connect(self):
        # Wait for Player 1 connection
        self.gameSocket.listen(1024)
        self.clientSocket, self.clientAddress = self.gameSocket.accept()
        print("Successfully Connected to Player1")

    def closeConnection(self):
        self.clientSocket.close()
        self.gameSocket.close()
        print("Successfully Closed Connection with Player1")

    def getData(self) -> str: 
        resp = self.clientSocket.recv(1024).decode('ascii')
        print("Receive data from Player1")
        return resp
    
    def sendData(self, data): 
        self.clientSocket.sendall(data.encode())
        print("Send data to Player2")

    def playerThread(self, target, args) -> Thread:
        t1 = Thread(target = target, args = args)
        t1.daemon = True
        t1.start() 
        return t1 


def askHostInfo() -> (str, int): 
    hostNameAnswer = simpledialog.askstring("HostName", "Enter host name/IP address of Player 2")
    portAnswer = simpledialog.askinteger("Player 2 Port", "Enter Player 2's Port")

    return (hostNameAnswer, portAnswer)


def setupPlayer2Connection() -> ServerClass:
    
    # Ask the host information
    server = askHostInfo() 
    s = ServerClass(server)

    # Establish connection with Player1
    s.connect()
    return s


def diplayPlayer1Name(root: Tk, name: str): 
    headerView = Frame(root)
    headerView.pack()

    l1 = Label(headerView, text = "Player1's username: "+name)
    l1.config(font =("Courier", 14))
    l1.pack()

    l2 = Label(headerView, text = "Turn: Opponent")
    l2.config(font =("Courier", 14))
    l2.pack()

    return l2


def getPlayer1Username(s, root: Tk) -> str: 
    player1Username = s.getData() 
    turnBtn = diplayPlayer1Name(root, player1Username)

    return player1Username, turnBtn


def setPlayer2Username() -> str: 
    name = simpledialog.askstring("Player 2 Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Player 2 Username", "Username must be alphanumeric, please try again!")
    return name


def sendPlayer2Username(s) -> str: 
    # Create and send player2 username 
    player2Username = setPlayer2Username()
    s.sendData(player2Username)
    
    return player2Username


def setupPlayer2BoardGame(s, root: Tk, turnBtn, player1Username, player2Username) -> BoardClass:
    # setup board game
    player2 = BoardClass(root, s, "O", turnBtn, player1Username, player2Username, player2Username)
    player1Move = s.getData()
    turnBtn.config(text = "Turn: You")

    player2.setupBoardGameGUI() 
    player2.updateGameBoard(player1Move, "X")

    return player2


def displayStat(player2, root: Tk): 
    clearFrame(root)

    (player1Name, player2Name, gamePlayed, numWins, numLosses, numTies) = player2.computeStats()

    statView = Frame(root, bg = "yellow")
    statView.pack()

    l1 = Label(statView, bg = "yellow", text = "Player 2: "+player2Name)
    l2 = Label(statView, bg = "yellow", text = "Game Played: "+ str(gamePlayed))
    l3 = Label(statView, bg = "yellow", text = "Number of Wins: "+ str(numWins))
    l4 = Label(statView, bg = "yellow", text = "Number of Losses: "+ str(numLosses))
    l5 = Label(statView, bg = "yellow", text = "Number of Ties: "+ str(numTies))

    l1.pack()
    l2.pack()
    l3.pack()
    l4.pack()
    l5.pack()


def clearFrame(root: Tk): 
    for widget in root.winfo_children():
        widget.destroy()


def checkForGameOver(player2) -> bool: 
    if player2.isWinner() or player2.boardIsFull():
        return True
    return False


def playGame(player2, s, root: Tk, turnBtn): 
    while True: 
        player1Move = s.getData()

        if player1Move == "Play Again": 
            player2.updateGamesPlayed()
            player2.resetGameBoard()
            turnBtn.config(text = "Turn: Opponent")
            player2.setLockMove(True)

        elif player1Move == "Fun Times": 
            displayStat(player2, root)
            
            # Closing Connection
            s.closeConnection()
            break

        else: 
            player2.updateGameBoard(player1Move, "X")
            player2.setLockMove(False)
            turnBtn.config(text = "Turn: You")

        if player2.checkForGameOver():
            turnBtn.config(text = "Turn: Game Over")
            player2.setLockMove(True)
            s.sendData("Game Over")
            continue


def player2Manager(root: Tk): 
    clearFrame(root)
    
    # Player 2 Module Part 1 & 2 
    s = setupPlayer2Connection()

    # Player 2 Module Part 3
    player1Username, turnBtn = getPlayer1Username(s, root)

    # Player 2 Module Part 4.0
    player2Username = sendPlayer2Username(s)

    # Player 2 Module Part 4.1 
    player2 = setupPlayer2BoardGame(s, root, turnBtn, player1Username, player2Username)
    player2.updateGamesPlayed()

    s.playerThread(playGame, (player2, s, root, turnBtn, ))


def setupPlayer2Game(): 
    frame = Tk()
    frame.title("Player 2")
    frame.geometry('500x500')

    player2Manager(frame) 

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer2Game()