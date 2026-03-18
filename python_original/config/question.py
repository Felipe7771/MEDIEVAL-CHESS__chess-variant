import sys, time
import keyboard as kb

def enter(emcrement):
    kb.hook(lambda _: None)
    print("___________________________________________________________________________________________")
    print(":: [SPACE] para",emcrement)
    time.sleep(0.15)
    while True:
            event = kb.read_event()
            if event.name == 'space':
                break
            
    kb.unhook_all()

def attacking(key, emcrement, quant_attacks):
    
    can_move = quant_attacks > 1
    kb.hook(lambda _: None)
    
    print(":: [Q ou 0] para VOLTAR    :: [",key.upper(),"] para",emcrement)
    if can_move:
        print(":: [ WASD/↑ ← ↓ → ] para ESCOLHE o alvo")
        
    time.sleep(0.15)
    move = ""
    while True:
            event = kb.read_event()
            if ((event.name == 'up') or (event.name == 'w')) and can_move:
                time.sleep(0.15)
                move = "w"
                break
                    
            elif ((event.name == 'down') or (event.name == 's')) and can_move:
                time.sleep(0.15)
                move = "s"
                break
            
            elif ((event.name == 'right') or (event.name == 'd')) and can_move:
                time.sleep(0.15)
                move = "d"
                break
            
            elif ((event.name == 'left') or (event.name == 'a')) and can_move:
                time.sleep(0.15)
                move = "a"
                break   
            
            elif (event.name == 'q') or (event.name == '0'):
                time.sleep(0.15)
                move = "back"
                break   
            
            elif event.name == key:
                time.sleep(0.15)
                move = key
                break
            
    kb.unhook_all()
    return move

def moving(key, emcrement, quant_attacks):
    can_move = quant_attacks > 0
    kb.hook(lambda _: None)
    print(":: [ WASD/↑ ← ↓ → ] para ESCOLHE a peça")
    
    if can_move:
        print(":: [",key.upper(),"] para",emcrement)
    else:
        print('<--- esta PEÇA não tem movimentos --->')
        
    time.sleep(0.15)
    move = ""
    while True:
            event = kb.read_event()
            if (event.name == 'up') or (event.name == 'w'):
                time.sleep(0.15)
                move = "w"
                break
                    
            elif (event.name == 'down') or (event.name == 's'):
                time.sleep(0.15)
                move = "s"
                break
            
            elif (event.name == 'right') or (event.name == 'd'):
                time.sleep(0.15)
                move = "d"
                break
            
            elif (event.name == 'left') or (event.name == 'a'):
                time.sleep(0.15)
                move = "a"
                break   
            
            elif event.name == key and can_move:
                time.sleep(0.15)
                move = key
                break
            
    kb.unhook_all()
    return move

def question(descrip):
    kb.hook(lambda _: None)
    selected = False
    indice = 0
    print("___________________________________________________________________________________________")
    while not selected:
        
        print(":: ",end="")
        for i, item in enumerate(descrip):
            if i == indice:
                print(" >● [",item.upper(),"]",end=" ")
            else:
                print("  ○",item,end=" ")
        print(":: (A/←) ou (→/D) :: [SPACE] para SELECIONAR")
        time.sleep(0.15)
        while True:
            event = kb.read_event()
            if (event.name == 'left' or event.name == 'a'):
                time.sleep(0.15)
                if indice-1 < 0:
                    indice = len(descrip)-1
                else:
                    indice = indice-1
                break
                    
            elif (event.name == 'right' or event.name == 'd'):
                time.sleep(0.15)
                if indice+1 == len(descrip):
                    indice = 0
                else:
                    indice = indice+1
                break
            
            elif event.name == 'space':
                selected = True
                break
            
        if not selected:
            sys.stdout.write("\033[F")  # Move o cursor para a linha anterior
            sys.stdout.write("\033[K")  # Limpa até o final da linha
    
    kb.unhook_all()
    return indice

def play_again(descrip):
    kb.hook(lambda _: None)
    selected = False
    indice = 0
    print("___________________________________________________________________________________________")
    print("NOVA PARTIDA? ♔ ♕ ♖ ♗ ♘ ♙_____________________________________________________________")
    while not selected:
        
        print(":: ",end="")
        for i, item in enumerate(descrip):
            if i == indice:
                print(" >● [",item.upper(),"]",end=" ")
            else:
                print("  ○",item,end=" ")
        print(":: (A/←) ou (→/D) :: [SPACE] para SELECIONAR")
        time.sleep(0.15)
        while True:
            event = kb.read_event()
            if (event.name == 'left' or event.name == 'a'):
                time.sleep(0.15)
                if indice-1 < 0:
                    indice = len(descrip)-1
                else:
                    indice = indice-1
                break
                    
            elif (event.name == 'right' or event.name == 'd'):
                time.sleep(0.15)
                if indice+1 == len(descrip):
                    indice = 0
                else:
                    indice = indice+1
                break
            
            elif event.name == 'space':
                selected = True
                break
            
        if not selected:
            sys.stdout.write("\033[F")  # Move o cursor para a linha anterior
            sys.stdout.write("\033[K")  # Limpa até o final da linha
    
    kb.unhook_all()
    return indice