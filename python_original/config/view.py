import config.data as dt

def isPreviousSelect(x,y,first):
    if y-1 >= 0:
        if dt.selection[x][y-1] != 0:
            return ''
    
    return first

def render_view_with_score(simbol, describe, team):
    simbol_white = '+' if dt.score_game[dt.white] >= 0 else ''
    simbol_black = '+' if dt.score_game[dt.black] >= 0 else ''
    print(f'({simbol_white}{dt.score_game[dt.white]}) - {dt.players[dt.white]}')
    print(f'({simbol_black}{dt.score_game[dt.black]}) - {dt.players[dt.black]}')
    print()
    
    render_geral_view(simbol, describe, team)

def render_geral_view(simbol, describe, team):
    for x in range(10):
        if x == 0 or x == 9:
            
            # if team == dt.black and x == 9:
            #     print('-'.join(["--" for i in range(10)]),end='')
            #     print(f'|{simbol} {describe}')
                
            # if team == dt.white and x == 0:
            #     print('-'.join(["--" for i in range(10)]),end='')
            #     print(f'|{simbol} {describe}')
            continue
        for y in range(10):
            
            if y == 0 or y == 9:
                continue
            
            printCell(x,y)
            
        if team == dt.black and x == 6:
            print(f' |{simbol} {describe}',end='')
        elif x == 6:
            print(f' |',end='')
            
        if x == 5:
            print(f' |-----',end='')
        if x == 4:
            print(f' |-----',end='')
            
        if team == dt.white and x == 3:
            print(f' |{simbol} {describe}',end='')
        elif x == 3:
            print(f' |',end='')
            
        if x != 9:
            print()

def printCell(x,y):
            cell = dt.table[x][y]
            
            if cell['material'] == 0 or cell['part'] == dt.space or cell['team'] == dt.noteam:
                x_old = x % 2
                y_old = (y+(1-x_old)) % 2
                
                space = dt.space
                selec = dt.selection[x][y]
                first = '\b' + dt.view_slc[selec][0]
                last  = dt.view_slc[selec][1]
                
                first = isPreviousSelect(x,y,first)
                
                if y == 1:
                    first = dt.view_slc[selec][0]
                    
                if (y_old == 1):
                    
                    if selec != 0:
                        print(f' {first}{dt.parts[dt.black][space]}',last,end='')
                    else:
                        print(first,dt.parts[dt.black][space],last,end='')
                else:
                    
                    if selec != 0:
                        print(f' {first}{dt.parts[dt.white][space]}',last,end='')
                    else:
                        print(first,dt.parts[dt.white][space],last,end='')
            
            else:
                selec = dt.selection[x][y]
                first = '\b' + dt.view_slc[selec][0]
                last  = dt.view_slc[selec][1]
                
                first = isPreviousSelect(x,y,first)
                view_part = dt.parts[cell['team']][cell['part']]
                
                if y == 1:
                    first = dt.view_slc[selec][0]
                
                if selec != 0:
                    print(f' {first}{view_part}',last,end='')
                else:
                    print(first,view_part,last,end='')

def view_team_parts():
    for x in dt.team_parts:
        print(x)
        for y in dt.team_parts[x]:
            print(y)
            
def view_by():
    for i, x in enumerate(dt.by):
        for j, y in enumerate(x):
            if(len(y) > 0):
                print("atck(",i,",",j,") => ",y)
        print()
