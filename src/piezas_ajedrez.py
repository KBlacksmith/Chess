BLANCO = True
NEGRO = False

def imprimir_tablero(tablero: list, turno: bool): 
    if turno == BLANCO: 
        for i in range(7, -1, -1): 
            linea = str(i+1) + " "
            for j in range(8):
                linea += str(tablero[i*8+j]) + " "
            print(linea)
        print("  A B C D E F G H \n")
    else: 
        for i in range(8): 
            linea = str(i+1)+" "
            for j in range(7, -1, -1): 
                linea += str(tablero[i*8+j])+" "
            print(linea)
        print("  H G F E D C B A \n")

def jaque(tablero: list, turno: bool, blancas: list, negras: list): 

    if turno == BLANCO:
        piezas = blancas
        enemigo = negras 
    else: 
        piezas = negras
        enemigo = blancas
    rey = None
    for pieza in piezas:
        if isinstance(pieza, King): 
            rey = pieza.posicion
            break
    check = False
    for pieza in enemigo: 
        mov = pieza.movimientos_validos(tablero)
        if rey in mov: 
            check = True
            break

    return check

class Pieza: 
    def __init__(self, color: bool, posicion: int) -> None:
        self.simbolo = "#"
        self.color = color
        self.valor = 0
        self.posicion = posicion
        self.movida = False
    def __str__(self) -> str:
        return self.simbolo
    def movimientos_validos(self, tablero)->list: 
        return []
    def mover(self, tablero, mov: int)->None:
        if isinstance(tablero[mov], Pieza): 
            tablero[mov].posicion = -1
        tablero[mov] = self
        tablero[self.posicion] = "."
        self.posicion = mov
        self.movida = True
    def deshacer_movimiento(self, tablero, mov: int)->None: 
        self.mover(tablero, mov)

class Pawn(Pieza): 
    def __init__(self, color: bool, posicion: int) -> None:
        super().__init__(color, posicion)
        self.valor = 1
        if self.color: 
            self.simbolo = "P"
        else: 
            self.simbolo = "p"
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
    def puede_promover(self):
        if self.color == BLANCO: 
            if self.posicion//8 == 7: 
                return True
        else: 
            if self.posicion//8 == 0: 
                return True
        return False
    def promover(self, queen = False)->str: 
        if queen: 
            return "Q"
        print("Promoción")
        promocion = input("R/N/B/Q: ").strip().upper()
        while promocion not in "RNBQ": 
            promocion = input("R/N/B/Q: ").strip().upper()
        if promocion == "R": 
            return Rook(self.color, self.posicion)
        elif promocion == "N": 
            return Knight(self.color, self.posicion)
        elif promocion == "B": 
            return Bishop(self.color, self.posicion)
        return Queen(self.color, self.posicion)

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
        if (self.posicion+9)//8 == self.posicion//8+1 and (self.posicion+9)%8 == self.posicion % 8 + 1 and self.posicion+9 <= 63: 
            if tablero[self.posicion+9] == "." or tablero[self.posicion+9].color != self.color: 
                movimientos.append(self.posicion+9)

        #ENROQUE
        if not self.movida: 
            #KINGSIDE
            rook = tablero[self.posicion+3]
            if tablero[self.posicion+1] == "." and tablero[self.posicion+2] == "." and isinstance(rook, Rook): 
                if rook.color == self.color and not rook.movida: 
                    movimientos.append(self.posicion+2)
            #QUEENSIDE
            rook = tablero[self.posicion-4]
            if tablero[self.posicion-1] == "." and tablero[self.posicion-2] == "." and tablero[self.posicion-3] == "." and isinstance(rook, Rook): 
                if rook.color == self.color and not rook.movida: 
                    movimientos.append(self.posicion-2)

        #ENROQUE
        #if not self.movida:# and not jaque(tablero, self.color): 
        #    if tablero[self.posicion+1] == "." and tablero[self.posicion+2] == "." and isinstance(tablero[self.posicion+3], Rook) and not tablero[self.posicion+3].movida: 
        #        movimientos.append(self.posicion+2)
        #    if tablero[self.posicion-1] == "." and tablero[self.posicion-2] == "."  and tablero[self.posicion-3] == "." and isinstance(tablero[self.posicion-4], Rook) and not tablero[self.posicion-4].movida: 
        #        movimientos.append(self.posicion-2)
        return movimientos
    def mover(self, tablero, mov: int) -> None:
        #ENROQUE
        if abs(self.posicion-mov) == 2: 
            if mov-self.posicion > 0: 
                #KINGSIDE
                rook = tablero[self.posicion+3]
                if isinstance(rook, Rook): 
                    rook.mover(tablero, self.posicion+1)
            else: 
                #QUEENSIDE
                rook = tablero[self.posicion-4]
                if isinstance(rook, Rook): 
                    rook.mover(tablero, self.posicion-1)
        if isinstance(tablero[mov], Pieza): 
            tablero[mov].posicion = -1
        tablero[mov] = self
        tablero[self.posicion] = "."
        self.posicion = mov
        self.movida = True
    def deshacer_movimiento(self, tablero, mov: int) -> None:
        if abs(self.posicion-mov) == 2: 
            
            if self.posicion%8 == 6: 
                #KINGSIDE
                rook = tablero[self.posicion-1]
                if isinstance(rook, Rook):
                    rook.deshacer_movimiento(tablero, self.posicion+1)
            else: 
                #QUEENSIDE
                rook = tablero[self.posicion+1]
                if isinstance(rook, Rook): 
                    rook.deshacer_movimiento(tablero, self.posicion-2)
            rook.movida = False
        tablero[mov] = self
        tablero[self.posicion] = "."
        self.posicion = mov
        self.movida = True