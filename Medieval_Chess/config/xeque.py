import database as db
import combat as comb
# import config.game as g
import calcule as mat
import generation as genera
import selection as select
import methods as mth
import moving as mov

# REGRAS LÓGICAS PARA XEQUE-MATE
def isXeque_Mate(TEAM) -> bool:
    
    ENEMY = select.get_enemy(TEAM)
    
    # Não adianta verificar xeque-mate se o jogo não considerou um rei em xeque ou se existe ainda um principe inimigo
    if ((not db.xeque[TEAM]) or 
        (mth.has_part(TEAM, db.ID_PRINCE[TEAM]))): return False
    
    King = select.getKing(TEAM)
    
    if King is None:
        # transformar o príncipe em REI
        mth.check_KingANDQueen()
        # Tente Novamente
        King = select.getKing(TEAM)
    
    isAttacked = isKingAttacked(King, ENEMY)
    areMovesOccupied_Attacked = areMovesKingOccupied_Attacked(King, TEAM, ENEMY)
    manyAttacksAtKing = countAttacksAtKing(King, ENEMY)
    
    # print(f"Rei está sendo atacado? {isAttacked}")
    # print(f"Todos os movimentos do Rei estão sendo atacados? {areMovesOccupied_Attacked}")
    # print(f"Quantidade de ataques ao Rei: {manyAttacksAtKing}")
    # time.sleep(3)
    
    if (isAttacked and areMovesOccupied_Attacked):
        if manyAttacksAtKing > 1:
            return True
    else:
        return False #os itens abaixo precisam pelo menos que as 2 condições sejam true
    
    Forward = whoAttackKing(King, ENEMY)
    if Forward is None:
        return False
    
    # print(f"Peça atacante ao Rei: {Forward['part']} na posição ({Forward['x']}, {Forward['y']})")
    # print("Não Pode eliminar o atacante? ",cannotKillForward(Forward, TEAM))
    # print("Não Pode impedir o atacante? ",cannotStopForward(Forward, King, TEAM))
    # time.sleep(3)
    
    if (cannotKillForward(Forward, TEAM) and cannotStopForward(Forward, King, TEAM)):
        return True
    
    return False # caso ainda haja esperança 
    
    
# 1. Rei está sendo atacado
def isKingAttacked(King: dict, ENEMY) -> bool:
    i, j = King['coo']
    return len(db.COMBAT[i][j][ENEMY]) > 0

# 2. Todos os movimentos do Rei estão sendo atacados
def areMovesKingOccupied_Attacked(King: dict, TEAM, ENEMY) -> bool:
    iy, ix = King['coo']
    ARENA = db.COMBAT
    
    for dy, dx in db.PART_MOVES_UNIT[King['part']]:
        x = ix + dx
        y = iy + dy   
        
        if not (0 < x < db.game_tbx and 0 < y < db.game_tby):
            continue

        CELL = db.TABLE[y][x]
        CELL_TEAM = CELL['team']
        
        # rei pode fugir se:
        # - não houver peça aliada
        # - a casa não for atacada

        if ((CELL_TEAM != TEAM) and 
            (not len(ARENA[x][y][ENEMY]) > 0)):
            return False
    
    return True

# 3. (>= 2 Ataques ao rei)? Sim: XEQUE-MATE, Não: continue
def countAttacksAtKing(King, ENEMY) -> int:
    i, j = King['coo']
    return len(db.COMBAT[i][j][ENEMY])

# !-> Determinar atacante ao rei
def whoAttackKing(King, ENEMY) -> dict:
    i, j = King['coo']
    FORWARD = db.COMBAT[i][j][ENEMY]

    return FORWARD

# 4. Não é possível eliminar o Atacante ao rei
  # -> Verifica se sua casa está sendo atacado
  # -> Outras peças OU rei está atacando? Simule movimento
                        # -> rei continua em xeque: movimento ilegal, CONTINUE
                        # -> sai do xeque? movimento permitido, NÃO XEQUE
