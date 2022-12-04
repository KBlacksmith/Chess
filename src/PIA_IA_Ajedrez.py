import re
from piezas_ajedrez import *
from math import inf
from time import time


def cuadro_a_num(cuadro: str):
    col = "abcdefgh".find(cuadro[0])
    if col == -1: 
        return -1
    fila = int(cuadro[1])
    if fila < 1 or fila > 8: 
        return -1
    return (fila-1)*8+col

def num_a_cuadro(num: int)->str: 
    if num == -1: 
        return "None"
    columnas = "abcdefgh"
    return columnas[num%8]+str(num//8+1)

def crear_tablero(): 
    tablero = ["." for i in range(64)]
    #PIEZAS BLANCAS
    tablero[0] = Rook(True, 0)
    tablero[0].simbolo = "L"
    tablero[1] = Knight(True, 1)
    tablero[2] = Bishop(True, 2)
    tablero[3] = Queen(True, 3)
    tablero[4] = King(True, 4)
    tablero[5] = Bishop(True, 5)
    tablero[6] = Knight(True, 6)
    tablero[7] = Rook(True, 7)
    for i in range(8, 16): 
        tablero[i] = Pawn(True, i)
    #PIEZAS NEGRAS
    for i in range(48, 56): 
        tablero[i] = Pawn(False, i)
    tablero[56] = Rook(False, 56)
    tablero[57] = Knight(False, 57)
    tablero[58] = Bishop(False, 58)
    tablero[59] = Queen(False, 59)
    tablero[60] = King(False, 60)
    tablero[61] = Bishop(False, 61)
    tablero[62] = Knight(False, 62)
    tablero[63] = Rook(False, 63)
    return tablero

def validar_sn(): 
    sn = input().strip().lower()
    while sn != "s" and sn != "n": 
        sn = input("Ingrese únicamente \"s\" o \"n\": ").strip().lower()
    return sn == "s"

def movimientos_validos(tablero, pieza: Pieza, blancas: list, negras: list, explicito = False)->list: 
    if pieza.posicion < 0 or pieza.posicion > 63: 
        return []
    temp_movimientos = pieza.movimientos_validos(tablero)
    movimientos = temp_movimientos.copy()
    for mov in temp_movimientos: 
        if jaque(tablero, pieza.color, blancas, negras) and isinstance(pieza, King) and abs(pieza.posicion-mov) == 2: 
            movimientos.remove(mov)
            continue
        #Revisamos cada movimiento y lo eliminamos de la lista si genera un estado de jaque
        temp = tablero[mov]
        pos_original = pieza.posicion
        movida = pieza.movida
        pieza.mover(tablero, mov)
        if jaque(tablero, pieza.color, blancas, negras):
            movimientos.remove(mov)
        
        pieza.deshacer_movimiento(tablero, pos_original)
        tablero[mov] = temp
        if isinstance(tablero[mov], Pieza): 
            tablero[mov].posicion = mov
        pieza.movida = movida
    if explicito: 
        print(str(pieza)+"["+num_a_cuadro(pieza.posicion)+"]: "+str(movimientos))
    return movimientos

def num_movimientos(tablero, turno: bool, blancas: list, negras: list, explicito = False)->int: 
    if turno == BLANCO: 
        piezas = blancas
    else: 
        piezas = negras
    num_movs = 0
    for pieza in piezas: 
        #Aumentamos la cuenta de movimientos legales disponibles
        num_movs += len(movimientos_validos(tablero, pieza, blancas, negras, explicito))
    return num_movs

def validar_movimiento(mov: str): 
    if len(mov) != 4: 
        return False
    if re.fullmatch("[a-h][1-8][a-h][1-8]", mov) is None: 
        return False
    mov_inicial = cuadro_a_num(mov[:2])
    #print(mov_inicial)
    if mov_inicial == -1: 
        return False
    mov_final = cuadro_a_num(mov[2:])
    #print(mov_final)
    if mov_final == -1: 
        return False
    return True

def evaluacion_material(turno: bool, blancas: list, negras: list)->int: 
    valor = 0
    if turno == BLANCO: 
        for pieza in blancas: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor += pieza.valor
        for pieza in negras: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor -= pieza.valor
    else: 
        for pieza in negras: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor += pieza.valor
        for pieza in blancas: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor -= pieza.valor
    #Para calcular el valor material, sumamos o restamos el valor de cada pieza según su color
    
    return valor

def evaluacion_mobilidad(tablero: list, turno: bool, blancas: list, negras: list)->int: 
    return num_movimientos(tablero, turno, blancas, negras) - num_movimientos(tablero, not turno, blancas, negras)

def evaluacion_heuristica(tablero: list, turno: bool, blancas: list, negras: list): 
    #Evaluación de las piezas en el tablero
    valor_piezas = evaluacion_material(turno, blancas, negras)*3

    #Evaluación de los movimientos disponibles
    valor_mobilidad = evaluacion_mobilidad(tablero, turno, blancas, negras)
 
    return valor_piezas+valor_mobilidad
    #return -1*(valor_piezas+valor_mobilidad)

def evaluacion_experimental(tablero: list, turno: bool, blancas: list, negras: list)->int: 
    valores = {
        "p": 100, #PEON
        "n": 320, #CABALLO
        "b": 330, #ALFIL
        "r": 500, #TORRE
        "q": 900, #REINA
        "k": 20000 #REY 
    }
    valor = 0
    if turno == BLANCO: 
        for pieza in blancas: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor += valores[pieza.simbolo.lower()]
        for pieza in negras: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor -= valores[pieza.simbolo.lower()]
    else: 
        for pieza in negras: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor += valores[pieza.simbolo.lower()]
        for pieza in blancas: 
            if pieza.posicion >= 0 and pieza.posicion <= 63: 
                valor -= valores[pieza.simbolo.lower()]

def recibir_ayuda()->bool: 
    ayuda = input("Jugará como Blanco o Negro? B/N: ").strip().lower()
    while ayuda != "b" and ayuda != "n": 
        ayuda = input("B/N: ").strip().lower()
    return ayuda == "b"

def minimax_alfa_beta(tablero: list, turno: bool, jugador: bool, blancas: list, negras: list, profundidad: int, Max = True, alfa = -inf, beta = inf)->dict: 
    #Obtenemos la cantidad de movimientos que el jugador en turno puede realizar
    n = num_movimientos(tablero, turno, blancas, negras)
    #Determinamos como estado final un caso en que se llega a profundidad de 4 o que el jugador ya no tiene movimientos que realizar
    if profundidad == 0 or n == 0:
        if n == 0: 
            #Si el jugador no tiene movimientos, pero tampoco se encuentra en jaque es una situación de empate
            if not jaque(tablero, turno, blancas, negras): 
                return {"origen": -1, "mov": -1, "valor": 0}
            #Si se encuentra en jaque, regresamos -infinito porque es un caso donde pierde
            if turno == jugador: 
                return {"origen": -1, "mov": -1, "valor": -inf}
            #Si el oponente se encuentra en jaque y no tiene movimientos, es jaque mate y victoria para el jugador
            else: 
                return {"origen": -1, "mov": -1, "valor": inf}
        #Realizamos la evaluación del tablero
        valor = evaluacion_heuristica(tablero, jugador, blancas, negras)
        #if turno == jugador: 
        return {"origen": -1, "mov": -1, "valor": valor}
        #Si se evalúa desde la perspectiva del oponente, necesitamos corregir el valor del tablero para obtener un valor mínimo
        #return {"origen": -1, "mov": -1, "valor": -valor}
    
    
    #print(piezas)
    if turno == BLANCO: 
        piezas = blancas
    else: 
        piezas = negras

    if Max: 
        mejor_movimiento = {"origen": -1, "mov": -1, "valor": -inf}
        valor = -inf
        for pieza in piezas:
            #print(type(pieza))
            if isinstance(pieza, Pieza): 
                movimientos = movimientos_validos(tablero, pieza, blancas, negras)
                for mov in movimientos: 
                    temp = tablero[mov]
                    pos_original = pieza.posicion
                    movida = pieza.movida
                    pieza.mover(tablero, mov)
                    promovida = False
                    if isinstance(pieza, Pawn): 
                        promovida = pieza.puede_promover()    
                        if promovida: 
                            tablero[pieza.posicion] = Queen(pieza.color, pieza.posicion)
                    valor = max(valor, minimax_alfa_beta(tablero, not turno, jugador, blancas, negras, profundidad-1, not Max, alfa, beta)["valor"])
                    alfa = max(alfa, valor)
                    if promovida: 
                        tablero[pieza.posicion] = pieza
                    #pieza.mover(tablero, pos_original)
                    pieza.deshacer_movimiento(tablero, pos_original)
                    tablero[mov] = temp
                    if isinstance(tablero[mov], Pieza): 
                        tablero[mov].posicion = mov
                    pieza.movida = movida
                    if mejor_movimiento["valor"] != valor: 
                        mejor_movimiento["origen"] = pos_original
                        mejor_movimiento["valor"] = valor
                        mejor_movimiento["mov"] = mov
                    if beta < alfa: 
                        break
    else: 
        mejor_movimiento = {"origen": -1, "mov": -1, "valor": inf}
        valor = inf
        for pieza in piezas:
            #print(type(pieza))
            if isinstance(pieza, Pieza): 
                movimientos = movimientos_validos(tablero, pieza, blancas, negras)

                for mov in movimientos: 
                    temp = tablero[mov]
                    pos_original = pieza.posicion
                    movida = pieza.movida
                    pieza.mover(tablero, mov)
                    promovida = False
                    if isinstance(pieza, Pawn): 
                        promovida = pieza.puede_promover()    
                        if promovida: 
                            tablero[pieza.posicion] = Queen(pieza.color, pieza.posicion)
                    valor = min(valor, minimax_alfa_beta(tablero, not turno, jugador, blancas, negras, profundidad-1, not Max, alfa, beta)["valor"])
                    beta = min(beta, valor)
                    if promovida: 
                        tablero[pieza.posicion] = pieza
                    pieza.deshacer_movimiento(tablero, pos_original)
                    tablero[mov] = temp
                    if isinstance(tablero[mov], Pieza): 
                        tablero[mov].posicion = mov
                    pieza.movida = movida
                    if mejor_movimiento["valor"] != valor: 
                        mejor_movimiento["origen"] = pos_original
                        mejor_movimiento["valor"] = valor
                        mejor_movimiento["mov"] = mov
                    if beta < alfa: 
                        break
    return mejor_movimiento

def minimax(tablero: list, turno: bool, jugador: bool, blancas: list, negras: list, profundidad: int, Max = True)->dict: 
    #Obtenemos la cantidad de movimientos que el jugador en turno puede realizar
    n = num_movimientos(tablero, turno, blancas, negras)
    #Determinamos como estado final un caso en que se llega a profundidad de 4 o que el jugador ya no tiene movimientos que realizar
    if profundidad == 0 or n == 0:
        if n == 0: 
            #Si el jugador no tiene movimientos, pero tampoco se encuentra en jaque es una situación de empate
            if not jaque(tablero, turno, blancas, negras): 
                return {"origen": -1, "mov": -1, "valor": 0}
            #Si se encuentra en jaque, regresamos -infinito porque es un caso donde pierde
            if turno == jugador: 
                return {"origen": -1, "mov": -1, "valor": -inf}
            #Si el oponente se encuentra en jaque y no tiene movimientos, es jaque mate y victoria para el jugador
            else: 
                return {"origen": -1, "mov": -1, "valor": inf}
        #Realizamos la evaluación del tablero
        valor = evaluacion_heuristica(tablero, jugador, blancas, negras)
        #if turno == jugador: 
        return {"origen": -1, "mov": -1, "valor": valor}
        #Si se evalúa desde la perspectiva del oponente, necesitamos corregir el valor del tablero para obtener un valor mínimo
        #return {"origen": -1, "mov": -1, "valor": -valor}
    
    
    #print(piezas)
    if turno == BLANCO: 
        piezas = blancas
    else: 
        piezas = negras

    if Max: 
        mejor_movimiento = {"origen": -1, "mov": -1, "valor": -inf}
        valor = -inf
        for pieza in piezas:
            #print(type(pieza))
            if isinstance(pieza, Pieza): 
                movimientos = movimientos_validos(tablero, pieza, blancas, negras)
                for mov in movimientos: 
                    temp = tablero[mov]
                    pos_original = pieza.posicion
                    movida = pieza.movida
                    pieza.mover(tablero, mov)
                    promovida = False
                    if isinstance(pieza, Pawn): 
                        promovida = pieza.puede_promover()    
                        if promovida: 
                            tablero[pieza.posicion] = Queen(pieza.color, pieza.posicion)
                    valor = max(valor, minimax(tablero, not turno, jugador, blancas, negras, profundidad-1, False)["valor"])
                    if promovida: 
                        tablero[pieza.posicion] = pieza
                    #pieza.mover(tablero, pos_original)
                    pieza.deshacer_movimiento(tablero, pos_original)
                    tablero[mov] = temp
                    if isinstance(tablero[mov], Pieza): 
                        tablero[mov].posicion = mov
                    pieza.movida = movida
                    if mejor_movimiento["valor"] != valor: 
                        mejor_movimiento["origen"] = pos_original
                        mejor_movimiento["valor"] = valor
                        mejor_movimiento["mov"] = mov
    else: 
        mejor_movimiento = {"origen": -1, "mov": -1, "valor": inf}
        valor = inf
        for pieza in piezas:
            #print(type(pieza))
            if isinstance(pieza, Pieza): 
                movimientos = movimientos_validos(tablero, pieza, blancas, negras)

                for mov in movimientos: 
                    temp = tablero[mov]
                    pos_original = pieza.posicion
                    movida = pieza.movida
                    pieza.mover(tablero, mov)
                    promovida = False
                    if isinstance(pieza, Pawn): 
                        promovida = pieza.puede_promover()    
                        if promovida: 
                            tablero[pieza.posicion] = Queen(pieza.color, pieza.posicion)
                    valor = min(valor, minimax(tablero, not turno, jugador, blancas, negras, profundidad-1, True)["valor"])
                    if promovida: 
                        tablero[pieza.posicion] = pieza
                    pieza.deshacer_movimiento(tablero, pos_original)
                    tablero[mov] = temp
                    if isinstance(tablero[mov], Pieza): 
                        tablero[mov].posicion = mov
                    pieza.movida = movida
                    if mejor_movimiento["valor"] != valor: 
                        mejor_movimiento["origen"] = pos_original
                        mejor_movimiento["valor"] = valor
                        mejor_movimiento["mov"] = mov
    return mejor_movimiento
#
# MAIN LOOP
#

if __name__=="__main__":
    tablero = crear_tablero()

    p_blancas = []
    p_negras = []

    for p in tablero: 
        if isinstance(p, Pieza): 
            if p.color == BLANCO: 
                p_blancas.append(p)
            else: 
                p_negras.append(p)

    turno = True
    n = num_movimientos(tablero, turno, p_blancas, p_negras)
    ayuda = recibir_ayuda()
    maxProf = int(input("Profundidad de búsqueda: "))
    ronda = 1
    while n > 0:
        imprimir_tablero(tablero, turno)
        if turno == BLANCO:
            print("Blanco ("+str(ronda)+")")

        else:
            print("Negro ("+str(ronda)+")")
        #print("Valor actual: "+str(evaluacion_heuristica(tablero, turno)))
        print("Movimientos posibles: "+str(n))

        #print("Movimientos posibles: "+str(n))
        #MINIMAX
        if turno == ayuda: 
            print("MINIMAX")
            print("Calculando mejor movimiento...")
            t_inicial = time()
            mejor = minimax_alfa_beta(tablero, turno, ayuda, p_blancas, p_negras, maxProf)
            #mejor = minimax(tablero, turno, ayuda, p_blancas, p_negras, maxProf)
            t_final = time()
            print("MEJOR VALOR: "+str(mejor["valor"]))
            print("Mejor movimiento: "+num_a_cuadro(mejor["origen"])+num_a_cuadro(mejor["mov"]))
            print("Tiempo de ejecución: "+str(t_final-t_inicial))   
        
        #INICIA TURNO
        continuar = True
        while continuar: 
            movimiento = input("Ingrese su movimiento: ").strip().lower()
            while not validar_movimiento(movimiento):
                movimiento = input("Movimiento inválido: ").strip().lower()
            pos_actual = cuadro_a_num(movimiento[:2])
            pos_final = cuadro_a_num(movimiento[2:])
            #if pos_actual in piezas: 
            if isinstance(tablero[pos_actual], Pieza) and tablero[pos_actual].color == turno: 
                movimientos = movimientos_validos(tablero, tablero[pos_actual], p_blancas, p_negras)
                if pos_final in movimientos: 
                    continuar = False
                else: 
                    print("Movimiento inválido")
            else: 
                print(str(num_a_cuadro(pos_actual))+" no es una de sus piezas")
        pieza = tablero[pos_actual]
        if isinstance(pieza, Pieza):
            pieza.mover(tablero, pos_final)
            if isinstance(pieza, Pawn) and pieza.puede_promover(): 
                tablero[pieza.posicion] = pieza.promover()
                del pieza
            
        #FIN TURNO
        p_blancas.clear()
        p_negras.clear()
        for p in tablero: 
            if isinstance(p, Pieza):
                if p.color == BLANCO: 
                    p_blancas.append(p)
                else: 
                    p_negras.append(p)
        turno = not turno
        print("-"*20)
        if turno == BLANCO:
            ronda += 1
        n = num_movimientos(tablero, turno, p_blancas, p_negras)
    imprimir_tablero(tablero, turno)
    if jaque(tablero, turno, p_blancas, p_negras): 
        if turno == BLANCO: 
            print("GANA NEGRO")
        else: 
            print("GANA BLANCO")
    else: 
        print("EMPATE")
