import turtle


class Connect4:
    def __init__(self):
        self.tablero = turtle.Turtle()
        self.circulo = turtle.Turtle()
        self.espaciosY = [0] * 8
        self.rojoPos = set()
        self.amarilloPos = set()
        self.coordenadasX = {i: -300 + (i - 1) * 100 for i in range(1, 8)}
        self.coordenadasY = {i: -300 + (i - 1) * 100 for i in range(1, 7)}
        self.jugador_actual = "Red"

    def crear_tablero(self):
        self.tablero.ht()
        self.tablero.width(10)
        self.tablero.speed(0)
        self.tablero.penup()
        self.tablero.goto(-350, 300)
        self.tablero.pendown()

        # Dibujar el contorno
        for _ in range(2):
            self.tablero.forward(700)
            self.tablero.right(90)
            self.tablero.forward(600)
            self.tablero.right(90)

        # Dibujar líneas verticales
        for i in range(6):
            self.tablero.penup()
            self.tablero.goto(-250 + i * 100, 300)
            self.tablero.pendown()
            self.tablero.goto(-250 + i * 100, -300)

        # Dibujar líneas horizontales
        for i in range(5):
            self.tablero.penup()
            self.tablero.goto(-350, 200 - i * 100)
            self.tablero.pendown()
            self.tablero.goto(350, 200 - i * 100)

        # Numerar columnas
        for i in range(7):
            self.tablero.penup()
            self.tablero.goto(-320 + i * 100, 320)
            self.tablero.write(str(i + 1), font=("Arial", 20))

    def colocar_ficha(self, columna):
        if self.espaciosY[columna] >= 6:
            print("Columna llena. Escoge otra.")
            return False

        fila = self.espaciosY[columna] + 1
        self.espaciosY[columna] += 1
        x, y = self.coordenadasX[columna], self.coordenadasY[fila]

        # Guardar posición
        if self.jugador_actual == "Red":
            self.rojoPos.add((columna, fila))
        else:
            self.amarilloPos.add((columna, fila))

        # Dibujar ficha
        self.dibujar_ficha(x, y, self.jugador_actual)

        # Verificar si hay ganador
        if self.verificar_victoria(columna, fila, self.jugador_actual):
            print(f"¡Gana {self.jugador_actual}!")
            turtle.textinput("Mensaje", f"¡Gana {self.jugador_actual}!\nPresiona 'OK' para salir")
            return True

        # Cambiar turno
        self.jugador_actual = "Yellow" if self.jugador_actual == "Red" else "Red"
        return False

    def dibujar_ficha(self, x, y, color):
        self.circulo.color("black")
        self.circulo.width(5)
        self.circulo.speed(500)
        self.circulo.penup()
        #POSICION
        self.circulo.goto(x,y)
        self.circulo.pendown()
        #DIBUJAR Y PINTAR
        self.circulo.begin_fill()
        self.circulo.circle(50)
        self.circulo.color(color)
        self.circulo.end_fill()

    def verificar_victoria(self, col, fila, color):
        posiciones = self.rojoPos if color == "Red" else self.amarilloPos

        def check(dx, dy):
            count = 1
            for d in (-1, 1):
                for i in range(1, 4):
                    if (col + dx * i * d, fila + dy * i * d) in posiciones:
                        count += 1
                    else:
                        break
            return count >= 4

        return any(
            check(dx, dy) for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]
        )

    def get_estado_tablero(self):
        """Devuelve el estado del tablero como una matriz de 6x7."""
        tablero = [[0 for _ in range(7)] for _ in range(6)]
        for (c, f) in self.rojoPos:
            tablero[6 - f][c - 1] = "R"  # Rojo = 1
        for (c, f) in self.amarilloPos:
            tablero[6 - f][c - 1] = "A"  # Amarillo = -1
        return tablero

    def play(self):
        self.crear_tablero()
        while True:
            try:
                columna = int(turtle.numinput(f"Turno {self.jugador_actual}", "Ingrese columna (1-7)", minval=1, maxval=7))
                if self.colocar_ficha(columna):
                    break
            except TypeError:
                print("Juego cancelado.")
                break

    def play_vs_ia(self, vs_ia=False, alpha_beta=False):
        """Permite jugar contra la IA o hacer un enfrentamiento entre dos IA."""
        self.crear_tablero()
        while True:
            if not vs_ia or self.jugador_actual == "Red":
                try:
                    columna = int(turtle.numinput(f"Turno {self.jugador_actual}", "Ingrese columna (1-7)", minval=1, maxval=7))
                except TypeError:
                    print("Juego cancelado.")
                    break
            else:
                columna = self.movimiento_ia(alpha_beta)

            if self.colocar_ficha(columna):
                break

    def movimiento_ia(self, usar_alpha_beta):
        # Se obtiene el estado del tablero
        estado_actual = self.get_estado_tablero()
        
        print(estado_actual)
        print("IA está pensando...")
        return 4
