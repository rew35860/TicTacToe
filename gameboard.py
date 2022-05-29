from tkinter import * 
from tkinter import simpledialog


class BoardClass: 
    def __init__(self, root: Tk, marker: str, player1Name: str = "", player2Name: str = "", 
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
        
        self.marker = marker

        self.move = ""
        self.previousBtn = None 
    
        self.lockMove = False

        self.allMoves = []
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.buttonBoard = [' ',' ',' ',' ',' ',' ',' ',' ',' ']


    def getMove(self): 
        return self.move 


    def moveIsAvalible(self): 
        return True if self.move not in self.allMoves else False


    def buttonClicked(self, button, name: str): 
        print("in button")
        if not self.lockMove and name not in self.allMoves:
            print(button["text"])
            if self.move != "" and self.move != name and self.move not in self.allMoves: 
                self.previousBtn["text"] = ""
                button["text"] = self.marker
                self.previousBtn = button
                self.move = name
            else: 
                button["text"] = self.marker
                self.previousBtn = button
                self.move = name


    def setLockMove(self, lock: bool):
        self.lockMove = lock


    def getLockMove(self): 
        return self.lockMove 


    def setupBoardGameGUI(self): 
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
