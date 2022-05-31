from tkinter import *
from tkinter import simpledialog
from gameboard import BoardClass
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
    

def diplayPlayer1Name(root: Tk, name: str): 
    l = Label(root, text = "Player1 Name: "+name)
    l.config(font =("Courier", 14))
    l.pack()


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
    player1Username= clientSocket.recv(1024).decode('ascii')
    diplayPlayer1Name(root, player1Username)

    # Create and send player2 username 
    player2Username = setPlayer2Name() 
    clientSocket.sendall(player2Username.encode())

    # Display Board Game with Player 1 move
    player2 = BoardClass(root, clientSocket, "O", player1Username, player2Username, player2Username)
    player1Move = clientSocket.recv(1024).decode('ascii')
    player2.setupBoardGameGUI() 
    
    print(player1Move)
    player2.updateGameBoard(player1Move, "X")

    # Play Game 
    playGame(player2, clientSocket, root) 
    
    # Closing Connection
    # clientSocket.close()
    # gameSocket.close()


def setupPlayer2GUI(): 
    frame = Tk()
    frame.title("Player 2")
    frame.geometry('500x500')

    connectToPlayer1(frame) 

    frame.mainloop()



if __name__ == '__main__':
    setupPlayer2GUI()