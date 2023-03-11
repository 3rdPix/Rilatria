from dataclasses import dataclass
from random import randint as rint


class Carta:
    vida: int = 0
    honor: int = 0
    suerte: int = 0
    dinero: int = 0


class Jugador:
    
    def __init__(self) -> None:
        
        self._vida: int = 6
        self._honor: int = 2
        self._suerte: int = 2
        self._dinero:int = 2

    def is_alive(self) -> bool:
        if self.vida < 1: return False
        if self.dinero < 1 and self.suerte < 1: return False
        return True
    
    def won(self) -> bool:
        if self.vida == 10 and self.suerte == 10: return True
        if self.honor == 10 and self.dinero == 10: return True
        return False
    
    def get_vida(self): return self._vida
    def set_vida(self, new_val):
        if new_val < 0: self._vida = 0
        elif new_val > 10: self._vida = 10
        else: self._vida = new_val
    vida = property(get_vida, set_vida)

    def get_honor(self): return self._honor
    def set_honor(self, new_val):
        if new_val < 0: self._honor4 = 0
        elif new_val > 10: self._honor = 10
        else: self._honor = new_val
    honor = property(get_honor, set_honor)

    def get_suerte(self): return self._suerte
    def set_suerte(self, new_val):
        if new_val < 0: self._suerte = 0
        elif new_val > 10: self._suerte = 10
        else: self._suerte = new_val
    suerte = property(get_suerte, set_suerte)

    def get_dinero(self): return self._dinero
    def set_dinero(self, new_val):
        if new_val < 0: self._dinero = 0
        elif new_val > 10: self._dinero = 10
        else: self._dinero = new_val
    dinero = property(get_dinero, set_dinero)

    def efectos_reserva(self) -> None:
        if self.vida > 5: self.dinero -= 1
        if self.honor > 5:
            self.vida += 1
            if self.honor == 10: self.vida += 1
        if self.suerte > 5:
            if rint(1, 2) == 1:
                self.dinero += 1
                if self.suerte == 10: self.vida += 1
            else: self.vida -= 1
        if self.dinero > 5: self.honor -= 1


class Juego:

    def __init__(self) -> None:
        self.jugador = Jugador()
        self.iniciar(self.jugador)

    def stats(self, w: Jugador) -> None:
        print('┌' + '─' * 60 + '┐')
        print(f"│{f'Vida: {w.vida}, Honor: {w.honor}, Suerte: {w.suerte}, Dinero: {w.dinero}': ^60s}│")
        print('└' + '─' * 60 + '┘')

    def iniciar(self, j: Jugador) -> None:
        while j.is_alive():
            self.stats(j)
            carta_1 = self.obtener_carta()
            carta_2 = self.obtener_carta()
            carta_3 = self.obtener_carta()
            self.mostrar_opciones(carta_1, carta_2, carta_3)
            opt = int(input())
            match opt:
                case 1: self.add_stat(carta_1, j)
                case 2: self.add_stat(carta_2, j)
                case 3: self.add_stat(carta_3, j)
            if j.won(): break
            j.efectos_reserva()
            if j.won(): break
        print("Fin del juego")
        self.stats(j)
        exit()
            
    def obtener_carta(self) -> Carta:
        new_carta = Carta()
        element1 = rint(1, 4)
        val1 = rint(-3, 3)
        match element1:
            case 1: new_carta.vida = val1
            case 2: new_carta.honor = val1
            case 3: new_carta.suerte = val1
            case 4: new_carta.dinero = val1
        
        element2 = rint(1, 4)
        while element1 == element2: element2 = rint(1, 4)
        if val1 > 0: val2 = rint(-3, 0)
        elif val1 <= 0: val2 = rint(0, 3)
        match element2:
            case 1: new_carta.vida = val2
            case 2: new_carta.honor = val2
            case 3: new_carta.suerte = val2
            case 4: new_carta.dinero = val2
        return new_carta
    
    def mostrar_opciones(self, c1: Carta, c2: Carta, c3: Carta) -> None:
        print(f'-----------------')
        print(f'CARTAS ALEATORIAS')
        print(f'-----------------\n')
        c1_txt = "│ CARTA 1 \n│ "
        if c1.vida != 0: c1_txt += f"Vida: {c1.vida} "
        if c1.honor != 0: c1_txt += f"Honor: {c1.honor} "
        if c1.suerte != 0: c1_txt += f"Suerte: {c1.suerte} "
        if c1.dinero != 0: c1_txt += f"Dinero: {c1.dinero} "
        c1_txt += "\n"
        print(c1_txt)
        c2_txt = "│ CARTA 2 \n│ "
        if c2.vida != 0: c2_txt += f"Vida: {c2.vida} "
        if c2.honor != 0: c2_txt += f"Honor: {c2.honor} "
        if c2.suerte != 0: c2_txt += f"Suerte: {c2.suerte}  "
        if c2.dinero != 0: c2_txt += f"Dinero: {c2.dinero} "
        c2_txt += "\n"
        print(c2_txt)
        c3_txt = "│ CARTA 3 \n│ "
        if c3.vida != 0: c3_txt += f"Vida: {c3.vida} "
        if c3.honor != 0: c3_txt += f"Honor: {c3.honor} "
        if c3.suerte != 0: c3_txt += f"Suerte: {c3.suerte} "
        if c3.dinero != 0: c3_txt += f"Dinero: {c3.dinero} "
        c3_txt += "\n"
        print(c3_txt)
        print("Elige una opción:")

    def add_stat(self, c: Carta, j: Jugador) -> None:
        j.vida += c.vida
        j.honor += c.honor
        j.suerte += c.suerte
        j.dinero += c.dinero

xd = Juego()