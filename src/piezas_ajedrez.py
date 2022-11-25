BLANCO = True
NEGRO = False

def imprimir_tablero(tablero: list): 
    for i in range(7, -1, -1): 
        linea = str(i+1) + " "
        for j in range(8): 
            #if tablero[i*8+j] == ".": 
            #    if i%2 == 0: 
            #        if j %2 == 0: 
            #            linea += " "
            #        else: 
            #            linea += "#"
            #    else: 
            #        if j %2 == 0: 
            #            linea += "#"
            #        else: 
            #            linea += " "
            #    pass
            #else: 
            linea += str(tablero[i*8+j]) + " "
        print(linea)
    print("  A B C D E F G H \n")

def jaque(tablero: list, turno: bool): #, pos_inicial: int, pos_final: int
    #temp = tablero[pos_final]
    #tablero[pos_final] = tablero[pos_inicial]
    #tablero[pos_inicial] = "."
    #tablero[pos_final].posicion = pos_final

    p_blancas = []
    p_negras = []
    for p in tablero: 
        if isinstance(p, Pieza): 
            if p.color == BLANCO: 
                p_blancas.append(p.posicion)
            else: 
                p_negras.append(p.posicion)
    piezas = None
    enemigo = None
    if turno == BLANCO:
        piezas = p_blancas
        enemigo = p_negras 
    else: 
        piezas = p_negras
        enemigo = p_blancas
    rey = None
    for p in piezas:
        if isinstance(tablero[p], King): 
            rey = p
            break
    #print("REY: "+str(rey))
    check = False
    for p in enemigo: 
        mov = tablero[p].movimientos_validos(tablero)
        if rey in mov: 
            check = True
            break
    
    #tablero[pos_inicial] = tablero[pos_final]
    #tablero[pos_final] = temp
    #tablero[pos_inicial].posicion = pos_inicial
    return check

class Pieza: 
    def __init__(self, color: bool, posicion: int) -> None:
        self.simbolo = "#"
        #W -> Verdadero, N -> Falso
        self.color = color
        self.valor = 0
        self.posicion = posicion
        self.movida = False
    def __str__(self) -> str:
        return self.simbolo
    def movimientos_validos(self, tablero)->list: 
        return []
    def mover(self, tablero, mov: int)->None: 
        #print("test1")
        #if jaque(tablero, self.color, self.posicion, mov): 
            #print("test2")
        #    return False
        tablero[mov] = self
        tablero[self.posicion] = "."
        self.posicion = mov
        self.movida = True
        #return True

