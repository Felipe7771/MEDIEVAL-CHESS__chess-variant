import config.data as dt
import os

letter_part = {
    dt.pawn: '',
    dt.rook: 'T',
    dt.bishop: 'B',
    dt.knight: 'C',
    dt.queen: 'D',
    dt.king: 'R'
}

coo_y = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h'
}

def setMovesCode(capture):
    oldy, oldx = dt.part_play['oldy'], dt.part_play['oldx']
    newy, newx = dt.part_play['newy'], dt.part_play['newx']
    team = dt.part_play['team']
    part = dt.part_play['part']
    
    dt.coo_moves = letter_part[part]
    dt.coo_moves += str('x' if capture else '')
    
    coo = str(coo_y[newy]) + str(newx)
    dt.coo_moves += coo
    
def setPromotion(promotion):
    dt.coo_moves += '=' + str(letter_part[promotion])
    
def setIcon(icon):
    dt.coo_moves += str(icon)
    
def setMoveToList():
    dt.arq_moves.append(dt.coo_moves)
    dt.coo_moves = ''
    
def createRegister():
    names = [dt.players[dt.white], dt.players[dt.black]]
    x = 6
    names = [names[0][:x], names[1][:x]]
    
    arq_name = 'games/' + names[0] + 'VS' + names[1]
    arq_raiz = arq_name
    a = 0
    while True:
        extra = str(a)
        arq_name = arq_raiz + (extra if a > 0 else '')
        
        if os.path.exists(arq_name):
            a +=1
        else:
            break
        
    arq_name+='.txt'
    
    with open(arq_name,'w',encoding="utf-8") as f:
        f.write(" ".join(dt.arq_moves))
    
    
    