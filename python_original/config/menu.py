import config.data as dt
import config.question as q
import config.game as g
import os

def setIncialMenu():
    os.system('cls')
    print('♟ ♞ ♝ ♜ ♛ ♚ _XADREZ_♔ ♕ ♖ ♗ ♘ ♙')
    q.enter('Jogar')
    names = g.setNamePlayers()
    
    g.BeginingGame(names)

def set_historic_score(pts_white, pts_black):
    dt.score_historical.append({
        dt.white: pts_white,
        dt.black: pts_black
    })
    