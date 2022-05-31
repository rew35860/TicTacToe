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

    def getData(self) -> str: 
        resp = self.clientSocket.recv(1024).decode('ascii')
        print("Receive data from Player1")
        return resp
    
    def sendData(self, data): 
        self.clientSocket.sendall(data.encode())
        print("Send data to Player2")


def player2Thread(target, args):
    t1 = Thread(target = target, args = args)
    t1.daemon = True
    t1.start() 


def setupPlayer2(s, root):
    # setup connection
    # Establish connection with Player1 and receive Player1 username
    s.connect()
    player1Username = s.getData()

    # Display Player1 username 
    clearFrame(root)
    diplayPlayer1Name(root, player1Username)

    # Create and send player2 username 
    player2Username = setPlayer2Name() 
    s.sendData(player2Username)

    # setup board game
    player2 = BoardClass(root, s, "O", player1Username, player2Username, player2Username)
    player1Move = s.getData()

    player2.setupBoardGameGUI() 
    player2.updateGameBoard(player1Move, "X")


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
    

def diplayPlayer1Name(root: Tk, name: str): 
    l = Label(root, text = "Player1's username: "+name)
    l.config(font =("Courier", 14))
    l.pack()


def displayWaitingScreen(root: Tk):
    canvas = Canvas(root)
    canvas.pack()

    canvasText = canvas.create_text(150, 120, text='')

    staticString = "Waiting for Player1"
    animatedString = "........."

    #Time delay between chars, in milliseconds
    delta = 500 
    delay = 0

    for i in range(len(animatedString) + 1):
        s = animatedString[:i]
        updateText = lambda s = s: canvas.itemconfigure(canvasText, text=staticString+s)
        canvas.after(delay, updateText)
        delay += delta


def changeYourMoveText(player2, gameSocket, label, button, isWaiting: bool): 
    yourTurnText = "It's your turn!"
    waitText = "Waiting for Player1's move"

    label.config(text = waitText if isWaiting else yourTurnText)
    button.config(text = "Get Player1 Move" if isWaiting else "Send Your Move")


def sendMoveAction(player2, gameSocket): 
    if player2.getLockMove():
        Player1Move = gameSocket.recv(1024).decode('ascii')
        player2.updateGameBoard(Player1Move, "X")
        
        player2.setLockMove(False)


def setupPlayComponents(player2, gameSocket, root: Tk): 
    sendMove = Button(root, text = "Send Your Move", 
                                                command = lambda: 
                                                sendMoveAction(player2, gameSocket))
    sendMove.pack()


def playGame(player2, gameSocket, root: Tk): 
    # Player1Move = gameSocket.recv(1024).decode('ascii')
    # setupPlayComponents(player2, gameSocket, root) 

    # while True: 
    print("waiting...")
    # Player1Move = gameSocket.recv(1024).decode('ascii')
    # player2.updateGameBoard(Player1Move, "X")
    # player2.setLockMove()
    # changeYourMoveText(player2, gameSocket, label, button, False)



def player2Manager(root: Tk): 
    clearFrame(root)
    
    server = setPlayer2Server() 
    s = ServerClass(server)

    player2Thread(setupPlayer2, (s, root, ))
    displayWaitingScreen(root)

    # Display Board Game with Player 1 move
    # player2 = BoardClass(root, clientSocket, "O", player1Username, player2Username, player2Username)
    # player1Move = clientSocket.recv(1024).decode('ascii')
    # player2.setupBoardGameGUI() 

    # print(player1Move)
    # player2.updateGameBoard(player1Move, "X")

    # # Play Game 
    # playGame(player2, clientSocket, root) 
    
    # # Closing Connection
    # # clientSocket.close()
    # # gameSocket.close()


def setupPlayer2GUI(): 
    frame = Tk()
    frame.title("Player 2")
    frame.geometry('500x500')

    player2Manager(frame) 

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer2GUI()