import database as db
import generation as genera
import selection as select

LINES_TURN = {
    db.white: (7, 8),
    db.black: (1, 2)
}

COO_LETTERS = ["","a","b","c","d","e","f","g","h"]

# ==================================================
# Board View + Possible Move Options   
# ================================================== 
# VIZUALIZAR MAPA
# perguntar tipo da visão:
# only_map: apenas as peças no tabuleiro
# choose_part: mapa + parte de texto do turno do jogador
#                       tutorial de seleção
#                       nome da peça + se possível movimento
# --------------------------------------------------

def view_table(show_turn=False, attack_move=False) -> None:
    ALLY = db.TURNS[db.ID_TURN]
    
    TABLE = db.TABLE
    CELL_WIDTH = 4 
    
    horizontal = '─' * CELL_WIDTH
    
    top    = '┌' + '┬'.join([horizontal]*8) + '┐'
    middle = '├' + '┼'.join([horizontal]*8) + '┤'
    bottom = '└' + '┴'.join([horizontal]*8) + '┘'
    
    # Inserir primeira linha de grade
    print(top)
    
    # analisar TABLE (i linha x j coluna)
    for i in range(1, db.game_Ylenght):
        # criar uma lista das casas a serem mostradas
        board = []
        for j in range(1, db.game_Xlenght):
            
            SQUARE = TABLE[i][j]
            
            if (SQUARE['part'] == db.space):
                board.append(print_space(i,j))
            else:
                board.append(print_part(SQUARE,i,j))
        
        # exibir linha
        print_line(board, CELL_WIDTH)
        
        if ((not show_turn) or (i not in LINES_TURN[ALLY])):
            print()
        else:
            print_show_turn(i, ALLY, attack_move)
        
        # possivelmente exibir interceção das linhas
        print_middle_lines(i, middle)
        
        if ((not show_turn) or (i not in LINES_TURN[ALLY]) and (i != 8)):
            print()
            
        elif (i != 8):
            print(" # |")
    
    # exibir fim da grade do tabuleiro
    print(bottom)

# exibir casa
def render_cell(piece:str, CELL_WIDTH:int) -> str:
    return piece.center(CELL_WIDTH)

# exibir linha a partir da lista das casas criadas
def print_line(board:list, CELL_WIDTH:int)-> None:
    line = '│' + '│'.join(render_cell(p,CELL_WIDTH) for p in board) + '│'
    
    print(line,end='')

# exibir interceção entre as linha
def print_middle_lines(i:int, middle:str) -> None:
    # se o número da coluna lida não for a última linha de TABLE, exiba a interceção
    if i < db.game_Xlenght - 1:
            print(middle,end='')

def print_part(square_TABLE: dict, i:int, j:int)-> str:
    part = square_TABLE['part']
    team = square_TABLE['team']
    
    view_print = db.PART[team][part]
    
    view_select = db.SELECT[i][j]
    
    return str(view_select + view_print + view_select)

# linha: i
# coluna: j
# se linha i+(j-1) e coluna j forem impares: espaço branco se vazio
# senão: preto se vazio

def print_space(i: int, j: int) -> str:
    SQUARE = db.SELECT[i][j]
    # se linha i+(j-1) e coluna j forem impares: espaço branco se vazio
    # senão: preto se vazio
    if (
        (((j & 1) == 0) and ((i & 1) == 0)) or 
        (((j & 1) != 0) and ((i & 1) != 0))
       ):
        part = db.PART[db.white][db.space]
    
    else:
        part = db.PART[db.black][db.space]
    
    # se seleção for 1 (casa em foco), adicionar [ ] entre o espaço
    if (SQUARE in (db.focusSELECT, db.viewSELECTED)):
        first = db.VIEW_SELECT[SQUARE][0]
        last = db.VIEW_SELECT[SQUARE][1]
    # se seleção for 3 (opção visível), adicionar ">" e " " entre o espaço
    else:
        first = part
        last = part
    
    return str(first+(part*2)+last)

def print_show_turn(i: int, ALLY, attack_move: bool) -> None:
    lines = {
        'turn_moviment': {
            db.white: 7,
            db.black: 1
        },
        
        'selection_describe': {
            db.white: 8,
            db.black: 2
        }      
    }
    
    # Exibição da mensagem de turno do jogador
    if (i == lines['turn_moviment'][ALLY]):
        print_turn_moviment(ALLY)
        
    # Exibição de seleção da casa escolhida
    elif (i == lines['selection_describe'][ALLY]):
        print_selection_describe(attack_move)
    
    else:
        print()

def print_turn_moviment(ALLY) -> None:
    
    NAME_PLAYER = db.NAME_PLAYERS[ALLY]
    TIME = db.get_Key_byDictValue(db.TEAMID, ALLY)
    
    print(f" # || TURNO DE '{NAME_PLAYER.upper()}' ({TIME})")
    
def print_selection_describe(attacking_move: bool) -> None:
    
    PART, TEAM = select.getPartANDteamFocused()
    pos = select.getCooFocused()
    
    EXTRA = '➔  ' if attacking_move else ''
    
    if pos == (0,0):
        print(f" # || Selecionado: {EXTRA}[NENHUM]")
        return
    
    i, j = pos
    
    if (PART is None):
        ITEM_SELECTION = "[00]"
        
    elif (PART != db.space):   
        NAME = db.get_Key_byDictValue(db.PARTID, PART)
        ICON_PART = db.PART[TEAM][PART]
        
        ATTACK = '🗡' if attacking_move else ''
        
        ITEM_SELECTION = f"{ATTACK} {NAME} ({ICON_PART})"
        
    else:
        ITEM_SELECTION = f"[{COO_LETTERS[i]}{j}]"
    
    
    print(f" # || Selecionado: {EXTRA}{ITEM_SELECTION}")

# ==================================================
# Temporary Rendering  
# ================================================== 

genera.set_InitialPiecesTable()
view_table(show_turn=True, attack_move=True)
# for i in range(1,db.game_Xlenght):
#     for j in range(1,db.game_Ylenght):
#         print(db.get_Key_byDictValue(db.PARTID,db.TABLE[i][j]['part']),end=", ")
    
#     print()