import database as db
import copy

# definir organização de peças
#  ♖ ♗ ✧ ♔ ♕  ♤ ♗ ♖     
#  ♙ ♘ ♙ ♙ ♙ ♙ ♘ ♙,

arrengement_pieces = [
    [
        db.rook, db.bishop,
        db.jester, db.king, db.queen, db.prince,
        db.bishop, db.rook
    ],
    [
        db.pawn, db.knight,
        db.pawn, db.pawn, db.pawn, db.pawn,
        db.knight, db.pawn
    ]
]

# Definição de posicionamento de peças
# 1. Definir id das peças para cada
# 1.1 Salvar quantidades inseridas de cada peça no tabuleiro
# 2. ler o arrengement_pieces em i linhas e j colunas
# 3. Começar com os pretos
# 4. Linhas 1 e 2, lendo arrengement-pieces normalmente
# 5. ID = 'material' + quant.inserida
# 6. Setar material, time e peça em TABLE
# 7. Setar a equipe em PART_TEAM inicialmente
# 8. Começar com os brancos
# 9. Linhas 7 e 8, lendo arrengement-pieces invertido
# 10. ID = 'material' + quant.inserida
# Setar material, time e peça em TABLE
# 11. Setar a equipe em PART_TEAM inicialmente

def set_InitialPiecesTable():
    # salvar quantidade de peças adicionadas
    QUANT = {
        db.pawn:0,
        db.knight:0,
        db.bishop:0,
        db.jester:0,
        db.prince:0,
        db.rook:0,
        db.queen:0,
        db.king:0
    }
    
    # começar com os Pretos
    team = db.black
    for i in range(2):
        for j in range(1,9):
            part = arrengement_pieces[i][j-1]
            
            QUANT[part] += 1
            id_part = get_idPart(part,QUANT[part])
            
            set_partToTable(team, part, (1+i, j))
            set_initial_PartTeam(team, id_part, (1+i, j))
    
    # Peças Brancas
    team = db.white
    for i in range(1,-1,-1):
        for j in range(1,9):
            part = arrengement_pieces[i][j-1]
            
            QUANT[part] += 1
            id_part = get_idPart(part,QUANT[part])
            
            set_partToTable(team, part, (8+i, j))
            set_initial_PartTeam(team, id_part, (8+i, j))
            
            
# 5. ID = 'material' + quant.inserida
def get_idPart(part, index_add_quant):
    return str(db.MATERIAL[part]) + str(index_add_quant)
 
# 6. Setar material, time e peça em TABLE
def set_partToTable(team, part, position):
    x, y = position
    db.TABLE[x][y]['material'] = db.MATERIAL[part]
    db.TABLE[x][y]['team'] = team
    db.TABLE[x][y]['part'] = part

# 11. Setar a equipe em PART_TEAM inicialmente
def set_initial_PartTeam(team, id, part, position):
    x, y = position
    DATA_PART = {
        'id': id,
        'part': part,
        'attacks': 0,
        'y': y,
        'x': x
    }
    db.PART_TEAM[team].append(DATA_PART)
