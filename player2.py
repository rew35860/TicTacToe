from tkinter import *
from threading import *
from tkinter import simpledialog
from gameboard import BoardClass
import socket

class ServerClass: 
    """
    A class for main server

    Attributes
    ----------
    gameSocket : socket 
        creating socket 
    clientSocket : socket 
        socket to communicate with the client (Player1)
    clientAddress : socket 
        client ip address 

    Methods
    -------
    connect()
        connect main server to a client server 
    
    closeConnection() 
        close server connection 
    
    getData() 
        get data from the client 

    sendData()
        send data to the client
    
    playerThread() 
        create and start thread 
    """

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
    """ Ask Player2 about Player1 host information.

    Host information includes host name and port number. 
    (Player 2 Module Part 1)

    Returns:
        Tuple of host name (str) and port number (int).
    """

    hostNameAnswer = simpledialog.askstring("HostName", "Enter host name/IP address of Player 2")
    portAnswer = simpledialog.askinteger("Player 2 Port", "Enter Player 2's Port")

    return (hostNameAnswer, portAnswer)


def setupPlayer2Connection() -> ServerClass:
    """ Creating Player2 server 

    Returns:
        ServerClass: dealing with socket calls 
    """
    
    # Ask the host information
    server = askHostInfo() 
    s = ServerClass(server)

    # Establish connection with Player1
    s.connect()
    return s


def getPlayer1Username(s: ServerClass, root: Tk) -> str: 
    """ get player1 username and calling displayPlayer1Name function

    Args:
        s (ServerClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 

    Returns:
        str: player1 username 
        turnLabel: player2's turn 
    """

    player1Username = s.getData() 
    turnLabel = displayPlayer1Name(root, player1Username)

    return player1Username, turnLabel


def displayPlayer1Name(root: Tk, name: str): 
    """ Display Player1 username and player2's turn 

    Args:
        root (Tk): tkinter main frame for adding GUI components 
        name (str): player1 username

    Returns:
        tk label: turn label
    """

    headerView = Frame(root)
    headerView.pack()

    l1 = Label(headerView, text = "Player1's username: "+name)
    l1.config(font =("Courier", 14))
    l1.pack()

    l2 = Label(headerView, text = "Turn: Opponent")
    l2.config(font =("Courier", 14))
    l2.pack()

    return l2


def setPlayer2Username() -> str: 
    """ Prompt Player2 for thier username.

    Username has to be alphanumeric username.

    Returns:
        str : Player2 username.
    """

    name = simpledialog.askstring("Player 2 Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Player 2 Username", "Username must be alphanumeric, please try again!")
    return name


def sendPlayer2Username(s: ServerClass) -> str: 
    """ Send player2 username to player1

    Args:
        s (ServerClass): dealing with socket calls

    Returns:
        str: player2 username
    """

    # Create and send player2 username 
    player2Username = setPlayer2Username()
    s.sendData(player2Username)
    
    return player2Username


def setupPlayer2BoardGame(s: ServerClass, root: Tk, turnLabel, player1Username: str, player2Username: str) -> BoardClass:
    """ setup player2 board game with player1's first move

    Args:
        s (ServerClass): dealing with socket calls
        root (Tk): tkinter main frame for adding GUI components 
        turnLabel (_type_): player2's turn 
        player1Username (str): player1 username
        player2Username (str): player2 username

    Returns:
        BoardClass: board game object for player2 
    """

    # setup board game
    player2 = BoardClass(root, s, "O", turnLabel, player1Username, player2Username, player2Username)
    player1Move = s.getData()
    turnLabel.config(text = "Turn: You")

    player2.setupBoardGameGUI() 
    player2.updateGameBoard(player1Move, "X")

    return player2


def displayStat(player2: BoardClass, root: Tk): 
    """ Display Stat at the end of the game 

    Args:
        player2 (BoardClass): dealing with gameboard function calls 
        root (Tk): tkinter main frame for adding GUI components 
    """

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
    """ clear the main GUI

    Args:
        root (Tk): tkinter main frame for adding GUI components 
    """

    for widget in root.winfo_children():
        widget.destroy()


def playGame(player2: BoardClass, s: ServerClass, root: Tk, turnLabel): 
    """ Play the game by waiting for player1 moves and check if game is over 

    Args:
        player2 (BoardClass): dealing with gameboard function calls 
        s (ServerClass): dealing with socket calls 
        root (Tk): tkinter main frame for adding GUI components 
        turnLabel (tk label): label for player1 turn
    """

    while True: 
        player1Move = s.getData()

        if player1Move == "Play Again": 
            player2.updateGamesPlayed()
            player2.resetGameBoard()
            turnLabel.config(text = "Turn: Opponent")
            player2.setLockMove(True)

        elif player1Move == "Fun Times": 
            displayStat(player2, root)
            
            # Closing Connection
            s.closeConnection()
            break

        else: 
            player2.updateGameBoard(player1Move, "X")
            player2.setLockMove(False)
            turnLabel.config(text = "Turn: You")

        if player2.checkForGameOver():
            turnLabel.config(text = "Turn: Game Over")
            player2.setLockMove(True)
            s.sendData("Game Over")
            continue


def player2Manager(root: Tk): 
    """ Connecting with Player1 and playing the game

    Args:
        root (Tk): tkinter main frame for adding GUI components 
    """

    clearFrame(root)
    
    # Player 2 Module Part 1 & 2 
    s = setupPlayer2Connection()

    # Player 2 Module Part 3
    player1Username, turnLabel = getPlayer1Username(s, root)

    # Player 2 Module Part 4.0
    player2Username = sendPlayer2Username(s)

    # Player 2 Module Part 4.1 
    player2 = setupPlayer2BoardGame(s, root, turnLabel, player1Username, player2Username)
    player2.updateGamesPlayed()

    # Play Game
    s.playerThread(playGame, (player2, s, root, turnLabel, ))


def setupPlayer2Game(): 
    """ Creating tkinter window and calling player2Manager 
    """

    frame = Tk()
    frame.title("Player 2")
    frame.geometry('500x500')

    player2Manager(frame) 

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer2Game()