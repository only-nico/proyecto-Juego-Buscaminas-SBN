import pygame
import random
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

class Subject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

class Buscaminas(Subject):
    def __init__(self, filas, columnas, minas):
        super().__init__()
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.tablero = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.minas_tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
        self.juego_terminado = False
    #colocar minas aleatorias en el tablero
    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if self.minas_tablero[fila][columna] != -1:
                self.minas_tablero[fila][columna] = -1
                minas_colocadas += 1
    #contador de minas en un area circundante
    def contar_minas_alrededor(self, fila, columna):
        if self.minas_tablero[fila][columna] == -1:
            return -1
        contador = 0
        for i in range(max(0, fila - 1), min(self.filas, fila + 2)):
            for j in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                if self.minas_tablero[i][j] == -1:
                    contador += 1
        return contador

    def inicializar_tablero(self):
        self.colocar_minas()

        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.minas_tablero[fila][columna] != -1:
                    self.minas_tablero[fila][columna] = self.contar_minas_alrededor(fila, columna)
    #muestra el tablero
    def mostrar_tablero(self, mostrar_minas=False):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.tablero[fila][columna] == 'X' and self.minas_tablero[fila][columna] == -1:
                    print("*", end=" ")
                elif self.tablero[fila][columna] == 'X' and mostrar_minas:
                    print(self.minas_tablero[fila][columna], end=" ")
                else:
                    print(self.tablero[fila][columna], end=" ")
            print()
        print()
    #lo que pasa al hacer click izquierod
    def descubrir_casilla(self, fila, columna):
        if self.tablero[fila][columna] == 'X':
            return
        if self.minas_tablero[fila][columna] == -1:
            self.tablero[fila][columna] = 'X'
            self.mostrar_tablero(True)
            print("¡Has perdido!")
            self.juego_terminado = True
        else:
            self.tablero[fila][columna] = str(self.minas_tablero[fila][columna])
            if self.tablero[fila][columna] == '0':
                for i in range(max(0, fila - 1), min(self.filas, fila + 2)):
                    for j in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                        if self.tablero[i][j] == ' ':
                            self.descubrir_casilla(i, j)
    #marcador intero para la condicion de victoria
    def contar_marcadorInterno(self):
        contador = 0
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.tablero[fila][columna] == 'X' and self.minas_tablero[fila][columna] == -1:
                    contador += 1
        return contador
    #contador de marcadores que se muestran en pantalla
    def contar_marcadores(self):
        contador = 0
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.tablero[fila][columna] == 'X':
                    contador += 1
        return contador
    

