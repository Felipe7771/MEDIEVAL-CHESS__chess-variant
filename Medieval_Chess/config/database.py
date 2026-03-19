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

def get_Key_byDictValue(dict, value):
    for key, val in dict.items():
        if val == value:
            return key
    return None # Retorna None se não encontrar

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


MATERIAL = {
    space:    0,
    pawn:     1,
    knight:   3,
    bishop:   3,
    jester:   4,
    prince:   5,
    rook:     5,
    queen:    9,
    king:     100,
}

PART_MOVES_UNIT = {
    # Peão: ataca na diagonal 1 casa, anda para frente e para traz (nessa variante)
    pawn: [( 1, 0), (-1, 0)
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
    prince: [( 1,-1),( 1, 0),( 1, 1),
             ( 0,-1),        ( 0, 1),
             (-1,-1),(-1, 0),(-1, 1)],
    
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

REPLAY = {
    'replay1':{},
    'replay2':{},
}

XEQUE = {
    white: False,
    black: False
}

# O tabuleiro possui 2 espaços a mais de linha e coluna para conter areas mortas do jogo para não ocorrer erros de indice fora da lista
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

SELECT = [[
    '' for _ in range(10)] for _ in range(10)]

VIEW_SELECT = {
    0:['',''],      # SEM SELEÇÃO
    1:['[',']'],    # EM FOCO
    2:['',''],      # SELEÇÃO INVISÍVEL
    3:['>',' '],    # SELEÇÃO VISÍVEL
}

QUANT_MOVES = {
    white: 0,
    black: 0
}

table_Xlenght = len(TABLE)
table_Ylenght = len(TABLE[0])

game_Xlenght = table_Xlenght-1
game_Ylenght = table_Ylenght-1

# # 1: selecinando (→ ←)  2: pré-selecionado ([ ])
# selection = [[0 for _ in range(10)] for _ in range(10)]

# view_slc = {
#     0:[' ',' '],
#     1:['→','←'],
#     2:['[',']'],
#     3:['*','*'],
#     4:['!','!'],
#     5:['<','>'],
# }

PART_TEAM = {
    white:[],
    black:[]
}
# {id: '',part: '', attacks: 0, y: '', x: ''}

NAME_PLAYERS = {
    white:'',
    black:''
}

TURNS = [
    white,
    black,
    white
]

ID_TURN = 0

# Pontuação dos jogadores:
SCORE_GAME = {
    black: 0,
    white: 0
}

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

HAS_CAPTURE = False

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