import config.data as dt
import config.view as vw
import config.combat as comb
import config.generation as genera
import config.simbols as simb
import config.xeque as x
import config.question as q
import config.selection as selec
import random
import config.register as reg
import time
import os
# altera o turno mundando de preto para branco e vice-versa
# muda o id do turno

def id_team(team):
    return 0 if team == dt.white else 1

def id_enemy(team):
    return 1 if team == dt.white else 0

def rtn_team(team):
    return dt.white if team == dt.white else dt.black

def rtn_enemy(team):
    return dt.black if team == dt.white else dt.white
    
def change_turn():
    dt.id_turn = (dt.id_turn + 1) % 2
    
def random_team(names):
    k = random.randint(0,1)
    dt.players[dt.white] = names[k]
    dt.players[dt.black] = names[1-k]

def get_team_part(x,y, team):
    return next((part for part in dt.team_parts[team] if part['x'] == x and part['y'] == y), None)
    
def setInfo_part_play(part, team, newx, newy, oldx, oldy):
    dt.part_play = {
        'part': part,
        'team': team,
        'newx': newx,
        'newy': newy,
        'oldx': oldx,
        'oldy': oldy
    }
def BeginingGame(names):
    os.system('cls')
    random_team(names)
    print("Carregando...")
    time.sleep(1)
    os.system('cls')
    
    print(f'(PRETOS)\n"{dt.players[dt.black]}"\n\n------- VS -------\n\n"{dt.players[dt.white]}"\n(BRANCOS)')
    time.sleep(3)
    
    resetGame()
    
    genera.set_table_game()
    setTurn()
    dt.id_turn = 0
    
    LoopGame()

def resetGame():
    arq_moves = []
    
    dt.list_simbols = []
    
    dt.score_game = {
        dt.black: 0,
        dt.white: 0
    }
    
    dt.xeque = {
        dt.white: False,
        dt.black: False
    }

    dt.table = [[
        {
            'material': dt.space,
            'team':     dt.noteam,
            'part':     dt.space
        } 
        for _ in range(10)] for _ in range(10)]

    dt.quant_move = {
        dt.white: 0,
        dt.black: 0
    }

    dt.selection = [[0 for _ in range(10)] for _ in range(10)]

def set_combat():
    comb.update_team_parts()
    comb.set_combat_table()

def setTurn():
    set_combat()
    change_turn()
    
def endGame(winner, type_end, type_draw = 0):
    os.system('cls')
    ViewTable(dt.list_simbols, winner, end=True)
    reg.createRegister()
    time.sleep(1.5)
    
    if type_end == 'EMPATE':
        name_draw = dt.type_draw[type_draw]['name']
        description_draw = dt.type_draw[type_draw]['description']
        print("E M P A T E!")
        time.sleep(1)
        print(f'por {name_draw}...')
        time.sleep(2)
        print(f"{description_draw}")
        time.sleep(3)
        
    elif type_end == 'XEQUE-MATE':
        enemy = rtn_enemy(winner)
        
        print("X E Q U E - M A T E!")
        time.sleep(1)
        print(f"O Rei de {dt.players[enemy]} está MORTO não importa o movimento que faça...")
        time.sleep(2)
        print(f'\nVitória de {dt.players[winner].upper()}! ({dt.score_game[winner]} pontos)')

        time.sleep(3)
    
    NextGame()
    