class BuscaminasGUI:
    def __init__(self, juego):
        self.juego = juego
        self.filas = juego.filas
        self.columnas = juego.columnas
        self.minas = juego.minas
        self.tile_size = 40
        self.width = self.columnas * self.tile_size
        self.height = self.filas * self.tile_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.marcadores = 0
        self.marcadorInterno=0
        

    def draw_grid(self):
        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
    #dibujar los numeros, la mina es -1, indica el numero de minas en su vecindad o blanco si no hay nada en su vecindad
    def draw_numbers(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)  # Dibuja el contorno negro

                # Verifica si la celda está revelada
                if self.juego.tablero[i][j] != ' ':
                    color = (255, 255, 255)  # Color de fondo blanco por defecto
                    number = self.juego.minas_tablero[i][j]

                    if self.juego.tablero[i][j] == 'X':  # Verifica si la casilla está marcada
                        color = (255, 0, 0)  # Cambia el color de la casilla marcada

                    pygame.draw.rect(self.screen, color, rect)  # Rellena el color de la celda
                    if number != 0 and number != -1 and self.juego.tablero[i][j] != 'X':
                        text = self.font.render(str(number), True, (0, 0, 0))
                        text_rect = text.get_rect(center=(j * self.tile_size + self.tile_size // 2,
                                                          i * self.tile_size + self.tile_size // 2))
                        self.screen.blit(text, text_rect)
    #poner marcadores
    def draw_marcadores(self):
        marcador_text = self.font.render(f"Marcadores: {self.juego.contar_marcadores()}/{self.minas}", True, (0, 0, 0))
        marcador_rect = marcador_text.get_rect()
        marcador_rect.topleft = (10, self.height + 10)  # Posición ajustada para los marcadores
        self.screen.blit(marcador_text, marcador_rect)
    #actualizar pantalla
    def update(self):
        self.width = self.columnas * self.tile_size
        self.height = self.filas * self.tile_size

        self.screen = pygame.display.set_mode((self.width, self.height + 40))  # Ajusta el tamaño de la ventana

        self.screen.fill((255, 255, 255))

        # Dibujar el tablero
        self.draw_grid()
        self.draw_numbers()

        # Dibujar los marcadores
        self.draw_marcadores()

        pygame.display.flip()
    #implementa las acciones que se realizan en el juego
    def run(self):
        while not self.juego.juego_terminado:
            self.update()
            for event in pygame.event.get():#cerrar el juego
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == MOUSEBUTTONDOWN:#presionar un boton
                    x, y = pygame.mouse.get_pos()
                    fila = y // self.tile_size
                    columna = x // self.tile_size

                    if event.button == 1:  # Click izquierdo abrir casilla
                        self.juego.descubrir_casilla(fila, columna)
                        self.update()
                    elif event.button == 3:  # Click derecho marcar casilla
                        if self.juego.tablero[fila][columna] == ' ':
                            self.juego.tablero[fila][columna] = 'X'
                            self.marcadores += 1
                            self.update()
                        elif self.juego.tablero[fila][columna] == 'X':  # Si la casilla está marcada, deshacer la marcación
                            self.juego.tablero[fila][columna] = ' '
                            self.marcadores -= 1
                            self.update()
                    #condicion de victoria, si el contador de marcadores es igual a de minas y a su vez todas las minas estan marcadas, se gana el juego
                    if self.juego.contar_marcadorInterno() == self.minas and self.marcadorInterno == self.minas:
                        print("¡Has ganado!")
                        self.juego.juego_terminado = True
                        self.update()

                    if self.juego.juego_terminado:
                        self.update()
                        return

            self.clock.tick(3)
# Pantalla en la que se selecciona la dificultad        
class PantallaInicial:
    def __init__(self):
        pygame.init()
        self.width = 300# Tamaño de la pantalla
        self.height = 200
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.opciones = ["Fácil", "Intermedio", "Difícil"]#Niveles de dificultad
        self.selected_option = None
        self.finished = False

    def mostrar_pantalla(self):
        while not self.finished:
            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Calcular áreas de clic para las opciones de dificultad
                    for i, opcion in enumerate(self.opciones):
                        text = self.font.render(opcion, True, (0, 0, 0))
                        text_rect = text.get_rect(center=(self.width // 2, 75 + i * 50))

                        # Obtener el rectángulo ampliado para el texto
                        expanded_text_rect = text_rect.inflate(20, 20)

                        # Verificar si se hizo clic dentro del área ampliada
                        if expanded_text_rect.collidepoint(x, y):
                            self.selected_option = self.opciones[i]
                            self.finished = True

            for i, opcion in enumerate(self.opciones):
                text = self.font.render(opcion, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.width // 2, 75 + i * 50))

                # Dibujar bordes negros alrededor de las opciones de dificultad
                expanded_text_rect = text_rect.inflate(20, 20)
                pygame.draw.rect(self.screen, (0, 0, 0), expanded_text_rect, 2)
                self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def obtener_dificultad(self):
        return self.selected_option.lower()



# Pantalla de juego
class PantallaJuego:
    def __init__(self, dificultad):
        self.filas = 12
        self.columnas = 12
        self.minas = 20 if dificultad == "fácil" else 30 if dificultad == "intermedio" else 40
        self.juego = Buscaminas(self.filas, self.columnas, self.minas)
        self.gui = BuscaminasGUI(self.juego)
        self.juego.register_observer(self.gui)
        self.finished = False

    def mostrar_pantalla(self):
        self.juego.inicializar_tablero()
        self.gui.run()

        while not self.finished:
            if self.juego.juego_terminado:
                if self.juego.contar_marcadorInterno() == self.minas:
                    self.mostrar_mensaje("¡Has ganado!")
                else:
                    self.mostrar_mensaje("¡Has perdido!")
                self.finished = True

    def mostrar_mensaje(self, mensaje):
        pygame.init()
        screen = pygame.display.set_mode((300, 200))
        font = pygame.font.Font(None, 36)

        text = font.render(mensaje, True, (0, 0, 0))
        text_rect = text.get_rect(center=(150, 100))

        screen.fill((255, 255, 255))
        screen.blit(text, text_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


if __name__ == "__main__":
    pantalla_inicial = PantallaInicial()
    pantalla_inicial.mostrar_pantalla()

    if pantalla_inicial.selected_option:
        dificultad = pantalla_inicial.obtener_dificultad()
        pantalla_juego = PantallaJuego(dificultad)

        # Bucle principal del juego
        while not pantalla_juego.finished:
            pantalla_juego.mostrar_pantalla()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pantalla_juego.finished = True
                    break  # Salir del bucle si se detecta el evento de cierre
                    

        # Si se sale del bucle, cerrar Pygame
        pygame.quit()


