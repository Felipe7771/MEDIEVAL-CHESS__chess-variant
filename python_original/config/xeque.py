import config.data as dt
import config.combat as comb
import config.game as g
import config.simulation as simu
import config.calcule as mat
import config.generation as genera

def getKing(team):
    parts = dt.team_parts[team]
    return next((p for p in parts if p['part'] == dt.king), None)

def KingUndefined():
    print()

# REGRAS LÓGICAS PARA XEQUE-MATE
def isXeque_Mate(team):
    
    enemy = g.rtn_enemy(team)
    
    # Não adianta verificar xeque-mate se o jogo não considerou um rei em xeque
    if not dt.xeque[team]: return False
    
    King = getKing(team)
    
    if King is None:
        KingUndefined()
        return False
    
    isAttacked = isKingAttacked(King, enemy)
    areMovesOccupied_Attacked = areMovesKingOccupied_Attacked(King, team, enemy)
    manyAttacksAtKing = countAttacksAtKing(King, enemy)
    
    # print(f"Rei está sendo atacado? {isAttacked}")
    # print(f"Todos os movimentos do Rei estão sendo atacados? {areMovesOccupied_Attacked}")
    # print(f"Quantidade de ataques ao Rei: {manyAttacksAtKing}")
    # time.sleep(3)
    
    if (isAttacked and areMovesOccupied_Attacked):
        if manyAttacksAtKing > 1:
            return True
    else:
        return False #os itens abaixo precisam pelo menos que as 2 condições sejam true
    
    Forward = whoAttackKing(King, enemy)
    if Forward is None:
        return False
    
    # print(f"Peça atacante ao Rei: {Forward['part']} na posição ({Forward['x']}, {Forward['y']})")
    # print("Não Pode eliminar o atacante? ",cannotKillForward(Forward, team))
    # print("Não Pode impedir o atacante? ",cannotStopForward(Forward, King, team))
    # time.sleep(3)
    
    if (cannotKillForward(Forward, team) and cannotStopForward(Forward, King, team)):
        return True
    
    return False # caso ainda haja esperança 
    
    
# 1. Rei está sendo atacado
def isKingAttacked(King, enemy):
    return dt.combat[King['x']][King['y']][enemy]['attack']

# 2. Todos os movimentos do Rei estão sendo atacados
def areMovesKingOccupied_Attacked(King, team, enemy):
    ix, iy = King['x'], King['y']
    Arena = dt.combat
    
    for dx, dy in comb.part_dic[King['part']]:
        x = ix + dx
        y = iy + dy   
        
        if not (0 < x < dt.game_tbx and 0 < y < dt.game_tby):
            continue

        cell = dt.table[x][y]
        
        # rei pode fugir se:
        # - não houver peça aliada
        # - a casa não for atacada
        # print(f"Analisando casa ({x}, {y}): Peça: {cell['part']} Time: {cell['team']} Ataque inimigo: {Arena[x][y][enemy]['attack']}")
        # if cell['team'] != team:
        #     print(f"  --casa ({x}, {y}): Peça: {cell['part']} Ataque inimigo: {Arena[x][y][enemy]['attack']}")
        # time.sleep(1)
        if cell['team'] != team and not Arena[x][y][enemy]['attack']:
            return False
    
    return True

# 3. (>= 2 Ataques ao rei)? Sim: XEQUE-MATE, Não: continue
def countAttacksAtKing(King, enemy):
    x, y = King['x'], King['y']
    return len([enemys for enemys in dt.by[x][y] if enemys['team'] == enemy])

# !-> Determinar atacante ao rei
def whoAttackKing(King, enemy):
    x, y = King['x'], King['y']
    return next((forward for forward in dt.by[x][y] if forward['team'] == enemy), None)

# 4. Não é possível eliminar o Atacante ao rei
  # -> Verifica se sua casa está sendo atacado
  # -> Outras peças OU rei está atacando? Simule movimento
                        # -> rei continua em xeque: movimento ilegal, CONTINUE
                        # -> sai do xeque? movimento permitido, NÃO XEQUE
