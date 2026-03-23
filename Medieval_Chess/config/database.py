# ==================================================
# Global function   
# ==================================================

def get_Key_byDictValue(dict:dict, value):
    for key, val in dict.items():
        if val == value:
            return key
    return None # Retorna None se não encontrar

# ==================================================
# Identifiers for Global Names in the Code
# ==================================================

# Identificadores
# base de dados para coorelação de peças e espaços dentro do código
TEAMID = {
    'noteam':0,
    'white':1,
    'black':2
}

PARTID = {
    'space':3,
    'pawn':4,
    'knight':5,
    'bishop':6,
    'jester':7,
    'prince':8,
    'rook':9,
    'queen':10,
    'king':100,
}

UP=1
DOWN=2
LEFT=3
RIGHT=4

# variáveis de apoio de comunicação do código em indicar efeito gerado na tabela SELECT
noSELECT=0
focusSELECT=1
noviewSELECTED=2
viewSELECTED=3

# ==================================================
# Global Names
# ==================================================

# NOMES DE UTILIZAÇÃO
# Identificadores práticos do código a partir da base de dados
noteam= TEAMID['noteam']
white = TEAMID['white']
black = TEAMID['black']

space = PARTID['space']
pawn  = PARTID['pawn']
knight= PARTID['knight']
bishop= PARTID['bishop']
jester= PARTID['jester']
prince= PARTID['prince']
rook  = PARTID['rook']
queen = PARTID['queen']
king  = PARTID['king']

# ==================================================
# Part Identification Variables
# ==================================================

ID_KING = {
    white: '1001',
    black: '1002'
}
ID_QUEEN = {
    white: '91',
    black: '92'
}
ID_PRINCE = {
    white: '71',
    black: '72'
}

# ==================================================
# Parts Materials
# ==================================================

MATERIAL = {
    space:    0,
    pawn:     1,
    knight:   3,
    bishop:   3,
    jester:   4,
    prince:   7,
    rook:     5,
    queen:    9,
    king:     100,
}

# ==================================================
# Piece Boards, Attacks, Movement & Auxiliary Variables
# ==================================================
# O tabuleiro possui 2 espaços a mais de linha e coluna para conter areas mortas do jogo para não ocorrer erros de indice fora da lista
# --------------------------------------------------

TABLE = [[
    {
        'material': space,
        'team':     noteam,
        'part':     space
    } 
    for _ in range(10)] for _ in range(10)]


COMBAT = [[
    {
        white:{},
        black:{}
    }
    for _ in range(10)] for _ in range(10)]

MOVE = [[
    {
        white:{},
        black:{}
    }
    for _ in range(10)] for _ in range(10)]

table_Ylenght = len(TABLE)
table_Xlenght = len(TABLE[0])

game_Ylenght = table_Xlenght-1
game_Xlenght = table_Ylenght-1

# ==================================================
# Selection Grid & Coordinates of the Selected Piece
# ==================================================

SELECT = [[
    '' for _ in range(10)] for _ in range(10)]

VIEW_SELECT = {
    noSELECT:       ['',''],      # SEM SELEÇÃO
    focusSELECT:    ['[',']'],    # EM FOCO
    noviewSELECTED: ['',''],      # SELEÇÃO INVISÍVEL
    viewSELECTED:['>',' '],    # SELEÇÃO VISÍVEL
}

SELECTED_PART_COO = None

# ==================================================
# Internal Gameplay Control Variables
# ==================================================

HAS_CAPTURE = False

REPLAY = {
    'before_move':{},
    'before_second_move':{},
}

QUANT_MOVES = {
    white: 0,
    black: 0
}

XEQUE = {
    white: False,
    black: False
}

PART_TEAM = {
    white:{},
    black:{}
}
# 'id': {part: '', attacks: 0, moves: 0, coo: (x, y)}

# ==================================================
# Turn and Player Control Variables
# ==================================================

NAME_PLAYERS = {
    white:'',
    black:''
}

ID_TURN = 1

TURNS = [
    white,
    black,
    white
]

# Pontuação dos jogadores:
SCORE_GAME = {
    black: 0,
    white: 0
}

# ==================================================
# End-of-Game Messages
# ==================================================

TYPE_END ={
    # O ITEM 0 SÓ EXISTE PARA EVITAR CONFLITO COM O CÓDIGO.
    0: {
        'name': '',
        'description': ''
    },
    1: {
        'name': 'AFOGAMENTO',
        'description': 'o Rei do Inimigo NÃO está em xeque, MAS não tem nenhum movimento legal disponível.'
    },
    2: {
        'name': 'REI CONTRA REI',
        'description': 'Os dois jogadores só tem o Rei e não podem se atacar.'
    },
    3: {
        'name': 'REI VS REI E BISPO',
        'description': 'Um jogador tem apenas o Rei e o outro tem apenas o Rei e um Bispo, e não é possível dar xeque-mate.'
    },
    4: {
        'name': 'REI VS REI E CAVALO',
        'description': 'Um jogador tem apenas o Rei e o outro tem apenas o Rei e um Cavalo, e não é possível dar xeque-mate.'
    }
}

# ==================================================
# Unitary Movements of Pieces
# ==================================================

PART_MOVES_UNIT = {
    # Peão: ataca na diagonal 1 casa, anda para frente e para traz (nessa variante)
    pawn: [( 1, 0), (-1, 0),
           ( 1,-1), ( 1, 1),
           (-1,-1), (-1, 1)],
    
    # Cavalo: anda em L
    knight: [( 2, 1),( 2,-1),
             (-1, 2),( 1, 2),
             (-2, 1),(-2,-1),
             (-1,-2),( 1,-2)],
    
    # Bispo: Diagonal
    bishop: [( 1,-1),( 1, 1),
             (-1,-1),(-1, 1)],
    
    # Jester: dois movimentos de 3 casas {horizontal, diagonal}
    jester: [
            [( 1, 0),( 0,-1),(-1, 0),( 0, 1)], # horizontal
            [( 1,-1),( 1, 1),(-1,-1),(-1, 1)]  # vertical
          ],

    # Prince: 1 horizontal + 2 vertical
    # a divisão de movimentos só foi aplicada porque a vertical move em 2 e o horizontal em 1
    prince: [
            [( 1, 0),( 0,-1),(-1, 0),( 0, 1)], # horizontal
            [( 1,-1),( 1, 1),(-1,-1),(-1, 1)]  # vertical
          ],
    
    # Torre: Horizontal
    rook: [( 1, 0),( 0,-1),(-1, 0),( 0, 1)],
    
    # Rainha: diagonal + horizontal
    queen: [( 1,-1),( 1, 0),( 1, 1),
            ( 0,-1),        ( 0, 1),
            (-1,-1),(-1, 0),(-1, 1)],
    
    # Rei: 
    king: [( 1,-1),( 1, 0),( 1, 1),
           ( 0,-1),        ( 0, 1),
           (-1,-1),(-1, 0),(-1, 1)],
}

# ==================================================
# Part Design
# ==================================================

PART = {
    black: {
        space:  '█',
        pawn:   '♟',
        rook:   '♜',
        jester: '✦',
        prince: '♠',
        knight: '♞',
        bishop: '♝',
        queen:  '♛',
        king:   '♚'
    },
    white: {
        space:  ' ',
        pawn:   '♙',
        rook:   '♖',
        jester: '✧',
        prince: '♤',
        knight: '♘',
        bishop: '♗',
        queen:  '♕',
        king:   '♔'
    }
}