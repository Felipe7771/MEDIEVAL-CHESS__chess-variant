import config.data as dt
import copy

# define uma peça no tabuleiro
def set_part(material, team, part, position):
    x, y = position
    dt.table[x][y]['material'] = material
    dt.table[x][y]['team'] = dt.db[team]
    dt.table[x][y]['part'] = part
    
def set_table_game():
    material = [
        [
            dt.rook, dt.knight, dt.bishop,
            dt.king,dt.queen,
            dt.bishop, dt.knight, dt.rook
        ],
        [
            dt.pawn,dt.pawn,dt.pawn,dt.pawn,
            dt.pawn,dt.pawn,dt.pawn,dt.pawn
        ] 
    ]
    # Peças pretas
    team = 'black'
    id = 0
    for j in range(2):
        for i in range(1,9):
            part = material[j][i-1]
            set_part(dt.material[part], team, part, (1+j, i))
    
    # Peças brancas
    team = 'white'
    for j in range(1,-1,-1):
        for i in range(1,9):
            part = material[j][i-1]
            set_part(dt.material[part], team, part, (8-j, i))

def empty_history():
    dt.history = {
    'xeque': {
    dt.white: False,
    dt.black: False
    },
    
    'table': [[
        {
            'material': dt.space,
            'team':     dt.noteam,
            'part':     dt.space
        }
       for _ in range(10)] for _ in range(10)],
    
    'quant_move': {
        dt.white: 0,
        dt.black: 0
    },

    'selection': [[0 for _ in range(10)] for _ in range(10)],

    'combat': [[{dt.white:{'move':False,'attack':False}, dt.black:{'move':False,'attack':False}} for _ in range(10)] for _ in range(10)],

    'by': [[[] for _ in range(10)] for _ in range(10)],

    'team_parts': {
        dt.white:[],
        dt.black:[]
    },

    'score_game': {
        dt.black: 0,
        dt.white: 0
    }
}
    
# setar os dados do jogo para o histórico
def set_history():
    dt.history = copy.deepcopy({
        'xeque': {
            dt.white: dt.xeque[dt.white],
            dt.black: dt.xeque[dt.black]
        },
        'table': dt.table,
        'quant_move': dt.quant_move,
        'selection': dt.selection,
        'combat': dt.combat,
        'by': dt.by,
        'team_parts': dt.team_parts,
        'score_game': dt.score_game
    })

# de emergencia, retorna os dados do histórico para o jogo
def get_history():
    dt.table       = copy.deepcopy(dt.history['table'])
    dt.selection   = copy.deepcopy(dt.history['selection'])
    dt.combat      = copy.deepcopy(dt.history['combat'])
    dt.by          = copy.deepcopy(dt.history['by'])
    dt.team_parts  = copy.deepcopy(dt.history['team_parts'])
    dt.score_game  = copy.deepcopy(dt.history['score_game'])
    dt.quant_move  = copy.deepcopy(dt.history['quant_move'])

    dt.xeque[dt.white] = dt.history['xeque'][dt.white]
    dt.xeque[dt.black] = dt.history['xeque'][dt.black]