def cannotKillForward(Forward, team):
    fx, fy = Forward['x'], Forward['y']
    Defenders = [defend for defend in dt.by[fx][fy] if defend['team'] == team]
    
    # print(f"Defensores da peça atacante: {[defender['part'] for defender in Defenders]}")
    
    if not Defenders: return True # não há como defender
    old_xeque = dt.xeque[team]
    
    for defender in Defenders:
        # simulação
        simu.setSimulation()
        genera.set_history() # salva o estado do jogo antes da simulação
        
        dx, dy = defender['x'], defender['y']
        partD   = defender['part']
        
        dt.table[fx][fy] = {
            'material': dt.material[partD],
            'team':     team,
            'part':     partD
        }
    
        dt.table[dx][dy] = {
            'material': dt.space,
            'team':     dt.noteam,
            'part':     dt.space
        }
        
        # checar se o movimento colocou o PROPRIO rei em xeque (movimento ilegal)
        g.set_combat()
        # vw.render_geral_view('', '', team)
        # print(f"Simulando movimento do defensor {defender['part']} para eliminar o atacante...")
        # time.sleep(2)
        
        if not dt.xeque[team]: # verifica se a jogada é legal
            genera.get_history()
            
            # vw.render_geral_view('', '', team)
            # print(f"Fim")
            # time.sleep(10)
            
            return False
        
        else:
            genera.get_history()
            
    # vw.render_geral_view('', '', team)
    # print(f"Fim")
    # time.sleep(10)
    return True # nenhuma peça pode matar o atacante sem ser um movimento ilegal
        
# 5. Não é possível impedir atacante
  # determina peça do atacante
    # -> Não é (torre, bispo, rainha)? XEQUE-MATE
  # determine os espaços de análise
        # Torre: qual coordenada é igual a do rei? Essa é a linha de análise 
        # Bispo: bx > rx: ande +1 by > ry: ande -1 Ambos ao mesmo tempo, essas serão as casas de analise 
        # Rainha: Se tem uma coordenadora igual, faça como a torre, se não, faça como o Bispo
def get_squares_defend(Forward, partF, King, team):
    fx, fy = Forward['x'], Forward['y']
    kx, ky = King['x'], King['y']
    
    def get_vertical_horizontal_spaces(fx, fy, kx, ky, dx, dy):
        squares = []
        places = []
        for j in range(1, abs(fx-kx-1)):
            for i in range(1, abs(fy-ky-1)):
                x = fx + j*dx
                y = fy + i*dy
                
                squares.append(next((defend for defend in dt.by[x][y] if defend['team'] == team), {}))
                places.append([x,y])
        
        return squares, places
    
    def get_vertical_diagonal_spaces(fx, fy, kx, dx, dy):
        squares = []
        places = []
        for i in range(1, abs(fx-kx-1)):
                x = fx + i*dx
                y = fy + i*dy
                
                squares.append(next((defend for defend in dt.by[x][y] if defend['team'] == team), {}))
                places.append([x,y])
        
        return squares, places
                
                
    if partF == dt.rook: # torre
        dx = 0 if kx == fx else mat.direction(fx,kx)
        dy = 0 if ky == fy else mat.direction(fx,kx)
        
        return get_vertical_horizontal_spaces(fx, fy, kx, ky, dx, dy)
    
    elif partF == dt.bishop: # bispo
        dx = mat.direction(fx,kx)
        dy = mat.direction(fx,kx)
        
        return get_vertical_diagonal_spaces(fx, fy, kx, dx, dy)
    
    elif partF == dt.queen: # rainha
        if kx == fx or ky == fy:
            dx = 0 if kx == fx else mat.direction(fx,kx)
            dy = 0 if ky == fy else mat.direction(fx,kx)
            
            return get_vertical_horizontal_spaces(fx, fy, kx, ky, dx, dy)
        
        else:
            dx = mat.direction(fx,kx)
            dy = mat.direction(fx,kx) 
            
            return get_vertical_diagonal_spaces(fx, fy, kx, dx, dy)
    
    # tamanho da lista de espaços de análise? XEQUE-MATE
  # verifique se tem peças aliadas em movimento a esse espaços de analise
        # Não tem? XEQUE-MATE
        # tem? Simule movimento
                        # -> rei continua em xeque: movimento ilegal, IGNORE ESSA PEÇA CONTINUE
                        # -> sai do xeque? movimento permitido, NÃO XEQUE
        # nenhum conseque? XEQUE-MATE
