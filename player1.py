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


def setUpConnection(c, root):
    # Establish connection with Player2 
    c.connect()
    
    # Send Player 1 username to Player 2 
    player1Username = setPlayer1Name() 
    c.sendData(player1Username)

    # Display Player2 username 
    player2Username = c.getData()
    diplayPlayer2Name(root, player2Username)


def setPlayer1Server() -> (str, int): 
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
    """ Prompt Player 1 for thier username.

    Username has to be alphanumeric username.

    Returns:
        String of the Player 1 username.
    """

    name = simpledialog.askstring("Player 1 Username", "Enter your alphanumeric Username")
    while not(name.isalnum()):
       name = simpledialog.askstring("Player 1 Username", "Username must be alphanumeric, please try again!")
    return name


def player1TryConnect(root: Tk): 
 
    l = Label(root, text = "Would you like to try reconecting?")
    l.config(font =("Courier", 14))
    
    yestBtn = Button(root, text = "Yes", command = lambda: connectToPlayer2(root) )
    noBtn = Button(root, text = "No", command = root.destroy)
    
    l.pack()
    yestBtn.pack()
    noBtn.pack()


def clearFrame(root: Tk): 
    for widget in root.winfo_children():
        widget.destroy()


def diplayPlayer2Name(root: Tk, name: str): 
    l = Label(root, text = "Player2's username: "+name)
    l.config(font =("Courier", 14))
    l.pack()


def changeYourMoveText(player1, gameSocket, label, button, isWaiting: bool): 
    yourTurnText = "It's your turn!"
    waitText = "Waiting for Player2's move"

    label.config(text = waitText if isWaiting else yourTurnText)
    button.config(text = "Get Player2 move" if isWaiting else "Send Your Move")


def sendMoveAction(player1, gameSocket, button, isWaiting: bool): 
    if player1.getLockMove():
        Player2Move = gameSocket.recv(1024).decode('ascii')
        player1.updateGameBoard(Player2Move, "O")
        
        player1.setLockMove(False)


def setupPlayComponents(player1, gameSocket, root: Tk): 
    sendMove = Button(root, text = "Get Player2 Move", 
                                                command = lambda: 
                                                sendMoveAction(player1, gameSocket, 
                                                                            sendMove, True))
    sendMove.pack()


def playGame(player1, gameSocket, root: Tk): 
    # t1 = Thread(target = listeningForPlayer2(gameSocket))
    # t1.daemon = True
    # t1.start() 
    print("work?")


def listeningForPlayer2(gameSocket): 
    # while True: 
        # print("in listening 1")
        # Player2Move = gameSocket.recv(1024).decode('ascii')
        # print(Player2Move)
        # if Player2Move != "": 
        #     break 
    for i in range(100):
        # sleep(5)
        print(i)


def Player1Manager(root: Tk): 
    clearFrame(root)

    # try:
    # Connecting to Player 2 
    server = setPlayer1Server() 
    c = ClientClass(server)
    setUpConnection(c, root)

    # Display Board Game 
    player1 = BoardClass(root, c, "X", player1Username, player2Username, player2Username)
    player1.setupBoardGameGUI() 

    # Play Game 
    playGame(player1, gameSocket, root) 
    # t1 = Thread(target = listeningForPlayer2(gameSocket))
    # t1.daemon = True
    # t1.start() 

    # except:
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