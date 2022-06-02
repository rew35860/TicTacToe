from tkinter import * 
from threading import *
from tkinter import simpledialog
from gameboard import BoardClass
import socket


class ClientClass: 
    """
    A class for client server 

    Attributes
    ----------
    gameSocket : socket 
        creating socket 
    server : (str, int)
        host information including host name and port number 

    Methods
    -------
    connect()
        connect client server to main server 
    
    closeConnection() 
        close client connection 
    
    getData() 
        get data from the main server 

    sendData()
        send data to the main server 
    
    playerThread() 
        create and start thread 
    """

    def __init__(self, server): 
        # Creating Server 
        self.gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server

    def connect(self):
        # Wait for Player2 connection
        self.gameSocket.connect((self.server[0], self.server[1]))
        print("Successfully Connected to Player2")

    def closeConnection(self): 
        self.gameSocket.close() 
        print("Successfully Closed Connection with Player2")

    def getData(self) -> str: 
        resp = self.gameSocket.recv(1024).decode('ascii')
        print("Receive Data from Player2")
        return resp
    
    def sendData(self, data): 
        self.gameSocket.sendall(data.encode())
        print("Send Data to Player2")
    
    def playerThread(self, target, args):
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


def setPlayer1Name() -> str: 
    """ Prompt Player1 for thier username.

    Username has to be alphanumeric username.

    Returns:
        str : Player1 username.
    """

    name = simpledialog.askstring("Player1 Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Player1 Username", "Username must be alphanumeric, please try again!")
    return name


def displayPlayer2Name(root: Tk, name: str): 
    """ Display player2 username and player1's turn 

    Args:
        root (Tk): tkinter main frame for adding GUI components 
        name (str): player2 username

    Returns:
        tk label: turn label
    """
    headerView = Frame(root)
    headerView.pack()

    l1 = Label(headerView, text = "Player2's username: "+name)
    l1.config(font =("Courier", 14))
    l1.pack()

    l2 = Label(headerView, text = "Turn: You")
    l2.config(font =("Courier", 14))
    l2.pack()

    return l2


def setupPlayer1Connection(c: ClientClass, root: Tk) -> (str, str):
    """ Setup player1 connection with player2 

    1. connect to player2 server 
    2. send player1 username to player2 
    3. receive player2 username and display on the screen

    Args:
        c (ClientClass) : dealing with socket calls 
        root (Tk) : the tkinter main frame

    Returns:
        (str, str, btn) : player1 username, player2 username, turn button 
    """

    # Establish connection with Player2 
    c.connect()
    
    # Send Player 1 username to Player 2 
    player1Username = setPlayer1Name() 
    c.sendData(player1Username)

    # Display Player2 username 
    player2Username = c.getData()
    turnLabel = displayPlayer2Name(root, player2Username)

    return (player1Username, player2Username, turnLabel)


def closePlayer1Connection(c: ClientClass, root: Tk):
    """close connection with Player2

    Args:
        c (ClientClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
    """

    root.destroy
    c.closeConnection()


def player1TryConnect(c: ClientClass, root: Tk): 
    """ Retry connecting to Player2

    Args:
        c (ClientClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
    """

    # setup label 
    l = Label(root, text = "Would you like to try reconecting?")
    l.config(font =("Courier", 14))
    
    # setup buttons
    yestBtn = Button(root, text = "Yes", command = lambda: player1Manager(root))
    noBtn = Button(root, text = "No", command = lambda: closePlayer1Connection(c, root))
    
    l.pack()
    yestBtn.pack()
    noBtn.pack()


def sendPlayAgain(player1: BoardClass, c: ClientClass, root:Tk, askView, turnLabel): 
    """ Player1 wants to play again 

    Args:
        player1 (BoardClass): dealing with gameboard function calls 
        c (clientClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
        askView (Tk frame): view container of the askToPlayAgain function
        turnLabel (Tk button): label for player1 turn
    """

    askView.destroy()
    player1.updateGamesPlayed()
    player1.resetGameBoard()
    player1.setLockMove(False)
    
    c.sendData("Play Again")
    turnLabel.config(text = "Turn: You")
    c.playerThread(playGame, (player1, c, root, turnLabel, ))


def displayStat(player1: BoardClass, c: ClientClass, root: Tk): 
    """ Display stat at the end of the program 

    Args:
        player1 (BoardClass): dealing with gameboard function calls 
        c (ClientClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
    """

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
    c.closeConnection()


def askToPlayAgain(player1: BoardClass, c: ClientClass, root: Tk, turnLabel): 
    """ Ask Player1 to play again or quite the game 
    
    Args:
        player1 (BoardClass): dealing with gameboard function calls 
        c (ClientClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
        turnLabel (tk label): label for player1 turn
    """

    askView = Frame(root)
    askView.pack()

    l = Label(askView, text = "Would you like to play again?")
    l.config(font =("Courier", 14))
    
    yestBtn = Button(askView, text = "Yes", command = lambda: sendPlayAgain(player1, c, root, askView, turnLabel))
    noBtn = Button(askView, text = "No", command = lambda: displayStat(player1, c, root))
    
    l.pack()
    yestBtn.pack()
    noBtn.pack()


def clearFrame(root: Tk): 
    """ clear the current frame of the game 

    Args:
        root (Tk): tkinter main frame for adding GUI components 
    """

    for widget in root.winfo_children():
        widget.destroy()


def playGame(player1: BoardClass, c: ClientClass, root: Tk, turnLabel): 
    """ Play the game by waiting for player2 moves and check if game is over 

    Args:
        player1 (BoardClass): dealing with gameboard function calls 
        c (ClientClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
        turnLabel (tk label): label for player1 turn
    """

    while True: 
        player2Move = c.getData()
        player1.updateGameBoard(player2Move, "O")
        player1.setLockMove(False)
        turnLabel.config(text = "Turn: You")

        if player2Move == "Game Over" or player1.checkForGameOver():
            player1.setLockMove(True)
            turnLabel.config(text = "Turn: Game Over")
            askToPlayAgain(player1, c, root, turnLabel)
            break


def player1Manager(root: Tk): 
    """ Connecting with Player2 and playing the game

    Args:
        root (Tk): tkinter main frame for adding GUI components 
    """

    clearFrame(root)

    try:
        # Player 1 Module Part 1 
        server = askHostInfo() 

        # Player 1 Module Part 2.0-2.1
        c = ClientClass(server)
        player1Username, player2Username, turnLabel = setupPlayer1Connection(c, root)

        # Player 1 Module Part 3
        # Display Board Game 
        player1 = BoardClass(root, c, "X", turnLabel, player1Username, player2Username, player2Username)
        player1.setupBoardGameGUI() 
        player1.updateGamesPlayed() 

        # Playing the game
        c.playerThread(playGame, (player1, c, root, turnLabel))

    except:
        # Player 1 Module Part 2.2
        player1TryConnect(c, root)


def setupPlayer1Game(): 
    """ Creating tkinter window and calling player1Manager 
    """
    
    frame = Tk()
    frame.title("Player 1")
    frame.geometry('500x500')

    player1Manager(frame)

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer1Game()