def cannotStopForward(Forward, King, team):
    partF = Forward['part']
    if not (partF in (dt.rook, dt.bishop, dt.queen)): return True # XEQUE-MATE
    
    diffx = abs(Forward['x']-King['x'])
    diffy = abs(Forward['y']-King['y'])
    
    if (diffx in (1,0) and diffy in (1,0)): return True # bloqueio impossível. XEQUE-MATE
    
    squares_defend, places = get_squares_defend(Forward, partF, King, team)
    
    #limpar lista de itens vazios
    squares_defend = list(filter(None, squares_defend))
    
    if not squares_defend: return True # ninguém para bloquear. XEQUE-MATE
    
    old_xeque = dt.xeque[team]
    for id, square in squares_defend:
        for defender in square:
            px, py = places[id][0], places[id][1]
            # simulação
            genera.set_history() # salva o estado do jogo antes da simulação
            simu.setSimulation()
            dx, dy = defender['x'], defender['y']
            partD  = defender['part']
            
            dt.table[px][py] = {
                'material': dt.material[partD],
                'team':     team,
                'part':     partD
            }
        
            dt.table[dx][dy] = {
                'material': dt.space,
                'team':     dt.noteam,
                'part':     dt.space
            }
            
            # checar se o movimento colocou o PROPRIO rei em xeque (movimento ilegal)
            g.set_combat()
            
            if not dt.xeque[team]: # verifica se a jogada é legal
                genera.get_history()
                return False
            
            else:
                genera.get_history()
    
    return True # nenhuma peça pode bloquear o atacante sem ser um movimento ilegal. XEQUE-MATE
    
    
# Verificar se o jogo está empatado
def isDraw(team):
    enemy = g.rtn_enemy(team)
    King = getKing(enemy)
    
    parts = dt.team_parts
    
    # Afogamento, onde o jogador não tem movimentos legais, mas não está em xeque
    if dt.quant_move[enemy] == 0 and areMovesKingOccupied_Attacked(King, enemy, team) and not dt.xeque[enemy]:
        return True, 1
    
    hasKingTeam = mat.value_exist(parts, team, 'part', dt.king)
    hasKingEnemy = mat.value_exist(parts, enemy, 'part', dt.king)
    
    # Rei contra Rei, onde os dois jogadores só tem o rei e não podem se atacar
    if len(parts[team]) == 1 and len(parts[enemy]) == 1:
        if hasKingTeam and hasKingEnemy:
            return True, 2
    
    
    if (len(parts[team]) == 1 and len(parts[enemy]) == 2) or (len(parts[team]) == 2 and len(parts[enemy]) == 1):
        
        hasKightTeam = mat.value_exist(parts, team, 'part', dt.knight)
        hasKightEnemy = mat.value_exist(parts, enemy, 'part', dt.knight)
        
        hasBishopTeam = mat.value_exist(parts, team, 'part', dt.bishop)
        hasBishopEnemy = mat.value_exist(parts, enemy, 'part', dt.bishop)
        
        # Rei vs Rei e Bispo, onde um jogador tem apenas o rei e o outro tem apenas o rei e um bispo, e não é possível dar xeque-mate
        if ( (hasKingEnemy and hasKingTeam) and (hasBishopTeam or hasBishopEnemy) ):
            return True, 3
    
        # Rei vs Rei e Cavalo, onde um jogador tem apenas o rei e o outro tem apenas o rei e um cavalo, e não é possível dar xeque-mate
        if ( (hasKingEnemy and hasKingTeam) and (hasKightEnemy or hasKightTeam) ):
            return True, 4
    
    return False, 0

def MovesKingAreAttacking(King, team, enemy):
    ix, iy = King['x'], King['y']
    Arena = dt.combat
    
    for dx, dy in comb.part_dic[King['part']]:
        x = ix + dx
        y = iy + dy   
        
        if not (0 < x < dt.game_tbx and 0 < y < dt.game_tby):
            continue

        cell = dt.table[x][y]
        # Rei não está sendo pressionado se:
        # - houver peça aliada
        # - a casa não for atacada
        if cell['team'] in (team, dt.space) and not Arena[ix][iy][enemy]['attack']:
            return False
    
    return True