def cannotKillForward(Forward:dict, TEAM) -> bool:
    
    fy, fx = Forward['coo']
    Defenders = list(db.COMBAT[fx][fy][TEAM])
    
    if not Defenders: return True # não há como defender    
    for defender in Defenders:
        # simulação
        genera.Replay('before_move') # salva o estado do jogo antes da simulação
        
        dy, dx = defender['coo']
        PART   = defender['part']
        
        db.TABLE[fy][fx] = {
            'material': db.material[PART],
            'team':     TEAM,
            'part':     PART
        }
    
        db.TABLE[dy][dx] = {
            'material': db.space,
            'team':     db.noteam,
            'part':     db.space
        }
        
        mov.execute_Move((dy,dx), (fy,fx), TEAM)
        
        # checar se o movimento colocou o PROPRIO rei em xeque (movimento ilegal)
        g.set_combat()
        # vw.render_geral_view('', '', team)
        # print(f"Simulando movimento do defensor {defender['part']} para eliminar o atacante...")
        # time.sleep(2)
        
        if (not comb.check_illegal_moviment(TEAM)): # verifica se a jogada é legal
            return comb.valid_move()
            
            # vw.render_geral_view('', '', team)
            # print(f"Fim")
            # time.sleep(10)
        
        else:
            INVALID = comb.invalid_move()
            
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
def get_squares_defend(Forward, partF, King, TEAM):
    fx, fy = Forward['x'], Forward['y']
    kx, ky = King['x'], King['y']
    
    def get_vertical_horizontal_spaces(fx, fy, kx, ky, dx, dy):
        squares = []
        places = []
        for j in range(1, abs(fx-kx-1)):
            for i in range(1, abs(fy-ky-1)):
                x = fx + j*dx
                y = fy + i*dy
                
                squares.append(next((defend for defend in db.by[x][y] if defend['team'] == TEAM), {}))
                places.append([x,y])
        
        return squares, places
    
    def get_vertical_diagonal_spaces(fx, fy, kx, dx, dy):
        squares = []
        places = []
        for i in range(1, abs(fx-kx-1)):
                x = fx + i*dx
                y = fy + i*dy
                
                squares.append(next((defend for defend in db.by[x][y] if defend['team'] == TEAM), {}))
                places.append([x,y])
        
        return squares, places
                
                
    if partF == db.rook: # torre
        dx = 0 if kx == fx else mat.direction(fx,kx)
        dy = 0 if ky == fy else mat.direction(fx,kx)
        
        return get_vertical_horizontal_spaces(fx, fy, kx, ky, dx, dy)
    
    elif partF == db.bishop: # bispo
        dx = mat.direction(fx,kx)
        dy = mat.direction(fx,kx)
        
        return get_vertical_diagonal_spaces(fx, fy, kx, dx, dy)
    
    elif partF == db.queen: # rainha
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
def cannotStopForward(Forward, King, TEAM):
    partF = Forward['part']
    if not (partF in (db.rook, db.bishop, db.queen)): return True # XEQUE-MATE
    
    diffx = abs(Forward['x']-King['x'])
    diffy = abs(Forward['y']-King['y'])
    
    if (diffx in (1,0) and diffy in (1,0)): return True # bloqueio impossível. XEQUE-MATE
    
    squares_defend, places = get_squares_defend(Forward, partF, King, TEAM)
    
    #limpar lista de itens vazios
    squares_defend = list(filter(None, squares_defend))
    
    if not squares_defend: return True # ninguém para bloquear. XEQUE-MATE
    
    old_xeque = db.xeque[TEAM]
    for id, square in squares_defend:
        for defender in square:
            px, py = places[id][0], places[id][1]
            # simulação
            genera.set_history() # salva o estado do jogo antes da simulação
            simu.setSimulation()
            dx, dy = defender['x'], defender['y']
            partD  = defender['part']
            
            db.table[px][py] = {
                'material': db.material[partD],
                'team':     TEAM,
                'part':     partD
            }
        
            db.table[dx][dy] = {
                'material': db.space,
                'team':     db.noteam,
                'part':     db.space
            }
            
            # checar se o movimento colocou o PROPRIO rei em xeque (movimento ilegal)
            g.set_combat()
            
            if not db.xeque[TEAM]: # verifica se a jogada é legal
                genera.get_history()
                return False
            
            else:
                genera.get_history()
    
    return True # nenhuma peça pode bloquear o atacante sem ser um movimento ilegal. XEQUE-MATE
    
    
# Verificar se o jogo está empatado
def isDraw(TEAM):
    enemy = g.rtn_enemy(TEAM)
    King = getKing(enemy)
    
    parts = db.team_parts
    
    # Afogamento, onde o jogador não tem movimentos legais, mas não está em xeque
    if db.quant_move[enemy] == 0 and areMovesKingOccupied_Attacked(King, enemy, TEAM) and not db.xeque[enemy]:
        return True, 1
    
    hasKingTeam = mat.value_exist(parts, TEAM, 'part', db.king)
    hasKingEnemy = mat.value_exist(parts, enemy, 'part', db.king)
    
    # Rei contra Rei, onde os dois jogadores só tem o rei e não podem se atacar
    if len(parts[TEAM]) == 1 and len(parts[enemy]) == 1:
        if hasKingTeam and hasKingEnemy:
            return True, 2
    
    
    if (len(parts[TEAM]) == 1 and len(parts[enemy]) == 2) or (len(parts[TEAM]) == 2 and len(parts[enemy]) == 1):
        
        hasKightTeam = mat.value_exist(parts, TEAM, 'part', db.knight)
        hasKightEnemy = mat.value_exist(parts, enemy, 'part', db.knight)
        
        hasBishopTeam = mat.value_exist(parts, TEAM, 'part', db.bishop)
        hasBishopEnemy = mat.value_exist(parts, enemy, 'part', db.bishop)
        
        # Rei vs Rei e Bispo, onde um jogador tem apenas o rei e o outro tem apenas o rei e um bispo, e não é possível dar xeque-mate
        if ( (hasKingEnemy and hasKingTeam) and (hasBishopTeam or hasBishopEnemy) ):
            return True, 3
    
        # Rei vs Rei e Cavalo, onde um jogador tem apenas o rei e o outro tem apenas o rei e um cavalo, e não é possível dar xeque-mate
        if ( (hasKingEnemy and hasKingTeam) and (hasKightEnemy or hasKightTeam) ):
            return True, 4
    
    return False, 0

def MovesKingAreAttacking(King, TEAM, enemy):
    ix, iy = King['x'], King['y']
    Arena = db.combat
    
    for dx, dy in comb.part_dic[King['part']]:
        x = ix + dx
        y = iy + dy   
        
        if not (0 < x < db.game_tbx and 0 < y < db.game_tby):
            continue

        cell = db.table[x][y]
        # Rei não está sendo pressionado se:
        # - houver peça aliada
        # - a casa não for atacada
        if cell['team'] in (TEAM, db.space) and not Arena[ix][iy][enemy]['attack']:
            return False
    
    return True