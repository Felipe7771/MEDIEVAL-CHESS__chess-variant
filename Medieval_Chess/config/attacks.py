import database as db
import selection as select

# verificar se a casa de ataque coincide com o rei inimigo
def is_AttackKing(CELL, ENEMY):
    ID = db.ID_PRINCE[ENEMY]
    
    return select.has_part(ENEMY, ID) and CELL['team'] == ENEMY and CELL['part'] == db.king

# ==================================================
# Assignment of attacked squares in the COMBAT table    
# ==================================================
# adicionar casa de ataque no COMBAT
# junto a informações da peça atacante e onde se localiza
# --------------------------------------------------

def add_ACTION(ID_PART, NEW_COO, PART, TEAM, INITIAL_COO, ATTACK=True, WALK=True):
    
    iy, ix = INITIAL_COO
    y, x = NEW_COO
    
    ADD_PART = {
        'id': ID_PART,
        'part': PART, 
        'coo': (iy, ix)
    }
    
    if (ATTACK):
        db.COMBAT[y][x][TEAM].append(ADD_PART)
    
    if (WALK):
        db.MOVE[y][x][TEAM].append(ADD_PART)

def set_Jester_ATTACK(ID_PART, COO, PART, TEAM, MOVES, SECOND_MOVE):
    ENEMY = select.rtn_enemy(TEAM)
    iy, ix = COO
    
    # determinando qual movimento será feito
    INDICE_MOVE = 1 if SECOND_MOVE else 0
    MOVES = MOVES[INDICE_MOVE]
    
    TOTAL_ATTACKS = 0
    TOTAL_MOVES   = 0
    
    for dy, dx in MOVES:
        for STEP in range(1, 4):
            y = iy + dy*STEP   
            x = ix + dx*STEP
            
            if (not ((0 < y < db.game_Ylenght) and 
                    (0 < x < db.game_Xlenght))):
                break

            CELL = db.TABLE[y][x]
            CELL_TEAM = CELL['team']
            
            if (not SECOND_MOVE):
                # Podemos atacar no primeiro lance
                # Peças também atacam casas aliadas, porém como defesa, logo, não adiciona ao total de ataques
                if (CELL_TEAM == TEAM):
                    add_ACTION(ID_PART, (y, x), PART, TEAM, COO,WALK=False)
                    break
                
                # contabilizar ataque se tiver um inimigo no local
                TOTAL_MOVES +=1
                add_ACTION(ID_PART, (y, x), PART, TEAM, COO)
                
                if (CELL_TEAM == ENEMY):
                    TOTAL_ATTACKS +=1
                
                    if is_AttackKing(CELL, ENEMY):
                        db.XEQUE[ENEMY] = True
                    break
            
            else:
                # Só podemos andar no segundo lance, logo, só anda se estiver vazio
                if ((CELL_TEAM == db.noteam)):
                    TOTAL_MOVES +=1
                    add_ACTION(ID_PART, (y, x), PART, TEAM, COO, ATTACK=False)
                else:
                    break
                    
            

    db.PART_TEAM[TEAM][ID_PART]['attacks'] = TOTAL_ATTACKS
    db.PART_TEAM[TEAM][ID_PART]['moves']   = TOTAL_MOVES 

def set_Pawn_ATTACK(ID_PART, COO, PART, TEAM, MOVES):
    ENEMY = select.rtn_enemy(TEAM)
    iy, ix = COO
        
    TOTAL_ATTACKS = 0
    TOTAL_MOVES   = 0
    
    for dy, dx in MOVES:
        y = iy + dy   
        x = ix + dx
        
        if (not ((0 < y < db.game_Ylenght) and 
                 (0 < x < db.game_Xlenght))):
            continue

        CELL = db.TABLE[y][x]
        CELL_TEAM = CELL['team']
        
        # Se dx == 0, ele está se movendo na vertical, sem ataque e só se move se ninguem estiver lá
        if ((dx == 0) and (CELL_TEAM == db.noteam)):
            TOTAL_MOVES +=1
            add_ACTION(ID_PART, (y, x), PART, TEAM, COO, False)
            continue
        
        # Peças também atacam casas aliadas, porém como defesa, logo, não adiciona ao total de ataques
        if (CELL_TEAM == TEAM):
            add_ACTION(ID_PART, (y, x), PART, TEAM, COO,WALK=False)
            continue
        
        # contabilizar ataque se tiver um inimigo no local
        if (CELL_TEAM == ENEMY):
            TOTAL_MOVES +=1
            TOTAL_ATTACKS +=1
            
            add_ACTION(ID_PART, (y, x), PART, TEAM, COO)
        
            if is_AttackKing(CELL, ENEMY):
                db.XEQUE[ENEMY] = True
        
    db.PART_TEAM[TEAM][ID_PART]['attacks'] = TOTAL_ATTACKS
    db.PART_TEAM[TEAM][ID_PART]['moves']   = TOTAL_MOVES

