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
    ID_KING_TEAM = db.ID_KING[TEAM]
    DATA = db.PART_TEAM[TEAM].get(ID_KING_TEAM)
    
    return DATA['coo']

# retorna se aquela peça ainda existe
def has_part(TEAM, ID_PART):
    return ID_PART in db.PART_TEAM[TEAM]

def focusKing(TEAM):
    i, j = getKing(TEAM)
    setFocus(i, j)
    
def get_enemy(TEAM):
    return db.black if TEAM == db.white else db.white

# pegar uma lista de tuplas das coordenadas das peças aliadas
def get_Listcoo_PartsTeam(TEAM):
    return [COO.get('coo') for COO in db.PART_TEAM[TEAM].values() if 'coo' in COO]

# pegar uma lista de tuplas das coordenadas das casas de movimento da peça
def get_Listcoo_MovePart(ID_PART, TEAM):
    SPACES = []
    for i, ROW in enumerate(db.MOVE): # matriz
        for j, CELL in enumerate(ROW):  # cada célula
            
            for SPACE in CELL[TEAM]:# lista dentro da célula
                if (
                    isinstance(SPACE, dict)
                    and SPACE.get('id') == ID_PART
                ):
                    SPACES.append((i, j))

    return SPACES

# limpar seleção
def empty_selection():
    SELECT_BASE = db.SELECT
    
    for y in range(len(SELECT_BASE)):
        for x in range(len(SELECT_BASE)):
            
            db.SELECT[y][x] = db.noSELECT