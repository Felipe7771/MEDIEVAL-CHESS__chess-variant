import database as db
# remover peça morta do PART_TEAM
def remove_Deadpiece(team, piece_id:str) -> None:
    if piece_id in db.PART_TEAM[team]:
        del db.PART_TEAM[team][piece_id]

# retorna se aquela peça ainda existe
def has_part(TEAM, ID_PART: str) -> bool:
    return ID_PART in db.PART_TEAM[TEAM]

# 3. Veridicar se o principe vai receber promoção
def check_KingANDQueen() -> None:
# se o REI ou RAINHA estão mortos, se tiver PRINCIPE, transforme ele em um deles
    for TEAM in [db.white, db.black]:
        PRINCE_ID = db.ID_PRINCE[TEAM]
        if (has_part(TEAM, PRINCE_ID)):
            
            KING_ID = db.ID_KING[TEAM]
            QUEEN_ID = db.ID_QUEEN[TEAM]
            
            # Verificar REI
            if (has_part(TEAM, KING_ID)):
                
                DATA_PRINCE = db.PART_TEAM[TEAM][PRINCE_ID]
                DATA_PRINCE['part'] = db.king
                
                remove_Deadpiece(TEAM, PRINCE_ID)
                # adiciona no lugar do principe um novo rei
                db.PART_TEAM[TEAM][KING_ID] = DATA_PRINCE
              
            # Verificar RAINHA  
            elif (has_part(TEAM, QUEEN_ID)):
                DATA_PRINCE = db.PART_TEAM[TEAM][PRINCE_ID]
                DATA_PRINCE['part'] = db.queen
                
                remove_Deadpiece(TEAM, PRINCE_ID)
                # adiciona no lugar do principe um novo rei
                db.PART_TEAM[TEAM][QUEEN_ID] = DATA_PRINCE
    