def set_OneStep_ATTACK(ID_PART, COO, PART, TEAM, MOVES):
    ENEMY = select.rtn_enemy(TEAM)
    iy, ix = COO
        
    TOTAL_ATTACKS = 0
    TOTAL_MOVES   = 0
    
    for dy, dx in MOVES:
        y = iy + dy   
        x = ix + dx
        
        if (not ((0 < y < db.game_Ylenght) and 
                 (0 < x < db.game_Xlenght))):
            continue

        CELL = db.TABLE[y][x]
        CELL_TEAM = CELL['team']
        
        # Peças também atacam casas aliadas, porém como defesa, logo, não adiciona ao total de ataques
        if (CELL_TEAM == TEAM):
            add_ACTION(ID_PART, (y, x), PART, TEAM, COO,WALK=False)
            continue
        
        # contabilizar ataque se tiver um inimigo no local
        TOTAL_MOVES +=1
        
        if (CELL_TEAM == ENEMY):
            TOTAL_ATTACKS +=1
        
        if is_AttackKing(CELL, ENEMY):
            db.XEQUE[ENEMY] = True
            
        add_ACTION(ID_PART, (y, x), PART, TEAM, COO)
        
    db.PART_TEAM[TEAM][ID_PART]['attacks'] = TOTAL_ATTACKS
    db.PART_TEAM[TEAM][ID_PART]['moves']   = TOTAL_MOVES       
            
def set_RayCast_ATTACK(ID_PART, COO, PART, TEAM, MOVES, QUANT_MOVES=8):
    ENEMY = select.rtn_enemy(TEAM)
    iy, ix = COO
        
    TOTAL_ATTACKS = 0
    TOTAL_MOVES   = 0
    
    for dy, dx in MOVES:
        for STEP in range(1, QUANT_MOVES+1):
            y = iy + dy*STEP   
            x = ix + dx*STEP
            
            if (not ((0 < y < db.game_Ylenght) and 
                    (0 < x < db.game_Xlenght))):
                break

            CELL = db.TABLE[y][x]
            CELL_TEAM = CELL['team']
            
            # Peças também atacam casas aliadas, porém como defesa, logo, não adiciona ao total de ataques
            if (CELL_TEAM == TEAM):
                add_ACTION(ID_PART, (y, x), PART, TEAM, COO,WALK=False)
                break
            
            # contabilizar ataque se tiver um inimigo no local
            TOTAL_MOVES +=1
            add_ACTION(ID_PART, (y, x), PART, TEAM, COO)
            
            if (CELL_TEAM == ENEMY):
                TOTAL_ATTACKS +=1
            
                if is_AttackKing(CELL, ENEMY):
                    db.XEQUE[ENEMY] = True
                break
                

    db.PART_TEAM[TEAM][ID_PART]['attacks'] = TOTAL_ATTACKS
    db.PART_TEAM[TEAM][ID_PART]['moves']   = TOTAL_MOVES 
    
def get_all_spaces_attack(part_table, x, y):
    spaces = []
    for j, row in enumerate(db.by):              # matriz
        for i, cell in enumerate(row):           # cada célula
            for space in cell:     # lista dentro da célula
                if (
                    isinstance(space, dict)
                    and space.get('team') == part_table['team']
                    and space.get('x') == x
                    and space.get('y') == y
                ):
                    attack = {**space}
                    attack['x'] = j
                    attack['y'] = i
                    spaces.append(attack)

    return spaces