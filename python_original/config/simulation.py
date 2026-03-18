import config.data as dt

def setCombatSimulation():
    dt.combat_simul = [[{dt.white:{'move':False,'attack':False}, dt.black:{'move':False,'attack':False}} for _ in range(10)] for _ in range(10)]
    
    dt.by_simul = [[[] for _ in range(10)] for _ in range(10)]

def setSimulation():
    dt.table_simul = dt.table
    setCombatSimulation()
    
def endSimulation():
    dt.table_simul = [[
    {
        'material': dt.space,
        'team':     dt.noteam,
        'part':     dt.space
    } 
    for _ in range(10)] for _ in range(10)]
    
    setCombatSimulation()