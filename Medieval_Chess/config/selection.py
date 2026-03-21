import database as db
import numpy as np

def setFocus(i, j):
    # remove antigo
    if db.FOCUS_POS is not None:
        old_i, old_j = db.FOCUS_POS
        db.SELECT[old_i][old_j] = db.noSELECT

    # aplica novo
    db.FOCUS_POS = (i, j)
    db.SELECT[i][j] = db.focusSELECT


def getCooFocused():
    if db.FOCUS_POS is None:
        return 0, 0
    
    return db.FOCUS_POS

# pegar identificador da peça pelo time e posição
def get_id_part(team, y, x):
    GROUP = db.PART_TEAM[team]
    for KEYID in GROUP:
        
        PART = GROUP[KEYID]
        
        if (PART['coo'] == (y, x)):
            return KEYID

# pegar peça que está na casa do TABLE que coicide com o SELECT que está com focusSELECT
def getPartANDteamFocused():
    i, j = getCooFocused()
    return db.TABLE[i][j]['part'], db.TABLE[i][j]['team']

def getKing(TEAM):
    DATA = db.PART_TEAM[TEAM]
    
    return (DATA['x'], DATA['y'])

def focusKing(TEAM):
    i, j = getKing(TEAM)
    setFocus(i, j)
    
def get_enemy(TEAM):
    return db.black if TEAM == db.white else db.white