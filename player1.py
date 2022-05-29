from tkinter import * 
from tkinter import simpledialog
from gameboard import BoardClass
import socket

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
    l = Label(root, text = "Player2 Name: "+name)
    l.config(font =("Courier", 14))
    l.pack()


def changeYourMoveText(player1, gameSocket, label, button, isWaiting: bool): 
    yourTurnText = "It's your turn!"
    waitText = "Waiting for Player2's move"

    label.config(text = waitText if isWaiting else yourTurnText)
    button.config(text = "Get Player2 move" if isWaiting else "Send Your Move")


def sendMoveAction(player1, gameSocket, label, button, isWaiting: bool): 
    if player1.moveIsAvalible():
        print("move")
        if not player1.getLockMove():
            print("no move")
            player1Move = player1.getMove()
            gameSocket.sendall(player1Move.encode())

            player1.setLockMove(True)
            player1.updateGameBoard(player1Move, "X")

            changeYourMoveText(player1, gameSocket, label, button, isWaiting)
        else: 
            print("?? move")
            Player2Move = gameSocket.recv(1024).decode('ascii')
            player1.updateGameBoard(Player2Move, "O")
            
            player1.setLockMove(False)
            changeYourMoveText(player1, gameSocket, label, button, False)
    else: 
        player1.setLockMove(False)



def setupPlayComponents(player1, gameSocket, root: Tk): 
    l = Label(root, text = "It's your turn!")
    l.config(font =("Courier", 14))
    sendMove = Button(root, text = "Send Your Move", 
                                                command = lambda: 
                                                sendMoveAction(player1, gameSocket, 
                                                                                l, sendMove, True))

    l.pack()
    sendMove.pack()


def playGame(player1, gameSocket, root: Tk): 
    setupPlayComponents(player1, gameSocket, root) 

    # playing = True
    # while playing: 
        # Waiting for Player2 Move 
    # print(player1.getLockMove())
    # print("waiting...")
        # try: 
    # Player2Move = gameSocket.recv(1024).decode('ascii')
    # player1.updateGameBoard(Player2Move, "Y")
    # player1.setLockMove()
    # changeYourMoveText(player1, gameSocket, label, button, False)
    # playing = False
        # except EOFError:
        #     print("Connection closed")
        #     break








def connectToPlayer2(root: Tk): 
    clearFrame(root)

    # try:
    # Connecting to Player 2 
    server = setPlayer1Server() 
    gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gameSocket.connect((server[0], server[1]))

    # Send Player 1 username to Player 2 
    player1Username = setPlayer1Name() 
    gameSocket.sendall(player1Username.encode())

    # Receive Player 2 username 
    player2Username = gameSocket.recv(1024).decode('ascii')
    diplayPlayer2Name(root, player2Username)

    # Display Board Game 
    player1 = BoardClass(root, "X", player1Username, player2Username, player2Username)
    player1.setupBoardGameGUI() 

    # Play Game 
    playGame(player1, gameSocket, root) 

    # except:
    #     player1TryConnect(root)

    # finally: 
    #     gameSocket.close()

def setupPlayer1GUI(): 
    frame = Tk()
    frame.title("Player 1")
    frame.geometry('500x500')

    connectToPlayer2(frame)

    frame.mainloop()


if __name__ == '__main__':
    setupPlayer1GUI()