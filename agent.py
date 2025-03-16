import math
import random

class Agent:
    def __init__(self, player_id, alpha_beta=False, depth=4):
        self.id = str(player_id)  # Almacenar como string
        self.opponent_id = '2' if self.id == '1' else '1'  # ID del oponente como string
        self.alpha_beta = alpha_beta
        self.depth = depth

    def evaluar_tablero(self, tablero):
        """Evalúa el tablero considerando agrupaciones y posición."""
        score = 0
        # Preferencia por la columna central
        center_column = [fila[3] for fila in tablero]
        score += center_column.count(self.id) * 2
        score -= center_column.count(self.opponent_id) * 2

        # Evaluar líneas horizontales, verticales y diagonales
        for row in range(6):
            for col in range(7):
                if tablero[row][col] == self.id:
                    score += self.evaluar_posicion(tablero, row, col, self.id)
                elif tablero[row][col] == self.opponent_id:
                    score -= self.evaluar_posicion(tablero, row, col, self.opponent_id)

        return score

    def evaluar_posicion(self, tablero, row, col, player):
        """Evalúa potenciales líneas de 4 desde una posición."""
        value = 0
        direcciones = [(0, 1), (1, 0), (1, 1), (-1, 1)]  # Horizontal, Vertical, Diagonales
        for dx, dy in direcciones:
            count = 1
            vacios = 0
            for d in (1, -1):
                paso = 1
                while True:
                    x = col + dx * d * paso
                    y = row + dy * d * paso
                    if 0 <= x < 7 and 0 <= y < 6:
                        if tablero[y][x] == player:
                            count += 1
                        elif tablero[y][x] == '0' or tablero[y][x] == 0:
                            vacios += 1
                            break
                        else:
                            break
                        paso += 1
                    else:
                        break
            if count >= 4:
                value += 100
            elif count == 3 and vacios >= 1:
                value += 5
            elif count == 2 and vacios >= 2:
                value += 2
        return value

    def minimax(self, tablero, profundidad, alpha, beta, maximizando):
        if profundidad == 0 or self.juego_terminado(tablero):
            return self.evaluar_tablero(tablero), None

        mejor_columna = None
        movimientos_validos = [c for c in range(7) if self.movimiento_valido(tablero, c)]
        if not movimientos_validos:
            return 0, None

        if maximizando:
            max_eval = -math.inf
            for columna in movimientos_validos:
                nuevo_tablero = self.simular_movimiento(tablero, columna, self.id)
                evaluacion, _ = self.minimax(nuevo_tablero, profundidad-1, alpha, beta, False)
                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_columna = columna
                if self.alpha_beta:
                    alpha = max(alpha, evaluacion)
                    if beta <= alpha:
                        break
            return max_eval, mejor_columna
        else:
            min_eval = math.inf
            for columna in movimientos_validos:
                nuevo_tablero = self.simular_movimiento(tablero, columna, self.opponent_id)
                evaluacion, _ = self.minimax(nuevo_tablero, profundidad-1, alpha, beta, True)
                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_columna = columna
                if self.alpha_beta:
                    beta = min(beta, evaluacion)
                    if beta <= alpha:
                        break
            return min_eval, mejor_columna

    def elegir_movimiento(self, tablero):
        _, movimiento = self.minimax(tablero, self.depth, -math.inf, math.inf, True)
        if movimiento is None:
            movimientos_validos = [c for c in range(7) if self.movimiento_valido(tablero, c)]
            return random.choice(movimientos_validos) if movimientos_validos else None
        
        
        # Se le suma uno a la columna porque en nuestro connect4.py se manejan por la columna literal
        movimiento = movimiento + 1
        return movimiento

    def movimiento_valido(self, tablero, columna):
        return tablero[0][columna] in (0, '0')

    def simular_movimiento(self, tablero, columna, player_id):
        nuevo_tablero = [list(fila) for fila in tablero]
        for fila in range(5, -1, -1):
            if nuevo_tablero[fila][columna] in (0, '0'):
                nuevo_tablero[fila][columna] = player_id
                break
        return nuevo_tablero

    def juego_terminado(self, tablero):
        for row in range(6):
            for col in range(7):
                if tablero[row][col] not in (0, '0') and self.check_victoria(tablero, row, col):
                    return True
        return False

    def check_victoria(self, tablero, row, col):
        player = tablero[row][col]
        direcciones = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dx, dy in direcciones:
            count = 1
            for d in (1, -1):
                paso = 1
                while True:
                    x = col + dx * d * paso
                    y = row + dy * d * paso
                    if 0 <= x < 7 and 0 <= y < 6 and tablero[y][x] == player:
                        count += 1
                        paso += 1
                    else:
                        break
            if count >= 4:
                return True
        return False