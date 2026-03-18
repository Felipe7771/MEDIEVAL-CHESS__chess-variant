CELL_WIDTH = 3

board = [
    ['♜','♞','♝','♛','♚','♝','♞','♜'],
    ['♟','♟','♟','♟','♟','♟','♟','♟'],
    ['◼','◻','✦','✧','♠','♤','◼','◻'],
]

def render_cell(piece):
    return piece.center(CELL_WIDTH)

for row in board:
    print(''.join(render_cell(p) for p in row))