import config.data as dt
import config.game as g
import config.selection as selec
import config.generation as genera
import config.view as vw
import os
import config.question as q
import config.menu as m
import config.register as reg
import time

part_dic = {
    dt.rook: [(1, 0), (-1, 0), (0, 1), (0, -1)],
    dt.bishop: [(1, 1), (-1, 1),(-1, -1), (1, -1)],
    dt.queen: [(1, 0), (-1, 0),(0, 1), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)],
    dt.knight: [(2, 1),(2, -1),(-1, 2),(1, 2),(-2, 1),(-2, -1),(-1, -2),(1, -2)],
    dt.king: [(1,0),(1,-1),(1,1),(-1,0),(-1,-1),(-1,1),(0,1),(0,-1)],
    dt.pawn: [(1,-1),(1,0),(1,1),(2,0)]
    
}

def add_attack(x,y,part,team,ix,iy, simulation):
    
    if simulation:
        dt.combat_simul[x][y][team]['move'] = True
        dt.combat_simul[x][y][team]['attack'] = True
    else:
        dt.combat[x][y][team]['move'] = True
        dt.combat[x][y][team]['attack'] = True
    
    dt.quant_move[team]+= 1
    
    add_by_attack(ix, iy,part,team,x,y,simulation)
    
def pawn_add_move(x,y,team, simulation):
    
    if simulation:
        dt.combat_simul[x][y][team]['move'] = True
    else:
        dt.combat[x][y][team]['move'] = True

def add_team_parts(part,team, x,y):
    add_part = {'part': part,'attacks': 0,'fight':0,'x':x,'y':y}
    dt.team_parts[team].append(add_part)

def add_by_attack(ix,iy,part,team,x,y, simulation):
    add_part = {'team': team,'part': part,'x':ix,'y':iy}
    
    if simulation:
        dt.by_simul[x][y].append(add_part)
    else:
        dt.by[x][y].append(add_part)

def update_team_parts():
    # limpar listas de peças
    dt.team_parts = {
        dt.white:[],
        dt.black:[]
    }
    
    for x in range(dt.tb_lenx):
        for y in range(dt.tb_leny):
            
            cell = dt.table[x][y]
            if cell['team'] == dt.noteam:
                continue
            
            add_team_parts(cell['part'],cell['team'],x,y)

def attack(id, part, team, simulation):
    if part['part'] == dt.pawn:
        pawn_attack(id, part, team, part_dic[dt.pawn],simulation)
        
    elif part['part'] in (dt.knight, dt.king):
        one_step_attack(id, part, team, part_dic[part['part']], simulation)
        
    else:
        raycast_attack(id, part, team, part_dic[part['part']], simulation)
        

def pawn_attack (id, part, team, directions, simulation):
    enemy = g.rtn_enemy(team)
    ix, iy = part['x'], part['y']
    
    direct = -1 if team == dt.white else 1
    
    if simulation:
        game = dt.table_simul
    else:
        game = dt.table
    
    total_attacks = 0
    total_fights = 0
    
    for dx, dy in directions:
        x = ix + dx*direct
        y = iy + dy   
        
        if not (0 < x < dt.game_tbx and 0 < y < dt.game_tby):
            continue
        
        canDoubleStep = (team == dt.white and ix == 7) or (team == dt.black and ix == 2)
        if dx == 2 and not canDoubleStep:
            continue
        
        cell = game[x][y]
        
        if dy == 0:
            if cell['team'] == dt.noteam:
                total_attacks+= 1
                pawn_add_move(x,y,team,simulation)
                
        else:
            if cell['team'] == enemy:
                add_attack(x, y, part['part'], team,ix,iy,simulation)
                total_attacks+= 1
                total_fights+= 1
                
                if cell['part'] == dt.king:
                    dt.xeque[enemy] = True
        
    dt.team_parts[team][id]['attacks'] = total_attacks
    dt.team_parts[team][id]['fight'] = total_fights

def one_step_attack(id, part, team, directions, simulation):
    enemy = g.rtn_enemy(team)
    ix, iy = part['x'], part['y']
    
    if simulation:
        game = dt.table_simul
    else:
        game = dt.table
        
    total_attacks = 0
    total_fights = 0
    
    for dx, dy in directions:
        x = ix + dx
        y = iy + dy   
        
        if not (0 < x < dt.game_tbx and 0 < y < dt.game_tby):
            continue

        cell = game[x][y]
        
        if cell['team'] == team:
            dt.combat[x][y][team]['attack'] = True
            continue
        
        # contabilizar ataque se tiver um inimigo no local
        total_attacks+=1
        if cell['team'] not in [team, dt.noteam]:
            total_fights+= 1
            
        add_attack(x, y, part['part'], team,ix,iy, simulation)
        
        if cell['team'] == enemy:
            if cell['part'] == dt.king:
                dt.xeque[enemy] = True
            continue
        
    dt.team_parts[team][id]['attacks'] = total_attacks
    dt.team_parts[team][id]['fight'] = total_fights
        
    
            
def raycast_attack(id, part, team, directions, simulation):
    
    if simulation:
        game = dt.table_simul
    else:
        game = dt.table
    
    enemy = g.rtn_enemy(team)
    ix, iy = part['x'], part['y']
    
    total_attacks = 0
    total_fights = 0
    
    for dx, dy in directions:
        for step in range(1, max(dt.game_tbx, dt.game_tby)):
            x = ix + step * dx
            y = iy + step * dy   
            
            if not (0 < x < dt.game_tbx and 0 < y < dt.game_tby):
                break

            cell = game[x][y]
            
            if cell['team'] == team:
                dt.combat[x][y][team]['attack'] = True
                break
            
            # contabilizar ataque se tiver um inimigo no local
            total_attacks+=1
            if cell['team'] not in [team, dt.noteam]:
                total_fights+= 1
                
            add_attack(x, y, part['part'], team,ix,iy, simulation)
            
            if cell['team'] == enemy:
                if cell['part'] == dt.king:
                    dt.xeque[enemy] = True
                break
        
    dt.team_parts[team][id]['attacks'] = total_attacks
    dt.team_parts[team][id]['fight'] = total_fights
        
                
    
