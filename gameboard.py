from tkinter import * 
from tkinter import simpledialog


class BoardClass: 
    def __init__(self, root: Tk, gameSocket, marker: str, turnBtn, player1Name: str = "", player2Name: str = "", 
                                lastPlayerName: str = "", numWins: int = 0, 
                                numTies: int = 0, numlosses: int = 0):
        self.player1Name = player1Name 
        self.player2Name = player2Name 
        self.lastPlayerName = lastPlayerName
        self.numWins = numWins
        self.numTies = numTies
        self.numlosses = numlosses
        self.gamePlayed = 0 
        self.frame = root 
        self.turnBtn = turnBtn

        self.gameSocket = gameSocket
        self.marker = marker
        self.move = ""
    
        self.lockMove = False

        self.allMoves = []
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.buttonBoard = [' ',' ',' ',' ',' ',' ',' ',' ',' ']


    def setLastPlayer(self, name): 
        self.lastPlayerName = name 
    

    def getLastPlayer(self, name): 
        return self.lastPlayerName 


    def getMove(self): 
        return self.move 


    def setLockMove(self, lock: bool):
        self.lockMove = lock


    def checkForGameOver(self) -> bool: 
        if self.isWinner() or self.boardIsFull():
            self.turnBtn.config(text = "Turn: Game Over")
            return True
        return False


    def buttonClicked(self, button, name: str): 
        if not self.lockMove and name not in self.allMoves:
            button["text"] = self.marker
            self.previousBtn = button
            self.move = name
            self.gameSocket.sendData(self.move)
            self.turnBtn.config(text = "Turn: Opponent")

            self.updateGameBoard(name, self.marker)
            self.setLockMove(True)

            self.checkForGameOver()


    def setupBoardGameGUI(self): 
        print("set up board game")
        # Creating a Frame as a container for buttons 
        boardGameViewRow1 = Frame(self.frame)
        boardGameViewRow1.pack()
        
        boardGameViewRow2  = Frame(self.frame)
        boardGameViewRow2.pack()
        
        boardGameViewRow3  = Frame(self.frame)
        boardGameViewRow3.pack()

        # Adding Buttons 
        b1=Button(boardGameViewRow1,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b1, "b1"))
        b2=Button(boardGameViewRow1,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b2, "b2"))
        b3=Button(boardGameViewRow1,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b3, "b3"))
        b4=Button(boardGameViewRow2,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b4, "b4"))
        b5=Button(boardGameViewRow2,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b5, "b5"))
        b6=Button(boardGameViewRow2,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b6, "b6"))
        b7=Button(boardGameViewRow3,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b7, "b7"))
        b8=Button(boardGameViewRow3,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b8, "b8"))
        b9=Button(boardGameViewRow3,text="",height=4,width=8,bg="black",font="Times 15 bold",command=lambda: self.buttonClicked(b9, "b9"))

        b1.pack(side=LEFT)
        b2.pack(side=LEFT)
        b3.pack(side=LEFT)

        b4.pack(side=LEFT)
        b5.pack(side=LEFT)
        b6.pack(side=LEFT)

        b7.pack(side=LEFT)
        b8.pack(side=LEFT)
        b9.pack(side=LEFT)

        self.buttonBoard[0] = b1
        self.buttonBoard[1] = b2
        self.buttonBoard[2] = b3

        self.buttonBoard[3] = b4
        self.buttonBoard[4] = b5
        self.buttonBoard[5] = b6

        self.buttonBoard[6] = b7
        self.buttonBoard[7] = b8
        self.buttonBoard[8] = b9

        # Making the boardGameView in the center of the screen 
        self.frame.columnconfigure(1, weight=1)  
        self.frame.columnconfigure(2, weight=1)  
        self.frame.rowconfigure(0, weight=1)    
        self.frame.rowconfigure(2, weight=1)


    def updateGamesPlayed(self): 
        self.gamePlayed += 1 


    def resetGameBoard(self):
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.allMoves.clear()

        for i in self.buttonBoard:
            i["text"] = ""


    def updateGameBoard(self, move, marker):
        self.allMoves.append(move)

        for i in range(9): 
            if move[-1] == str(i+1): 
                if i  < 3: 
                    self.board[0][i] = marker
                elif 3 <= i < 6: 
                    self.board[1][i-3] = marker
                elif 6 <= i < 9: 
                    self.board[2][i-6] = marker
                
                self.buttonBoard[i]["text"] = marker if self.buttonBoard[i]["text"] == "" else self.buttonBoard[i]["text"]


    def isWinner(self) -> bool: 
        for i in range(3):
            # Check horizontal
            if self.board[i][0] == self.board[i][1] == self.board[i][2] \
                and self.board[i][0] != " ":
                
                print("1")
                if self.board[i][0] == self.marker:
                    print("1.2")
                    self.numWins += 1
                else: 
                    print("1.3")
                    self.numlosses += 1 
                return True
            
            # Check vertical
            if self.board[0][i] == self.board[1][i] == self.board[2][i] \
                and self.board[0][i] != " ":
                
                print("2")
                if self.board[0][i] == self.marker:
                    print("2.2")
                    self.numWins += 1
                else: 
                    print("2.3")
                    self.numlosses += 1 
                return True
            
            # Check diagonals
            if self.board[0][0] == self.board[1][1] == self.board[2][2] \
                and self.board[0][0] != " ":
                
                print("3")
                if self.board[0][0] == self.marker:
                    print("3.2")
                    self.numWins += 1
                else: 
                    print("3.3")
                    self.numlosses += 1 
                return True
            
            if self.board[2][0] == self.board[1][1] == self.board[0][2] \
                and self.board[2][0] != " ":
                
                print("4")
                if self.board[2][0] == self.marker:
                    print("4.1")
                    self.numWins += 1
                else: 
                    print("4.2")
                    self.numlosses += 1 
                return True
        
        return False


    def boardIsFull(self) -> bool: 
        if " " not in self.board[0] and " " not in self.board[1] and " " not in self.board[2]:
            self.numTies += 1 
            return True
        else:
            return False
        

    def computeStats(self) -> str: 
        return (self.player1Name, self.player2Name, self.gamePlayed, self.numWins, self.numlosses, self.numTies)

