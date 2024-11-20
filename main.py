from tkinter import *
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from datetime import datetime, timezone
from dateutil import parser
import time
from PIL import Image, ImageTk

# widgets = GUI elements: buttons, textboxes, labels, images
# windows = serves as a container to hold or contain these widgets

window = Tk() #instantiate an instance of a window
window.geometry("600x420")
window.title("NBA")
window.resizable(False, False)

icon = PhotoImage(file='nbalogo.png')
window.iconphoto(True, icon)

#format for how the output will look like
f = "--{gameStatus}-- {awayScore} {awayTeam} vs. {homeScore} {homeTeam} @ {gameTimeLTZ}"


#function that gets the game information
def refresh():
    board = scoreboard.ScoreBoard()
    dateLabel = Label(window, text="Date: " + board.score_board_date)
    gameList = []
    games = board.games.get_dict()
    counter = 0 
    for game in games:
        try:
            box = boxscore.BoxScore(game['gameId'])
            gameInfo = box.game.get_dict()
            gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None)
            gameList.append(Label(window, text= f.format(gameStatus=gameInfo['gameStatusText'], awayScore=gameInfo['awayTeam']['score'] ,awayTeam=game['awayTeam']['teamName'], homeScore=gameInfo['homeTeam']['score'],homeTeam=game['homeTeam']['teamName'], gameTimeLTZ=gameTimeLTZ)))
            gameList[counter].grid(row=counter+1, column=1)
        except:
            placeHolder = Label(window, text=f"Game {counter}")
            placeHolder.grid(row=counter+1, column=1)
        counter += 1
        
    dateLabel.grid(row=0, column=0)

#creates a button that allows the user to  refresh to get live information
refresh_button = Button(window, text="Refresh", command=refresh)
refresh_button.grid(row=7, column=0)

window.mainloop() # place window on computer screen, listen for events

