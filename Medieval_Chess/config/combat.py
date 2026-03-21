import database as db
import selection as select
import attacks as attck

# lista de times geral
TEAMS = [db.white, db.black]

# remover peça morta do PART_TEAM
def remove_Deadpiece(team, piece_id):
    if piece_id in db.PART_TEAM[team]:
        del db.PART_TEAM[team][piece_id]
        
# 1. verificar peças vivas (PART_TEAM vs TABLE)
# 2. limpar/filtrar peças mortas
# 3. limpar COMBAT
# 4. para cada peça:
#   - calcular ataques
#   - salvar no COMBAT
#   - atualizar attacks/moves no PART_TEAM

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
    
# 3. limpar COMBAT        
def set_empty_COMBAT():
    EMPTY = [[
    {
        db.white:{},
        db.black:{}
    } for _ in range(10)] for _ in range(10)]
    
    db.COMBAT = EMPTY
    db.MOVE  = EMPTY

# 4. para cada peça:
#   - calcular ataques
#   - salvar no COMBAT
#   - atualizar attacks/moves no PART_TEAM
def set_COMBAT():
    
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
    
    # limpar a tabela COMBAT
    set_empty_COMBAT()
    
    for TEAM in TEAMS:
        for ID_PART, PACKET_PART in db.PART_TEAM[TEAM].items():
            #   - calcular ataques
            set_ATTACK_places_COMBAT(ID_PART, PACKET_PART, TEAM)
            
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
