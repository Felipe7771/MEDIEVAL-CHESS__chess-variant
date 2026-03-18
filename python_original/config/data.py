db = {
'noteam':0,
'white':1,
'black':2,

'space':5,
'pawn':6,
'knight':7,
'bishop':8,
'rook':9,
'queen':10,
'king':100,
}

names = {
0:'noteam',
1:'white',
2:'black',

5:'space',
6:'pawn',
7:'knight',
8:'bishop',
9:'rook',
10:'queen',
100:'king'
}

score_historical = []

noteam= db['noteam']
white = db['white']
black = db['black']

space = db['space']
pawn  = db['pawn']
rook  = db['rook']
knight= db['knight']
bishop= db['bishop']
queen = db['queen']
king  = db['king']

material = {
    space:    0,
    pawn:     1,
    knight:   3,
    bishop:   3,
    rook:     5,
    queen:    9,
    king:     100,
}

# peça que se moveu:
# seu x,y atual, time, peça
# seu x,y antigo
part_play = {
    'part': space,
    'newx': 0,
    'newy': 0,
    'team': noteam,
    'oldx': 0,
    'oldy': 0
}

# Para avaliar tanto quanto se a jogada é ilegal ou não quanto para a avaliação da jogada, o dicionário histórico guarda todo o tabuleiro, pontos, peças, ataques, movimentos, etc... de cada turno. Assim, é possível analisar o que aconteceu em cada turno e avaliar a jogada atual com base nisso. O dicionário histórico é atualizado a cada turno, armazenando as informações relevantes para a análise futura.
# salvo ANTES que qualquer alteração a ser feita pela jogada seja feita, ou seja, o estado do jogo antes da jogada ser feita. Assim, é possível analisar o que aconteceu em cada turno e avaliar a jogada atual com base nisso.
history = {
    'xeque': {
    white: False,
    black: False
    },
    
    'table': [[
        {
            'material': space,
            'team':     noteam,
            'part':     space
        }
       for _ in range(10)] for _ in range(10)],
    
    'quant_move': {
        white: 0,
        black: 0
    },

    'selection': [[0 for _ in range(10)] for _ in range(10)],

    'combat': [[{white:{'move':False,'attack':False}, black:{'move':False,'attack':False}} for _ in range(10)] for _ in range(10)],

    'by': [[[] for _ in range(10)] for _ in range(10)],

    'team_parts': {
        white:[],
        black:[]
    },

    'score_game': {
        black: 0,
        white: 0
    }
}

xeque = {
    white: False,
    black: False
}

table = [[
    {
        'material': space,
        'team':     noteam,
        'part':     space
    } 
    for _ in range(10)] for _ in range(10)]

quant_move = {
    white: 0,
    black: 0
}

tb_lenx = len(table)
tb_leny = len(table[0])

game_tbx = tb_lenx-1
game_tby = tb_leny-1

# 1: selecinando (→ ←)  2: pré-selecionado ([ ])
selection = [[0 for _ in range(10)] for _ in range(10)]

view_slc = {
    0:[' ',' '],
    1:['→','←'],
    2:['[',']'],
    3:['*','*'],
    4:['!','!'],
    5:['<','>'],
}

# combat = [[{'move':False,'attack':False,'black':False,'white':False} for _ in range(10)] for _ in range(10)]
combat = [[{white:{'move':False,'attack':False}, black:{'move':False,'attack':False}} for _ in range(10)] for _ in range(10)]


by = [[[] for _ in range(10)] for _ in range(10)]


combat_simul = [[{white:{'move':False,'attack':False}, black:{'move':False,'attack':False}} for _ in range(10)] for _ in range(10)]

by_simul = [[[] for _ in range(10)] for _ in range(10)]

table_simul = [[
    {
        'material': space,
        'team':     noteam,
        'part':     space
    } 
    for _ in range(10)] for _ in range(10)]

team_parts = {
    white:[],
    black:[]
}

# {part: '', attacks: 0, y: '', x: ''}

players = {
    white:'',
    black:''
}

turns = [white,black,white]
id_turn = 0

# Pontuação dos jogadores:
score_game = {
    black: 0,
    white: 0
}

parts = {
    black: {
        space: '◼',
        pawn: '♟',
        rook: '♜',
        knight: '♞',
        bishop: '♝',
        queen: '♛',
        king: '♚'
    },
    white: {
        space: '◻',
        pawn: '♙',
        rook: '♖',
        knight: '♘',
        bishop: '♗',
        queen: '♕',
        king: '♔'
    }
}
# 0:  livre
# TIME
# 0: Nenhum
# 1: Pretas
# 2: Brancas
# PONTOS DE MATERIAL:
# 1: Peão
# 3: Bispo / Cavalo
# 5: Torre
# 9: Rainha
# 100: Rei
wasCaptured = False

list_simbols = []

simbols = {
    1: '(O)',
    10: '(<<)',
    40: '(-)',
    20: '(>)',
    30: '(Δ)',
    50: '(=)',
    60: '(+)',
    70: '(X)',
    80: '(*)',
    90: '(!)',
    100: '(囗)',
    110: '(#)',
    120: '(!!)',
    150: '(½)',
    200: '(!?)',
}

simbols_name = {
    '(O)': 'MOVIMENTO',
    '(<<)': 'FUGA',
    '(-)': 'SACRIFÍCIO',
    '(>)': 'AVANÇO',
    '(Δ)': 'DOMÍNIO',
    '(=)': 'TROCA',
    '(+)': 'CAPTURA',
    '(X)': 'AMEAÇA',
    '(*)': 'ATAQUE DESCOBERTO',
    '(!)': 'GARFO',
    '(囗)': 'CERCAMENTO',
    '(#)': 'XEQUE',
    '(!!)': 'XEQUE DUPLO',
    '(½)': 'EMPATE',
    '(!?)': 'XEQUE-MATE!',
}

type_draw ={
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

coo_moves = ''
signal = ''

arq_moves = []