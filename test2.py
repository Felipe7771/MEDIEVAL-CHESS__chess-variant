CELL_WIDTH = 4

def render_cell(piece):
    return piece.center(CELL_WIDTH)

def draw_board(board):
    horizontal = '─' * CELL_WIDTH
    
    top    = '┌' + '┬'.join([horizontal]*8) + '┐'
    middle = '├' + '┼'.join([horizontal]*8) + '┤'
    bottom = '└' + '┴'.join([horizontal]*8) + '┘'
    
    print(top)
    
    for i, row in enumerate(board):
        line = '│' + '│'.join(render_cell(p) for p in row) + '│'
        print(line)
        
        if i < len(board) - 1:
            print(middle)
    
    print(bottom)
    
board = [
    ['[♜]','♞','♝','♛','>♚','♝','♞','♜'],
    ['♟','♟','♟','♟','♟','♟','♟','♟'],
    ['████','◻','✦','✧','♠','[♤]','[██]','◻'],
    [' ']*8,
    ['>███']*8,
    ['◻']*8,
    ['♙']*8,
    ['♖','♘','♗','♕','♔','♗','♘','♖'],
]

draw_board(board)