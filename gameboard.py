from tkinter import * 
from tkinter import simpledialog


class BoardClass: 
    def __init__(self, root: Tk, player1Name: str = "", player2Name: str = "", 
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


    def buttonClicked(self, button, name: str): 
        


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

        # Making the boardGameView in the center of the screen 
        self.frame.columnconfigure(0, weight=1)  
        self.frame.columnconfigure(2, weight=1)  
        self.frame.rowconfigure(0, weight=1)    
        self.frame.rowconfigure(2, weight=1)


    def updateGamesPlayed(self): 
        self.gamePlayed += 1 