class Pawn(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 1
        if self.color: 
            self.simbolo = "P"
        else: 
            self.simbolo = "p"
        self.en_passant = False
    def movimientos_validos(self, tablero)->list: 
        movimientos = []
        diff = 8
        diag_izq = 7
        diag_der = 9
        if self.color == NEGRO: 
            diff *= -1
            diag_izq *= -1
            diag_der *= -1

        if self.posicion + diff >= 0 and self.posicion + diff <= 63: 
            if tablero[self.posicion+diff] == ".": 
                movimientos.append(self.posicion+diff)
                if self.posicion + 2*diff >= 0 and self.posicion+2*diff <= 63 and not self.movida: 
                    if tablero[self.posicion+2*diff] == ".": 
                        movimientos.append(self.posicion+2*diff)
                        self.en_passant = True
        #COMER
        if self.posicion + diag_izq >= 0 and self.posicion + diag_izq <= 63 and (
            (self.posicion+diag_izq)//8 == self.posicion//8 + 1 or (self.posicion+diag_izq)//8 == self.posicion//8 - 1
        ) and ((self.posicion+diag_izq)%8 == self.posicion%8-1 or (self.posicion+diag_izq)%8 == self.posicion%8+1): 
            if isinstance(tablero[self.posicion + diag_izq], Pieza) and tablero[self.posicion+diag_izq].color != self.color: 
                movimientos.append(self.posicion+diag_izq)
        if self.posicion + diag_der >= 0 and self.posicion + diag_der <= 63 and (
            (self.posicion+diag_der)//8 == self.posicion//8+1 or (self.posicion+diag_der)//8 == self.posicion//8-1
        ) and ((self.posicion+diag_der)%8 == self.posicion%8-1 or (self.posicion+diag_der)%8 == self.posicion%8+1): 
            if isinstance(tablero[self.posicion+diag_der], Pieza) and tablero[self.posicion+diag_der].color != self.color: 
                movimientos.append(self.posicion+diag_der)
        #EN PASSANT

        return movimientos

class Rook(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 5
        if self.color: 
            self.simbolo = "R"
        else: 
            self.simbolo = "r"
    def movimientos_validos(self, tablero: list)->list: 
        movimientos = []
        #Abajo
        pos = self.posicion
        while pos-8 >= 0: 
            pos -=8
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color:
                movimientos.append(pos)
                break
            else: 
                break
        #Arriba
        pos = self.posicion
        while pos + 8 <= 63: 
            pos += 8
            if tablero[pos] == ".":
                movimientos.append(pos)
            elif tablero[pos].color != self.color:
                movimientos.append(pos)
                break
            else: 
                break
        #Derecha
        pos = self.posicion
        while (pos + 1) // 8 == self.posicion // 8 and pos+1<=63:
            pos += 1
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Izquierda
        pos = self.posicion
        while (pos - 1) // 8 == self.posicion // 8 and pos-1 >=0: 
            pos -= 1
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break

        return movimientos
class Knight(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 3
        if self.color: 
            self.simbolo = "N"
        else: 
            self.simbolo = "n"
    def movimientos_validos(self, tablero)->list: 
        movimientos = []

        if self.posicion - 17 >= 0 and (self.posicion-17)//8 == self.posicion//8-2 and (self.posicion-17)%8 == self.posicion%8 - 1: 
            if tablero[self.posicion - 17] == "." or tablero[self.posicion - 17].color != self.color: 
                movimientos.append(self.posicion-17)

        if self.posicion - 15>=0 and (self.posicion-15)//8 == self.posicion//8-2 and (self.posicion-15)%8 == self.posicion%8 + 1: 
            if tablero[self.posicion - 15] == "." or tablero[self.posicion - 15].color != self.color: 
                movimientos.append(self.posicion-15)

        if self.posicion -10 >=0 and (self.posicion-10)//8 == self.posicion//8-1 and (self.posicion-10)%8 == self.posicion%8-2:
            if tablero[self.posicion - 10] == "." or tablero[self.posicion - 10].color != self.color: 
                movimientos.append(self.posicion-10)

        if self.posicion - 6 >= 0 and (self.posicion-6)//8 == self.posicion//8-1 and (self.posicion-6)%8 == self.posicion%8+2:
            if tablero[self.posicion - 6] == "." or tablero[self.posicion - 6].color != self.color: 
                movimientos.append(self.posicion-6)

        if self.posicion + 6 <= 63 and (self.posicion+6)//8 == self.posicion//8+1 and (self.posicion+6)%8 == self.posicion%8-2:
            if tablero[self.posicion +6] == "." or tablero[self.posicion +6].color != self.color: 
                movimientos.append(self.posicion+6)

        if self.posicion + 10 <= 63 and (self.posicion + 10) // 8 == self.posicion//8+1 and (self.posicion+10)%8 == self.posicion % 8 +2:
            if tablero[self.posicion +10] == "." or tablero[self.posicion +10].color != self.color: 
                movimientos.append(self.posicion+10)

        if self.posicion + 15 <= 63 and (self.posicion+15)//8 == self.posicion//8+2 and (self.posicion+15)%8 == self.posicion % 8 -1:
            if tablero[self.posicion +15] == "." or tablero[self.posicion +15].color != self.color:
                movimientos.append(self.posicion+15)

        if self.posicion + 17 <= 63 and (self.posicion + 17) //8 == self.posicion//8 + 2 and (self.posicion+17) % 8 == self.posicion % 8 +1: 
            if tablero[self.posicion +17] == "." or tablero[self.posicion +17].color != self.color: 
                movimientos.append(self.posicion+17)

        return movimientos

class Bishop(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 3
        if self.color: 
            self.simbolo = "B"
        else: 
            self.simbolo = "b"
    def movimientos_validos(self, tablero)->list: 
        movimientos = []
        #Izquierda-Abajo
        pos = self.posicion
        while pos-9 >= 0 and (pos-9)//8 == pos//8-1 and (pos-9)%8 == pos%8-1:
            pos -= 9
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Derecha-Abajo
        pos = self.posicion
        while pos-7 >= 0 and (pos-7)//8 == pos//8-1 and (pos-7)%8 == pos%8+1:
            pos -= 7
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Izquierda Arriba
        pos = self.posicion
        while pos+7 <= 63 and (pos+7)//8 == pos//8+1 and (pos+7)%8 == pos%8-1:
            pos += 7
            if tablero[pos] == ".":
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Derecha Arriba
        pos = self.posicion
        while pos+9 <= 63 and (pos+9)//8 == pos//8+1 and (pos+9)%8 == pos%8+1:
            pos += 9
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break            

        return movimientos

class Queen(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 9
        if self.color: 
            self.simbolo = "Q"
        else: 
            self.simbolo = "q"
    def movimientos_validos(self, tablero)->list: 
        movimientos = []

        #Abajo
        pos = self.posicion
        while pos-8 >= 0: 
            pos -=8
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color:
                movimientos.append(pos)
                break
            else: 
                break
        #Arriba
        pos = self.posicion
        while pos + 8 <= 63: 
            pos += 8
            if tablero[pos] == ".":
                movimientos.append(pos)
            elif tablero[pos].color != self.color:
                movimientos.append(pos)
                break
            else: 
                break
        #Derecha
        pos = self.posicion
        while (pos + 1) // 8 == self.posicion // 8 and pos+1<=63:
            pos += 1
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Izquierda
        pos = self.posicion
        while (pos - 1) // 8 == self.posicion // 8 and pos-1 >=0: 
            pos -= 1
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break

        #Izquierda-Abajo
        pos = self.posicion
        while pos-9 >= 0 and (pos-9)//8 == pos//8-1 and (pos-9)%8 == pos%8-1:
            pos -= 9
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Derecha-Abajo
        pos = self.posicion
        while pos-7 >= 0 and (pos-7)//8 == pos//8-1 and (pos-7)%8 == pos%8+1:
            pos -= 7
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Izquierda Arriba
        pos = self.posicion
        while pos+7 <= 63 and (pos+7)//8 == pos//8+1 and (pos+7)%8 == pos%8-1:
            pos += 7
            if tablero[pos] == ".":
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break
        #Derecha Arriba
        pos = self.posicion
        while pos+9 <= 63 and (pos+9)//8 == pos//8+1 and (pos+9)%8 == pos%8+1:
            pos += 9
            if tablero[pos] == ".": 
                movimientos.append(pos)
            elif tablero[pos].color != self.color: 
                movimientos.append(pos)
                break
            else: 
                break 
        
        return movimientos

class King(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 9999
        if self.color: 
            self.simbolo = "K"
        else: 
            self.simbolo = "k"
    def movimientos_validos(self, tablero)->list: 
        movimientos = []
        #IZQ-ABAJO
        if (self.posicion-9)//8 == self.posicion//8 - 1 and (self.posicion-9)%8 == self.posicion%8 -1 and self.posicion-9 >= 0: 
            if tablero[self.posicion-9] == "." or tablero[self.posicion-9].color != self.color: 
                movimientos.append(self.posicion-9)
        #ABAJO
        if (self.posicion-8)//8 == self.posicion//8 - 1 and (self.posicion-8)%8 == self.posicion%8 and self.posicion-8 >= 0: 
            if tablero[self.posicion-8] == "." or tablero[self.posicion-8].color != self.color: 
                movimientos.append(self.posicion-8)
        #DER-ABAJO
        if (self.posicion-7)//8 == self.posicion//8 - 1 and (self.posicion-7)%8 == self.posicion%8 + 1 and self.posicion-7 >= 0: 
            if tablero[self.posicion-7] == "." or tablero[self.posicion-7].color != self.color: 
                movimientos.append(self.posicion-7)
        #IZQUIERDA
        if (self.posicion-1)//8 == self.posicion//8 and (self.posicion-1)%8 == self.posicion%8 - 1 and self.posicion-1>=0: 
            if tablero[self.posicion-1] == "." or tablero[self.posicion-1].color != self.color: 
                movimientos.append(self.posicion-1)
        #DERECHA
        if (self.posicion+1)//8 == self.posicion//8 and (self.posicion+1)%8 == self.posicion%8 +1 and self.posicion+1<=63: 
            if tablero[self.posicion+1] == "." or tablero[self.posicion+1].color != self.color: 
                movimientos.append(self.posicion+1)
        #IZQ-ARRIBA
        if (self.posicion+7)//8 == self.posicion//8 + 1 and (self.posicion+7)%8 == self.posicion%8-1 and self.posicion+7<=63: 
            if tablero[self.posicion+7] == "." or tablero[self.posicion+7].color != self.color: 
                movimientos.append(self.posicion+7)
        #ARRIBA
        if (self.posicion+8)//8 == self.posicion//8+1 and (self.posicion+8)%8 == self.posicion%8 and self.posicion+8 <=63: 
            if tablero[self.posicion+8] == "." or tablero[self.posicion+8].color != self.color: 
                movimientos.append(self.posicion+8)
        #DER-ARRIBA
        if (self.posicion+9)//8 == self.posicion//8+1 and (self.posicion+9)//8 == self.posicion % 8 + 1 and self.posicion+9 <= 63: 
            if tablero[self.posicion+9] == "." or tablero[self.posicion+9].color != self.color: 
                movimientos.append(self.posicion+9)

        return movimientos