def set_combat_table(simulation=False):
    
    dt.quant_move[dt.white] = 0
    dt.quant_move[dt.black] = 0
    
    dt.xeque[dt.white] = False
    dt.xeque[dt.black] = False
    
    dt.combat = [[{dt.white:{'move':False,'attack':False}, dt.black:{'move':False,'attack':False}} for _ in range(10)] for _ in range(10)]
    
    dt.by = [[[] for _ in range(10)] for _ in range(10)]
    
    for team in dt.team_parts:
        for id, part in enumerate(dt.team_parts[team]):
            
            attack(id, part, team, simulation)
    
def get_all_spaces_attack(part_table, x, y):
    spaces = []
    for j, row in enumerate(dt.by):              # matriz
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

def execute_attack(sx, sy, ally, enemy):
    # setar historico
    genera.set_history()
    forwardX, forwardY = selec.find_pre_selection()
    
    # ATACAR!
    pts = dt.material[dt.table[sx][sy]['part']]
    
    dt.table[sx][sy] = {
        'material': dt.table[forwardX][forwardY]['material'],
        'team':     ally,
        'part':     dt.table[forwardX][forwardY]['part']
    }
    
    dt.table[forwardX][forwardY] = {
        'material': dt.space,
        'team':     dt.noteam,
        'part':     dt.space
    }
    
    # checar se o movimento colocou o PROPRIO rei em xeque (movimento ilegal)
    g.set_combat()
    # exibir xeques
    # print(f"XEQUE aos PRETOS: {'SIM' if dt.xeque[dt.black] else 'NÃO'}")
    # print(f"XEQUE aos BRANCOS: {'SIM' if dt.xeque[dt.white] else 'NÃO'}")
    # time.sleep(2)
    
    if dt.xeque[ally]:
        # retornar estado anterior
        genera.get_history()
        os.system('cls')
        print("<------ JOGADA ILEGAL! ------>\n Seu rei ficaria exposto AO XEQUE!.")
        time.sleep(2)
        return False
    
    else:
        # ganho de material:
        dt.wasCaptured = True if pts > 0 else False
        
        dt.score_game[ally] += pts
        dt.score_game[enemy] -= pts
        m.set_historic_score(dt.score_game[dt.white], dt.score_game[dt.black])
        
        g.setInfo_part_play(dt.table[sx][sy]['part'], ally, sx, sy, forwardX, forwardY)
        
        # key = [k for k, v in dt.db.items() if v == dt.part_play['part']][0]
        # team = [k for k, v in dt.db.items() if v == dt.part_play['team']][0]
        # print(f"Peça JOGDADA (part_play): quem? {key.upper()} do time {team.upper()} para a posição ({dt.part_play['newx']}, {dt.part_play['newy']}) saindo de ({dt.part_play['oldx']}, {dt.part_play['oldy']})")
        # time.sleep(4)
        
        capture = True if pts > 0 else False
        reg.setMovesCode(capture)
        
        selec.reset_selection()
        # uma forma mais visual de mostrar a peça atacando o espaço
        dt.selection[forwardX][forwardY] = 5
        dt.selection[sx][sy] = 4
        g.change_turn()
        return True

def setPromotePawn(sx, sy, team):
    os.system('cls')
    x = 1 if team == dt.white else 8
    print("___________________________________________\n")
    for y in range(10):
            
        if y == 0 or y == 9:
            continue
            
        vw.printCell(x,y)
        
    print("\n___________________________________________")
    print("PEÃO PROMOVIDO! Escolha a peça para a promoção:")
    options = [dt.queen, dt.rook, dt.bishop, dt.knight]
    
    VIEW = [dt.parts[team][dt.queen], dt.parts[team][dt.rook], dt.parts[team][dt.bishop], dt.parts[team][dt.knight]]
    
    CHOICE = q.question(VIEW)
    
    chosen_piece = options[CHOICE]
    
    dt.score_game[team] += dt.material[chosen_piece]
    m.set_historic_score(dt.score_game[dt.white], dt.score_game[dt.black])
    
    dt.table[sx][sy] = {
        'material': dt.material[chosen_piece],
        'team':     team,
        'part':     chosen_piece
    }
    
    reg.setPromotion(chosen_piece)
    
    selec.reset_selection()
    # uma forma mais visual de mostrar a peça atacando o espaço
    dt.selection[sx][sy] = 4
    os.system('cls')
    vw.render_view_with_score('', '', team)
    time.sleep(2)
    selec.reset_selection()
    g.set_combat()

def get_PartsAttackedBy(part, x, y,team):
    attacked = []
    for idj, j in enumerate(dt.by):
        for idi, i in enumerate(j):
            if i == [] or i == None or i == {}:
                    continue
            else:
                for cell in i:
                    if cell == [] or cell == None or cell == {}:
                        continue
                    elif {'team': team,'part': part,'x':x,'y':y} == cell:
                        if dt.table[idj][idi]['team'] != dt.noteam:
                            attacked.append(dt.table[idj][idi])
                    
    lista = [f"{dt.names[a['part']]} do time {dt.names[a['team']]}" for a in attacked]
    # print(f"Peças atacadas por {dt.names[part]} em ({x}, {y}): {lista}")
    # time.sleep(5)
    return attacked