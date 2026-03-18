import config.data as dt

def move_selection(sx, sy, move, team):
    # print(move)
    # time.sleep(1)
    moves = {
        'd': right_move_selec,
        'a': left_move_selec,
        'w': up_move_selec,
        's': down_move_selec,
    }

    part_selec = moves[move](sx, sy, dt.team_parts[team])
    
    p_sx, p_sy = part_selec['x'], part_selec['y']
    
    dt.selection[sx][sy] = 0
    dt.selection[p_sx][p_sy] = 1
    
def move_selection_attack(sx, sy, move, attack_spaces):
    moves = {
        'd': right_move_selec,
        'a': left_move_selec,
        'w': up_move_selec,
        's': down_move_selec,
    }

    part_selec = moves[move](sx, sy, attack_spaces)
    
    if(not part_selec):
        return
    
    p_sx, p_sy = part_selec['x'], part_selec['y']
    
    dt.selection[sx][sy] = 3
    dt.selection[p_sx][p_sy] = 1
    
#--------------------------------------------------------------
def right_move_selec(sx, sy, Arena):
    closed_parts = [p for p in Arena if p['y'] > sy]

    if closed_parts:
        selec_part = min(closed_parts, key=lambda p: (p['y'] - sy, abs(p['x'] - sx)))
        # print(closed_parts)
        # time.sleep(5)
        
    
    else:
        closed_parts = [p for p in Arena if p['y'] < sy]
        # print(closed_parts)
        # time.sleep(5)
        if not closed_parts:
            return None
        else:
            selec_part = max(closed_parts, key=lambda p: (sy - p['y'], -abs(p['x'] - sx)))
    
    return selec_part
#--------------------------------------------------------------
def left_move_selec(sx, sy, Arena):
    closed_parts = [p for p in Arena if p['y'] < sy]

    if closed_parts:
        selec_part = min(closed_parts, key=lambda p: (sy - p['y'], abs(p['x'] - sx)))
    
    else:
        closed_parts = [p for p in Arena if p['y'] > sy]
        
        if not closed_parts:
            return None
        else:
            selec_part = max(closed_parts, key=lambda p: (p['y'] - sy, -abs(p['x'] - sx)))
    
    return selec_part
#--------------------------------------------------------------
def up_move_selec(sx, sy, Arena):
    closed_parts = [p for p in Arena if p['x'] < sx]

    if closed_parts:
        selec_part = min(closed_parts, key=lambda p: (sx - p['x'], abs(p['y'] - sy)))
    
    else:
        closed_parts = [p for p in Arena if p['x'] > sx]

        if not closed_parts:
            return None
        else:
            selec_part = max(closed_parts, key=lambda p: (p['x'] - sx, -abs(p['y'] - sy)))
    
    return selec_part
#--------------------------------------------------------------
def down_move_selec(sx, sy, Arena):
    # print(f'{sx}, {sy}')
    closed_parts = [p for p in Arena if p['x'] > sx]
    # print(closed_parts)
    # time.sleep(5)

    if closed_parts:
        selec_part = min(closed_parts, key=lambda p: (p['x'] - sx, abs(p['y'] - sy)))
        # print(selec_part)
        # time.sleep(5)
    
    else:
        closed_parts = [p for p in Arena if p['x'] < sx]
        
        if not closed_parts:
            return None
        else:
            selec_part = max(closed_parts, key=lambda p: (sx - p['x'], -abs(p['y'] - sy)))
    
    return selec_part

    
def find_selection():
    for x in range(len(dt.selection)):
        if 1 in dt.selection[x]:
            for y in range(len(dt.selection)):
                
                if dt.selection[x][y] == 1:
                    return x, y


def set_selection_combat(space_attack, sx, sy):
    for space in space_attack:
        px, py = space['x'], space['y']
        
        dt.selection[px][py] = 3
            
    dt.selection[sx][sy] = 2
            
    dt.selection[space_attack[0]['x']][space_attack[0]['y']] = 1
    
# limpar selection, MAS a casa com valor 2 volta a ser 1, o restante voltam a ser 0
def clear_selection():
    for x in range(len(dt.selection)):
        for y in range(len(dt.selection)):
            if dt.selection[x][y] == 2:
                dt.selection[x][y] = 1
            else:
                dt.selection[x][y] = 0
                
# limper toda a selection, todas as casas voltam a ser 0
def reset_selection():
    for x in range(len(dt.selection)):
        for y in range(len(dt.selection)):
            dt.selection[x][y] = 0
            
# pegar as coordenadas da casa com valor 2
def find_pre_selection():
    for x in range(len(dt.selection)):
        if 2 in dt.selection[x]:
            for y in range(len(dt.selection)):
                
                if dt.selection[x][y] == 2:
                    return x, y