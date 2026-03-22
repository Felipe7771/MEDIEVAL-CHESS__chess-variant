import database as db
import selection as select
import attacks as attck
import generation as genera
import moving as mov

# lista de times geral
TEAMS = [db.white, db.black]

# remover peça morta do PART_TEAM
def remove_Deadpiece(team, piece_id):
    if piece_id in db.PART_TEAM[team]:
        del db.PART_TEAM[team][piece_id]

# ==================================================
# Standard analysis for setting up attacked squares       
# ==================================================       
# 1. verificar peças vivas (PART_TEAM vs TABLE)
# 2. limpar/filtrar peças mortas
# 3. Veridicar se o principe vai receber promoção
# 4. limpar COMBAT
# 5. para cada peça:
#   - calcular ataques
#   - salvar no COMBAT
#   - atualizar attacks/moves no PART_TEAM
#---------------------------------------------------

# 1. verificar peças vivas (PART_TEAM vs TABLE)
# 2. limpar/filtrar peças mortas
def check_alive_Table_PartTeam():
    
    for TEAM in TEAMS:
        DEAD_PARTS = []
        for ID_PART, PART in db.PART_TEAM[TEAM].items():
            
            y, x = PART['coo']
            
            # se não estiver coincidindo o TABLE com os dados do PART_TEAM, considere a peça morta
            if (PART['part'] != db.TABLE[y][x]['part']):
                DEAD_PARTS.append(ID_PART)
        
        # eliminar peças mortas do PART_TEAM
        for ID_PART in DEAD_PARTS:
            remove_Deadpiece(TEAM,ID_PART)
    

# 3. Veridicar se o principe vai receber promoção
def check_KingANDQueen():
# se o REI ou RAINHA estão mortos, se tiver PRINCIPE, transforme ele em um deles
    for TEAM in TEAMS:
        PRINCE_ID = db.ID_PRINCE[TEAM]
        if (select.has_part(TEAM, PRINCE_ID)):
            
            KING_ID = db.ID_KING[TEAM]
            QUEEN_ID = db.ID_QUEEN[TEAM]
            
            # Verificar REI
            if (select.has_part(TEAM, KING_ID)):
                
                DATA_PRINCE = db.PART_TEAM[TEAM][PRINCE_ID]
                DATA_PRINCE['part'] = db.king
                
                remove_Deadpiece(TEAM, PRINCE_ID)
                # adiciona no lugar do principe um novo rei
                db.PART_TEAM[TEAM][KING_ID] = DATA_PRINCE
              
            # Verificar RAINHA  
            elif (select.has_part(TEAM, QUEEN_ID)):
                DATA_PRINCE = db.PART_TEAM[TEAM][PRINCE_ID]
                DATA_PRINCE['part'] = db.queen
                
                remove_Deadpiece(TEAM, PRINCE_ID)
                # adiciona no lugar do principe um novo rei
                db.PART_TEAM[TEAM][QUEEN_ID] = DATA_PRINCE
    
# 4. limpar COMBAT        
def set_empty_COMBAT():
    EMPTY = [[
    {
        db.white:{},
        db.black:{}
    } for _ in range(10)] for _ in range(10)]
    
    db.COMBAT = EMPTY
    db.MOVE  = EMPTY
    
# 5. para cada peça:
#   - calcular ataques
#   - salvar no COMBAT
#   - atualizar attacks/moves no PART_TEAM
def set_COMBAT(JESTER):
    
    # Limpar movimentos possíveis e xeques, serão recalculados
    db.QUANT_MOVES = {
        db.white: 0,
        db.black: 0
    }
    
    db.XEQUE = {
        db.white: False,
        db.black: False
    }
    
    # filtrar peças vivas no tabuleiro
    check_alive_Table_PartTeam()
    
    # verificar se o principe deve se transformar
    check_KingANDQueen()
    
    # limpar a tabela COMBAT
    set_empty_COMBAT()
    
    for TEAM in TEAMS:
        for ID_PART, PACKET_PART in db.PART_TEAM[TEAM].items():
            #   - calcular ataques
            set_ATTACK_places_COMBAT(ID_PART, PACKET_PART, TEAM, JESTER)


