import re
from piezas_ajedrez import *
from math import inf
from time import time
#valores = {
#    "pawn": 1,
#    "knight": 3, 
#    "bishop": 3,  
#    "rook": 5, 
#    "queen": 9, 
#    "king": 9999
#}

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
    tablero[0] = Rook(True, 0)
    tablero[1] = Knight(True, 1)
    tablero[2] = Bishop(True, 2)
    tablero[3] = Queen(True, 3)
    tablero[4] = King(True, 4)
    tablero[5] = Bishop(True, 5)
    tablero[6] = Knight(True, 6)
    tablero[7] = Rook(True, 7)
    for i in range(8, 16): 
        tablero[i] = Pawn(True, i)
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
    #tablero[40] = Pawn(True, 40)
    #tablero[27] = King(True, 27)
    #tablero[35] = Rook(False, 35)
    #tablero[17] = Bishop(True, 17)
    #tablero[19] = Pawn(False, 19)
    return tablero

def validar_sn(): 
    sn = input().strip().lower()
    while sn != "s" and sn != "n": 
        sn = input("Ingrese únicamente \"s\" o \"n\": ").strip().lower()
    return sn == "s"

def num_movimientos(tablero, turno: bool)->int: 
    piezas = []
    for p in tablero: 
        if isinstance(p, Pieza) and p.color == turno: 
            piezas.append(p)
    num_movs = 0
    for p in piezas:
        #pieza = tablero[p]
        if isinstance(p, Pieza): 
            temp_movimientos = p.movimientos_validos(tablero)
            movimientos = temp_movimientos.copy()
            
            for mov in temp_movimientos: 
                pos_inicial = p.posicion
                temp = tablero[mov]
                tablero[mov] = tablero[p.posicion]
                tablero[p.posicion] = "."
                tablero[mov].posicion = mov
                #temp = tablero[pos_final]
                #tablero[pos_final] = tablero[pos_inicial]
                #tablero[pos_inicial] = "."
                #tablero[pos_final].posicion = pos_final
                if jaque(tablero, p.color):
                    movimientos.remove(mov)
                tablero[pos_inicial] = tablero[mov]
                tablero[mov] = temp
                tablero[pos_inicial].posicion = pos_inicial
                #tablero[pos_inicial] = tablero[pos_final]
                #tablero[pos_final] = temp
                #tablero[pos_inicial].posicion = pos_inicial
            
            num_movs += len(movimientos)
            #if len(movimientos) > 0: 
            #    m = []
            #    for mov in movimientos: 
            #        m.append(num_a_cuadro(mov))
            #    print(str(p)+"["+str(num_a_cuadro(p.posicion))+"]: "+str(m))
    return num_movs

def validar_movimiento(mov: str): 
    if len(mov) != 4: 
        return False
    if re.fullmatch("[a-z][0-9][a-z][0-9]", mov) is None: 
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

def evaluacion_material(tablero: list)->int: 
    pesos = {
        "P": 1, 
        "N": 3, 
        "B": 3, 
        "R": 5, 
        "Q": 9,
        "K": 9999
    }

    valor = 0

    for p in tablero: 
        if isinstance(p, Pieza): 
            if p.color == BLANCO: 
                valor += pesos[p.simbolo.upper()]
            else: 
                valor -= pesos[p.simbolo.upper()]
    return valor*2

def evaluacion_mobilidad(tablero: list)->int: 
    valor = 0
    valor += num_movimientos(tablero, BLANCO)
    valor -= num_movimientos(tablero, NEGRO)
    #valor += num_movimientos(tabler)
    return valor

def evaluacion_heuristica(tablero: list, turno: bool): 
    valor_piezas = evaluacion_material(tablero)
    #print("Valor piezas: "+str(valor_piezas))
    valor_mobilidad = evaluacion_mobilidad(tablero)
    #print("Valor mobilidad: "+str(valor_mobilidad))
    if turno == BLANCO: 
        return valor_piezas+valor_mobilidad
    return -1*(valor_piezas+valor_mobilidad)

def recibir_ayuda()->bool: 
    wb = input("Jugará como Blanco o Negro? B/N: ").strip().lower()
    while wb != "b" and wb != "n": 
        wb = input("B/N: ").strip().lower()
    return wb == "b"

