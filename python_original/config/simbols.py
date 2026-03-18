import config.data as dt
import config.game as g
import config.xeque as x
import config.combat as comb
# SIMBOLOS DE JOGO

def getMostImportantSimbol(list):
    return max(list, default=0)

# retorna simbolo e descrição
def getSimbol(value_simbol):
    if (value_simbol not in list(dt.simbols.keys())): 
        return "", ""
    
    icon = dt.simbols[value_simbol]
    
    return icon, dt.simbols_name[icon]

# retorna todos os simbolos da jogada realizada
def getSimbolsOfPlay():
    oldy, oldx = dt.part_play['oldy'], dt.part_play['oldx']
    newy, newx = dt.part_play['newy'], dt.part_play['newx']
    team = dt.part_play['team']
    enemy = g.rtn_enemy(team)
    part_move = dt.part_play['part']
    
    enemyKing = x.getKing(enemy)
    
    #* (!!) Xeque Duplo
    #? Ataque duplo ao Rei inimigo
    # verifique a contagem de ataques realizadas ao rei inimigo
    if enemyKing is not None and x.countAttacksAtKing(enemyKing, enemy) >= 2:
        
        dt.list_simbols.append(120)
        return
    
    
    #* (#) Xeque
    #? Ataque ao Rei inimigo 
    # verifique se o movimento colocou o rei inimigo em xeque
    if dt.xeque[enemy]:
        
        dt.list_simbols.append(110)
        return
        
        
    #* (囗) Cercamento 
    #? Todos os movimentos do Rei inimigo estão sendo atacados 
    # verifique se o rei inimigo estão sendo atacadas OU ocupadas por peças do jogador
    if x.MovesKingAreAttacking(enemyKing, enemy, team):
        
        dt.list_simbols.append(100)
        return
       
        
    attacked_parts = comb.get_PartsAttackedBy(part_move, newx, newy,team)
         
    #* (!) Garfo 
    #? Peça capaz de ameaçar multiplas peças inimigas
    # verificar se a quantidade de peças atacadas aumentaram para 2 ou mais após o movimento da peça jogada
    # peões em garfo não são muito importantes
    garfos = [p for p in attacked_parts if p['team'] == enemy and p['material'] >= dt.pawn]
    if (len(garfos) >= 2):
        
        dt.list_simbols.append(90)
        return
        

    #* (*) Ataque Descoberto 
    #? Movimento de Peça revela demais peças ameaçarem peças inimigas
    # verificar se alguma das peças aliadas (sem ser a peça movida) aumentou o numero de ataques a peças inimigas após o movimento da peça jogada
    hist_tp = dt.history['team_parts'][team]
    now_tp = dt.team_parts[team]
    
    for i in range(len(now_tp)):
        
        for j in range(len(hist_tp)):
            
            if ((now_tp[i]['part'] == hist_tp[j]['part']) and 
                (now_tp[i]['x'] == hist_tp[j]['x']) and 
                (now_tp[i]['y'] == hist_tp[j]['y'])):
                
                # print(f"Peça: {dt.names[now_tp[i]['part']]} em ({now_tp[i]['x']}, {now_tp[i]['y']}) - Ataques antes: {hist_tp[j]['fight']} - Ataques agora: {now_tp[i]['fight']}")
                # time.sleep(1.55)
                if now_tp[i]['fight'] > hist_tp[j]['fight']:
                    
                    dt.list_simbols.append(80)
                    return
    
       
    #* (X) Ameaça 
    #? Peça ameaçando uma peça inimigo de pontos de material maior
    # Pegue todas as peças inimigas que estão sendo atacadas pela peça jogada e verifique se alguma delas tem um valor de material maior do que a peça jogada
    # Ou quando está ameçando uma peça inimiga no centro do tabuleiro (d4, d5, e4, e5)
    for attacked in attacked_parts:
        if (dt.material[attacked['part']] > dt.material[part_move]):
            dt.list_simbols.append(70)
            return
        
    
    #* (+) Captura 
    #? Peça inimiga abatida/ ganho de material
    # verifique se houve um ganho de material para o jogador após a jogada
    if (len(dt.score_historical) > 1 and (dt.score_historical[-1][team] > dt.score_historical[-2][team])) or (dt.wasCaptured and len(dt.score_historical) == 1 and dt.score_historical[-1][team] > 0):
        
        dt.list_simbols.append(60)
        return
        
        
    #* (=) Troca 
    #? Troca de peças que anulam o ganho de material entre os jogadores
    # verifique se a largura da lista score_historical é maior que 1 (ou seja, houve pelo menos uma troca de peças) e se os pontos de material dos jogadores permaneceram os mesmos após a jogada
    if dt.wasCaptured and len(dt.score_historical) > 1 and dt.score_historical[-1][team] == dt.score_historical[-2][team]:
        
        dt.list_simbols.append(50)
        return
        
        
    #* (-) Sacrifício 
    #? Movimento de peça ao ataque do inimigo
    # verifique se o movimento da peça a colocou em um espaço atacado por uma peça inimiga
    if dt.combat[newx][newy][enemy]['attack']:
        
        dt.list_simbols.append(40)
        return
        
        
    #* (Δ) Domínio 
    #? Peças movidas ao centro do tabuleiro
    # verifique se a peça se moveu para o centro do tabuleiro (d4, d5, e4, e5)
    if part_move == dt.pawn and newx in [4, 5] and newy in [4, 5]:
        
        dt.list_simbols.append(30)
        return
        
        
    #* (>) Avanço 
    #? Peão avança para o campo inimigo
    # verifique se um peão avançou para o campo inimigo
    if part_move == dt.pawn and (newx not in (1,8)):
        
        dt.list_simbols.append(20)
        return
        
           
    #* (<<) Fuga 
    #? Movimento de peça em saída do ataque do inimigo
    # verifique no histórico se a peça jogada estava sendo atacada no turno anterior e se ela saiu do ataque no turno atual
    if dt.history['combat'][oldx][oldy][enemy]['attack'] and not dt.combat[newx][newy][enemy]['attack']:
        
        dt.list_simbols.append(10)
        return
    
    #* (O) Movimento
    #? Movimento sem características especiais
    dt.list_simbols.append(1)
    return
    
    
# todo || Ordem de importância
#! (!?) Xeque-Mate 
#? Fim do Jogo 
#
#! (½) Empate
#? Afogamento, Rei vs Rei, Rei vs (Rei, Bispo), Rei vs (Rei, Cavalo): Ninguém ganha
#