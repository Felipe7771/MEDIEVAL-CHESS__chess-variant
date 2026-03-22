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

# reorganiza opções de seleção a qual prioriza casas próximas á direção requirida em relação a casa pré-selecionada (i, j)
def get_coos_sorted_by_direction(COOS, i, j, direction):
    
    if direction == db.UP:
        # main = lambda t: t[0] < j
        
        cond_Priority = lambda t: abs(t[0] - j)
        cond_Tiebreaker = lambda t: abs(t[1] - i)
        not_main = lambda t: t[0] >= j

    elif direction == db.DOWN:
        # main = lambda t: t[0] > j
        
        cond_Priority = lambda t: abs(t[0] - j)
        cond_Tiebreaker = lambda t: abs(t[1] - i)
        not_main = lambda t: t[0] <= j

    elif direction == db.LEFT:
        # main = lambda t: t[1] < i
        
        cond_Priority = lambda t: abs(t[1] - i)
        cond_Tiebreaker = lambda t: abs(t[0] - j)
        not_main = lambda t: t[1] >= i

    elif direction == db.RIGHT:
        # main = lambda t: t[1] > i
        
        cond_Priority = lambda t: abs(t[1] - i)
        cond_Tiebreaker = lambda t: abs(t[0] - j)
        not_main = lambda t: t[1] <= i

    return sorted(
        COOS,
        key=lambda t: (
            not_main(t), # penaliza quem não está na direção
            cond_Priority(t) *2, # eixo principal (peso maior)
            cond_Tiebreaker(t) # desempate
        )
    )