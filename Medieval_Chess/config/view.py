import database as db

# VIZUALIZAR MAPA
# perguntar tipo da visão:
# only_map: apenas as peças no tabuleiro
# choose_part: mapa + parte de texto do turno do jogador
#                       tutorial de seleção
#                       nome da peça + se possível movimento

# linha: i
# coluna: j
# se linha i+(j-1) e coluna j forem impares: espaço branco se vazio
# senão: preto se vazio

def print_space(i, j):
    SQUARE = db.SELECT[i][j]
    # se linha i+(j-1) e coluna j forem impares: espaço branco se vazio
    # senão: preto se vazio
    if (((j & 1) != 0) or (((i + j - 1) & 1) != 0)):
        part = db.PART[db.white][db.space]
    
    else:
        part = db.PART[db.black][db.space]
    
    # se seleção for 1 (casa em foco), adicionar [ ] entre o espaço
    if (SQUARE in (1,3)):
        first = db.VIEW_SELECT[SQUARE][0]
        last = db.VIEW_SELECT[SQUARE][1]
    # se seleção for 3 (opção visível), adicionar ">" e " " entre o espaço
    else:
        first = part
        last = part
    
    return str(first+(part*2)+last)