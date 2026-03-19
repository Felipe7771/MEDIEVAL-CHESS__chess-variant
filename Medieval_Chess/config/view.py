import database as db
import generation as genera

# VIZUALIZAR MAPA
# perguntar tipo da visão:
# only_map: apenas as peças no tabuleiro
# choose_part: mapa + parte de texto do turno do jogador
#                       tutorial de seleção
#                       nome da peça + se possível movimento
def view_table():
    TABLE = db.TABLE
    CELL_WIDTH = 4 
    
    horizontal = '─' * CELL_WIDTH
    
    top    = '┌' + '┬'.join([horizontal]*8) + '┐'
    middle = '├' + '┼'.join([horizontal]*8) + '┤'
    bottom = '└' + '┴'.join([horizontal]*8) + '┘'
    
    # Inserir primeira linha de grade
    print(top)
    
    # analisar TABLE (i linha x j coluna)
    for i in range(1, db.game_Xlenght):
        # criar uma lista das casas a serem mostradas
        board = []
        for j in range(1, db.game_Ylenght):
            
            SQUARE = TABLE[i][j]
            
            if (SQUARE['part'] == db.space):
                board.append(print_space(i,j))
            else:
                board.append(print_part(SQUARE,i,j))
        
        # exibir linha
        print_line(board, CELL_WIDTH)
        # possivelmente exibir interceção das linhas
        print_middle_lines(i, middle)
    
    # exibir fim da grade do tabuleiro
    print(bottom)

# exibir casa
def render_cell(piece, CELL_WIDTH):
    return piece.center(CELL_WIDTH)

# exibir linha a partir da lista das casas criadas
def print_line(board, CELL_WIDTH):
    line = '│' + '│'.join(render_cell(p,CELL_WIDTH) for p in board) + '│'
    
    print(line)

# exibir interceção entre as linha
def print_middle_lines(i, middle):
    # se o número da coluna lida não for a última linha de TABLE, exiba a interceção
    if i < db.game_Xlenght - 1:
            print(middle)

def print_part(square_TABLE, i, j):
    part = square_TABLE['part']
    team = square_TABLE['team']
    
    view_print = db.PART[team][part]
    
    view_select = db.SELECT[i][j]
    
    return str(view_select + view_print + view_select)

# linha: i
# coluna: j
# se linha i+(j-1) e coluna j forem impares: espaço branco se vazio
# senão: preto se vazio

def print_space(i, j):
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


genera.set_InitialPiecesTable()
view_table()
# for i in range(1,db.game_Xlenght):
#     for j in range(1,db.game_Ylenght):
#         print(db.get_Key_byDictValue(db.PARTID,db.TABLE[i][j]['part']),end=", ")
    
#     print()