# ==================================================
# Set calculation of attacked squares      
# ================================================== 
      
def set_ATTACK_places_COMBAT(ID_PART, PACKET_PART, TEAM, Jester_secondMove=False):
    
    PART = PACKET_PART['part']
    COO = PACKET_PART['coo']
    MOVES = db.PART_MOVES_UNIT[PART]
    
    # Peças com um movimento de única casa
    # (Cavalo, Rei)
    if (PART in (db.knight, db.king)):
        attck.set_OneStep_ATTACK(ID_PART, COO, PART, TEAM, MOVES)
    
    # Peças com um movimento de única casa ESPECIAL
    # (Peão)
    elif (PART in (db.pawn,)):
        attck.set_Pawn_ATTACK(ID_PART, COO, PART, TEAM, MOVES)
    
    # Movimento de Jester
    elif (PART in (db.jester,)):
        attck.set_Jester_ATTACK(ID_PART, COO, PART, TEAM, MOVES, SECOND_MOVE=Jester_secondMove)
        
    # Movimento de Principe
    elif (PART in (db.prince,)):
        attck.set_OneStep_ATTACK(ID_PART, COO, PART, TEAM, MOVES[0])
        attck.set_RayCast_ATTACK(ID_PART, COO, PART, TEAM, MOVES[1],QUANT_MOVES=2)
        
    # Demais peças que andam livremente nas suas direções
    else:
        attck.set_RayCast_ATTACK(ID_PART, COO, PART, TEAM, MOVES,QUANT_MOVES=8)
     
        
# ==================================================
# Practice a bid execution      
# ================================================== 
    
def try_movePart(COO_BASE, COO_MOVE, ID_PART, TEAM, JESTER=False):
    # Normalmente você vai querer que o COO_BASE seja as coodenadas da peça selecionada:
    # db.SELECTED_PART_COO
    
    # salvar status do jogo
    genera.Replay('before_move')
    
    # executar o movimento da peça selecionada
    mov.execute_Move(COO_BASE, COO_MOVE, TEAM)
    
    if (not JESTER):
        if (check_illegal_moviment(TEAM)):
            # retornar estado anterior
            return invalid_move()
        
        else:
            # tudo certo, limpar replay e a seleção
            return valid_move()
        
    else:
        # analise primeiro se o primeiro movimento é válido, já adiconando os possíveis movimentos do segundo lance
        if (check_illegal_moviment(TEAM, JESTER)):
            # retornar estado anterior
            return invalid_move()
            
        else:
            # verificar se os movimentos possíveis do segundo lançe são legais
            COOS_SECOND_MOVE = select.get_Listcoo_MovePart(ID_PART, TEAM)
            
            # se pelo menos tiver UM lançe legal, o segundo movimento pode ser feito
            for COO in COOS_SECOND_MOVE:
                # salvar status do novo tabuleiro
                genera.Replay('before_second_move')
                
                mov.execute_Move(COO_MOVE, COO, TEAM)
                
                if (not check_illegal_moviment(TEAM, JESTER)):
                    
                    # retornar estado anterior do lance, existe um movimento legal
                    genera.return_state_dataReplay('before_second_move')
                    return valid_move()
                    
                else:
                    # tente novamente
                    genera.return_state_dataReplay('before_second_move')
                
            # se nenhum for válido, então é ilegal
            return invalid_move()
    
def check_illegal_moviment(TEAM, JESTER=False):
    
    set_COMBAT(JESTER)
    return db.XEQUE[TEAM]

def invalid_move():
    genera.return_state_dataReplay('before_move')
            
    # retorne que o movimento não pode ser realizado por ser inválido
    return False

def valid_move():
    # tudo certo, limpar replay e a seleção
    db.SELECTED_PART_COO = None
    
    genera.empty_allReplay()
    select.empty_selection()
    
    # retorne que o movimento foi realizado com sucesso
    return True