def minimax(tablero: list, turno: bool, jugador: bool, depth = 0, Max = True, alfa = -inf, beta = inf)->dict: 
    #if jaque(tablero, turno)
    depth += 1

    if depth == 4 or num_movimientos(tablero, turno) == 0:
        valor = evaluacion_heuristica(tablero, turno)
        if turno == jugador: 
            return {"origen": -1, "mov": -1, "valor": valor}
        return {"origen": -1, "mov": -1, "valor": -valor}
    
    blancas = []
    negras = []

    for p in tablero: 
        if isinstance(p, Pieza): 
            if p.color == BLANCO: 
                blancas.append(p.posicion)
            else: 
                negras.append(p.posicion)

    piezas = None
    if turno == BLANCO: 
        piezas = blancas
    else: 
        piezas = negras

    #print(piezas)

    if Max: 
        mejor_movimiento = {"origen": 0, "mov": -1, "valor": -inf}
        valor = -inf
        for p in piezas:
            pieza = tablero[p]
            #print(type(pieza))
            if isinstance(pieza, Pieza): 
                temp_movimientos = pieza.movimientos_validos(tablero)
                movimientos = temp_movimientos.copy()

                for mov in temp_movimientos: 
                    pos_inicial = pieza.posicion
                    temp = tablero[mov]
                    tablero[mov] = tablero[pieza.posicion]
                    tablero[pieza.posicion] = "."
                    tablero[mov].posicion = mov
                    if jaque(tablero, pieza.color):
                        movimientos.remove(mov)
                    tablero[pos_inicial] = tablero[mov]
                    tablero[mov] = temp
                    tablero[pos_inicial].posicion = pos_inicial
                #print(movimientos)
                for mov in movimientos: 
                    temp = tablero[mov]
                    pos_original = pieza.posicion
                    movida = pieza.movida
                    pieza.mover(tablero, mov)
                    valor = max(valor, minimax(tablero, not turno, jugador, depth, not Max, alfa, beta)["valor"])
                    alfa = max(alfa, valor)
                    pieza.mover(tablero, pos_original)
                    tablero[mov] = temp
                    pieza.movida = movida
                    if mejor_movimiento["valor"] != valor: 
                        mejor_movimiento["origen"] = pos_original
                        mejor_movimiento["valor"] = valor
                        mejor_movimiento["mov"] = mov
                    if beta <= alfa: 
                        break
    else: 
        mejor_movimiento = {"origen": 0, "mov": 0, "valor": inf}
        valor = inf
        for p in piezas:
            pieza = tablero[p]
            #print(type(pieza))
            if isinstance(pieza, Pieza): 
                temp_movimientos = pieza.movimientos_validos(tablero)
                movimientos = temp_movimientos.copy()

                for mov in temp_movimientos: 
                    pos_inicial = pieza.posicion
                    temp = tablero[mov]
                    tablero[mov] = tablero[pieza.posicion]
                    tablero[pieza.posicion] = "."
                    tablero[mov].posicion = mov
                    if jaque(tablero, pieza.color):
                        movimientos.remove(mov)
                    tablero[pos_inicial] = tablero[mov]
                    tablero[mov] = temp
                    tablero[pos_inicial].posicion = pos_inicial
                #print(movimientos)
                for mov in movimientos: 
                    temp = tablero[mov]
                    pos_original = pieza.posicion
                    movida = pieza.movida
                    pieza.mover(tablero, mov)
                    valor = min(valor, minimax(tablero, not turno, jugador, depth, not Max, alfa, beta)["valor"])
                    beta = min(beta, valor)
                    pieza.mover(tablero, pos_original)
                    tablero[mov] = temp
                    pieza.movida = movida
                    if mejor_movimiento["valor"] != valor: 
                        mejor_movimiento["origen"] = pos_original
                        mejor_movimiento["valor"] = valor
                        mejor_movimiento["mov"] = mov
                    if beta <= alfa: 
                        break
    return mejor_movimiento

#
# MAIN LOOP
#

if __name__=="__main__":
    jugar = True    
    tablero = crear_tablero()

    p_blancas = []
    p_negras = []

    piezas = p_blancas

    for p in tablero: 
        if isinstance(p, Pieza): 
            if p.color == BLANCO: 
                p_blancas.append(p.posicion)
            else: 
                p_negras.append(p.posicion)

    imprimir_tablero(tablero)
    turno = True
    n = num_movimientos(tablero, turno)
    ayuda = recibir_ayuda()

    while n > 0:
        if turno == BLANCO:
            print("Turno W")
        else:
            print("Turno B")

        #MINIMAX
        if turno == ayuda: 
            print("Valor actual: "+str(evaluacion_heuristica(tablero, turno)))
            print("Calculando mejor movimiento...")
            t_inicial = time()
            mejor = minimax(tablero, turno, ayuda)
            t_final = time()
            print("Mejor movimiento: "+num_a_cuadro(mejor["origen"])+num_a_cuadro(mejor["mov"]))
            print("Tiempo: "+str(t_final-t_inicial))
        
        #INICIA TURNO
        continuar = True
        #print(piezas)
        #for p in piezas: 
        #    print(p)
        #    movs = tablero[p].movimientos_validos(tablero)
        #    movimientos = []
        #    for m in movs: 
        #        movimientos.append(num_a_cuadro(m))
        #    if len(movimientos) > 0: 
        #        print(str(tablero[p])+"["+num_a_cuadro(p)+"]: "+str(movimientos))
        while continuar: 
            movimiento = input("Ingrese su movimiento: ").strip().lower()
            while not validar_movimiento(movimiento):
                movimiento = input("Movimiento inválido: ").strip().lower()
            pos_actual = cuadro_a_num(movimiento[:2])
            pos_final = cuadro_a_num(movimiento[2:])

            if pos_actual in piezas: 
                temp_movimientos = tablero[pos_actual].movimientos_validos(tablero)
                movimientos = temp_movimientos.copy()

                if len(movimientos) > 0:
                    for mov in temp_movimientos: 
                        temp = tablero[mov]
                        movida = tablero[pos_actual].movida
                        tablero[pos_actual].mover(tablero, mov)
                        if jaque(tablero, tablero[mov].color):
                            movimientos.remove(mov)
                        tablero[mov].mover(tablero, pos_actual)
                        tablero[mov] = temp
                        tablero[pos_actual].movida = movida
                if pos_final in movimientos: 
                    continuar = False
                else: 
                    print("Movimiento inválido")
        pieza = tablero[pos_actual]
        if isinstance(pieza, Pieza):
            pieza.mover(tablero, pos_final)
            imprimir_tablero(tablero)
        #FIN TURNO
        p_blancas.clear()
        p_negras.clear()
        for p in tablero: 
            if isinstance(p, Pieza):
                if p.color == BLANCO: 
                    p_blancas.append(p.posicion)
                else: 
                    p_negras.append(p.posicion)
        turno = not turno
        if turno == BLANCO: 
            piezas = p_blancas
        else: 
            piezas = p_negras
        input("Fin de turno")
        n = num_movimientos(tablero, turno)