def LoopGame():
    # Tipo de final: XEQUE-MATE E EMPATE
    type_end = ''
    endgame = False
    while True:
        ally  = dt.turns[dt.id_turn]
        enemy = rtn_enemy(ally)
        
        King = x.getKing(ally)
        dt.selection[King['x']][King['y']] = 1
        #----------------------------------------------------
        while True:
            os.system('cls')
            sx, sy = selec.find_selection()
            team_part = get_team_part(sx,sy, ally)
            
            ViewTable(dt.list_simbols, ally)
            response = q.moving('space','SELECIONAR',team_part['attacks'])
            
            if response != 'space':
                selec.move_selection(sx, sy, response, ally)
            else:
                # determinar todos os espaços de movimento da peça que está selecionada
                # qualquer peça analisa a lista (by) e porcura todos os espaços demarca por ela e salva em uma lista
                # o peão faz o mesmo mas também procura o espaço a sua frente
                sx, sy = selec.find_selection()
                part_selec = dt.table[sx][sy]
                space_attack = comb.get_all_spaces_attack(part_selec, sx,sy)
                
                if part_selec['part'] == dt.pawn:
                    
                    direct = -1 if ally == dt.white else 1
                    if dt.combat[sx + direct][sy][ally]['move']:
                        space_attack.append({'x':sx + direct, 'y':sy, 'team': ally, 'part':dt.pawn})
                        
                        # peões brancos na linha 7 e peões pretos na linha 2 podem andar 2 casas
                        if (ally == dt.white and sx == 7) or (ally == dt.black and sx == 2):
                            if dt.combat[sx + 2*direct][sy][ally]['move']:
                                space_attack.append({'x':sx + 2*direct, 'y':sy, 'team': ally, 'part':dt.pawn})
                        
                
                # setar posição do selection da peça selecionada para 2, ataques para 3, selecione o primeiro dos ataques para 1
                selec.set_selection_combat(space_attack, sx, sy)
                
                while True:
                    
                    sx, sy = selec.find_selection()
                
                    quant_attacks = len(space_attack)
                    os.system('cls')
                    ViewTable(dt.list_simbols, ally)
                    response = q.attacking('enter','JOGAR', quant_attacks)
                    
                    if response == 'back':
                        selec.clear_selection()
                        result = False
                        break
                        # selec.set_selection_combat(space_attack, sx, sy)
                    
                    if response == 'enter':
                        dt.wasCaptured = False
                        result = comb.execute_attack(sx, sy, ally, enemy)
                        
                        if result:
                            dt.list_simbols = []
                            # mostrar rapidamente o ataque
                            os.system('cls')
                            vw.render_view_with_score('', '', ally)
                            time.sleep(2)
                            selec.reset_selection()
                            # verifica se a peça jogada é um peão e se ele chegou na última linha para promover-lo
                            if dt.table[sx][sy]['part'] == dt.pawn and ((ally == dt.white and sx == 1) or (ally == dt.black and sx == 8)):
                                comb.setPromotePawn(sx, sy, ally)
                            break
                    
                    else:
                        selec.move_selection_attack(sx, sy, response, space_attack)
                
                if result:
                    # Jogada realizada com sucesso, mas antes...
                    # VERIFICAR XEQUE-MATE
                    XEQUE_MATE = x.isXeque_Mate(enemy)
                    
                    if XEQUE_MATE:
                        type_end = 'XEQUE-MATE'
                        type_draw = 0
                        dt.list_simbols.append(200)
                        endgame = True
                    
                    # Verificar EMPATES
                    # Afogamento, onde o jogador não tem movimentos legais, mas não está em xeque
                    # Rei contra Rei, onde os dois jogadores só tem o rei e não podem se atacar
                    # Rei vs Rei e Bispo, onde um jogador tem apenas o rei e o outro tem apenas o rei e um bispo, e não é possível dar xeque-mate
                    # Rei vs Rei e Cavalo, onde um jogador tem apenas o rei e o outro tem apenas o rei e um cavalo, e não é possível dar xeque-mate
                    DRAW, type_draw = x.isDraw(enemy)
                    
                    if DRAW:
                        type_end = 'EMPATE'
                        dt.list_simbols.append(150)
                        endgame = True
                    break
        
        if endgame:
            simb.getSimbolsOfPlay()
            simbol_value = simb.getMostImportantSimbol(dt.list_simbols)
            simbol, describe = simb.getSimbol(simbol_value)
            
            reg.setIcon(simbol)
            reg.setMoveToList()
            endGame(ally, type_end, type_draw)
            # print(f"\n\n{type_end}!")
            return
        
        else:
            # verficar se a jogada realizada resultou em um evento específico dentro do jogo que deve ser exibida para o jogador, como por exemplo um xeque
            simb.getSimbolsOfPlay()
            simbol_value = simb.getMostImportantSimbol(dt.list_simbols)
            simbol, describe = simb.getSimbol(simbol_value)
            
            reg.setIcon(simbol)
            reg.setMoveToList()
    
    

def ViewTable(list_simbol, ally, end=False):
    
    simbol_value = simb.getMostImportantSimbol(list_simbol)
    simbol, describe = simb.getSimbol(simbol_value)
    
    points = dt.score_game[ally]
    points_auxiliar = "+" if points >= 0 else ''
    
    if not end and ally == dt.black:
        print(f"| SUA VEZ, (preto) {dt.players[ally]}!")
        print(f"|  ({points_auxiliar}{points})")
    elif not end:
        print("|\n|")
    
    print(35*'-')
        
    vw.render_geral_view(simbol, describe, ally)
    
    print(35*'-')
    
    if not end and ally == dt.white:
        print(f"| SUA VEZ, (branco) '{dt.players[ally]}'!")
        print(f"|  ({points_auxiliar}{points})\n")
    elif not end:
        print("|\n|\n")

def setNamePlayers():
    names = ['Jogador1','Jogador2']
    
    for i in range(2):
        os.system('cls')
        time.sleep(0.5)
        names[i] = input(f'Insira o nome do {i+1}º Jogador:\n')
        
        if len(names[i]) == 0:
            names[i] = 'Jogador'+str(i+1)
            
        elif names[i][0] == ' ':
            names[i] = names[i][1:]
    
    if names[0] == names[1]:
        names = ['Jogador1','Jogador2']
    
    return names

def NextGame():
    answers = ['REVANCHE!','nova partida','SAIR']
    response = q.play_again(answers)
    
    names = [dt.players[dt.white], dt.players[dt.black]]
    
    if response != 2:
        if response == 1:
            names = setNamePlayers()
        resetGame()
        BeginingGame(names)
    else:
        os.system('cls')
        print('Obrigado por jogar!')
        return