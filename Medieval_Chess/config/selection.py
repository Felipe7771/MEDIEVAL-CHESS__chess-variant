import database as db
import numpy as np

# ==================================================
# Piece Selection Methods and Initial King Selection    
# ==================================================
 
def setFocus(i: int, j: int) -> None:
    # remove antigo
    if db.SELECTED_PART_COO is not None:
        old_i, old_j = db.SELECTED_PART_COO
        db.SELECT[old_i][old_j] = db.noSELECT

    # aplica novo
    db.SELECTED_PART_COO = (i, j)
    db.SELECT[i][j] = db.focusSELECT


def getCooFocused() -> tuple:
    if db.SELECTED_PART_COO is None:
        return (0, 0)
    
    return db.SELECTED_PART_COO

# pegar peça que está na casa do TABLE que coicide com o SELECT que está com focusSELECT
def getPartANDteamFocused():
    i, j = getCooFocused()
    return db.TABLE[i][j]['part'], db.TABLE[i][j]['team']

def getKing(TEAM) -> tuple | None:
    ID_KING_TEAM = db.ID_KING[TEAM]
    DATA = db.PART_TEAM[TEAM].get(ID_KING_TEAM)
    
    return DATA['coo']

def focusKing(TEAM) -> None:
    i, j = getKing(TEAM)
    setFocus(i, j)

# ==================================================
# List of Coordinates for Selection    
# ==================================================

# pegar uma lista de tuplas das coordenadas das peças aliadas
def get_Listcoo_PartsTeam(TEAM) -> list:
    return [COO.get('coo') for COO in db.PART_TEAM[TEAM].values() if 'coo' in COO]

# pegar uma lista de tuplas das coordenadas das casas de movimento da peça
def get_Listcoo_MovePart(ID_PART: str, TEAM) -> list:
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

# ==================================================
# Support functions for part selection, etc.   
# ==================================================

# limpar seleção
def empty_selection():
    SELECT_BASE = db.SELECT
    
    for y in range(len(SELECT_BASE)):
        for x in range(len(SELECT_BASE)):
            
            db.SELECT[y][x] = db.noSELECT
            
# pegar identificador da peça pelo time e posição
def get_id_part(team, y: int, x: int) -> str | None:
    GROUP = db.PART_TEAM[team]
    for KEYID in GROUP:
        
        PART = GROUP[KEYID]
        
        if (PART['coo'] == (y, x)):
            return KEYID


# retorna se aquela peça ainda existe
def has_part(TEAM, ID_PART: str) -> bool:
    return ID_PART in db.PART_TEAM[TEAM]

    
def get_enemy(TEAM) -> bool:
    return db.black if TEAM == db.white else db.white