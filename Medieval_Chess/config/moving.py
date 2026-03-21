import database as db

# atualizar peça movida no PART_TEAM
def update_partMoved_PartTeam(id, team, newy, newx):
    piece = db.PART_TEAM[team][id]
    piece['coo'] = (newy, newx)
        
# movimentar peça no TABLE
def move_part(team, part, oldy, oldx, newy, newx):
    # deletar peça no espaço antigo
    db.TABLE[oldy][oldx] = {
        'material': db.space,
        'team':     db.noteam,
        'part':     db.space
    }
    
    # adicionar em novo espaço
    db.TABLE[newy][newx] = {
        'material': db.MATERIAL[part],
        'team':     team,
        'part':     part
    }