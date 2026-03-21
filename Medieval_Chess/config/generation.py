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
            set_initial_PartTeam(team, id_part, part, (1+i, j))
    
    # Peças Brancas
    team = db.white
    for i in range(1,-1,-1):
        for j in range(1,9):
            part = arrengement_pieces[i][j-1]
            
            QUANT[part] += 1
            id_part = get_idPart(part,QUANT[part])
            set_partToTable(team, part, (8-i, j))
            set_initial_PartTeam(team, id_part, part, (8-i, j))
            
            
# 5. ID = 'material' + quant.inserida
def get_idPart(part, index_add_quant):
    return str(db.MATERIAL[part]) + str(index_add_quant)
 
# 6. Setar material, time e peça em TABLE
def set_partToTable(team, part, position):
    y, x = position
    db.TABLE[y][x]['material'] = db.MATERIAL[part]
    db.TABLE[y][x]['team'] = team
    db.TABLE[y][x]['part'] = part

# 11. Setar a equipe em PART_TEAM inicialmente
def set_initial_PartTeam(team, id, part, position):
    DATA_PART = {
        'part': part,
        'attacks': 0,
        'moves': 0,
        'coo': position
    }
    
    db.PART_TEAM[team][str(id)] = DATA_PART

# setar dados ao replay para salvar estados antigos
def set_replay(replay):
    db.REPLAY[replay] = copy.deepcopy({
        'XEQUE': {
            db.white: db.XEQUE[db.white],
            db.black: db.XEQUE[db.black]
        },
        'TABLE': db.TABLE,
        'QUANT_MOVES': db.QUANT_MOVES,
        'COMBAT': db.COMBAT,
        'PART_TEAM': db.PART_TEAM,
        'SCORE_GAME': db.SCORE_GAME
    })

# retornar o estado do replay de volta ao jogo
def return_state_dataReplay(replay):
    db.TABLE       = copy.deepcopy(db.REPLAY[replay]['TABLE'])
    db.COMBAT      = copy.deepcopy(db.REPLAY[replay]['COMBAT'])
    db.PART_TEAM  = copy.deepcopy(db.REPLAY[replay]['PART_TEAM'])
    db.SCORE_GAME  = copy.deepcopy(db.REPLAY[replay]['SCORE_GAME'])
    db.QUANT_MOVES  = copy.deepcopy(db.REPLAY[replay]['QUANT_MOVES'])

    db.XEQUE[db.white] = db.REPLAY[replay]['XEQUE'][db.white]
    db.XEQUE[db.black] = db.REPLAY[replay]['XEQUE'][db.black]
    
# limpar todo replay
def empty_allReplay():
    for replay in range(2):
        db.REPLAY[replay] = {
            'XEQUE': {
                db.white: False,
                db.black: False
            },
    
            'TABLE': [[
                {
                    'material': db.space,
                    'team':     db.noteam,
                    'part':     db.space
                }
            for _ in range(10)] for _ in range(10)],
    
            'QUANT_MOVES': {
                db.white: 0,
                db.black: 0
            },

            'COMBAT': [[
            {
                db.white:{},
                db.black:{}
            }
            for _ in range(10)] for _ in range(10)],

            'PART_TEAM': {
                db.white:[],
                db.black:[]
            },

            'SCORE_GAME': {
                db.black: 0,
                db.white: 0
            }
        }

# resetar jogo
def reset_state():
    # poupar linhas de limpamento de dados com funções pré-feitas
    empty_allReplay()
    
    for replay in ['replay1', 'replay2']:
        set_replay(replay)
    
    db.REPLAY = {
        'replay1':{},
        'replay2':{},   
    }
    
    db.NAME_PLAYERS = {
        db.white:'',
        db.black:''
    }

    db.TURNS = [
        db.white,
        db.black,
        db.white
    ]

    db.ID_TURN = 0
    db.HAS_CAPTURE = False