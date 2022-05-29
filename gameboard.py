from tkinter import * 
from tkinter import simpledialog


class BoardClass: 
    def __init__(self, player1Name: str = "", player2Name: str = "", 
                                lastPlayerName: str = "", numWins: int = 0, 
                                numTies: int = 0, numlosses: int = 0, root):
        self.player1Name = player1Name 
        self.player2Name = player2Name 
        self.lastPlayerName = lastPlayerName
        self.numWins = numWins
        self.numTies = numTies
        self.numlosses = numlosses
        self.gamePlayed = 0 

    def setupBoardGameGUI(): 

    def updateGamesPlayed(): 
        self.gamePlayed += 1 
