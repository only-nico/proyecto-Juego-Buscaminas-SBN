import pygame
import sys
import random
# Dimensiones de la pantalla y la matriz
n = 10
width, height = 400, 400
cell_size = width // n
porcentaje_minas=20
# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Matriz Seleccionable')
clock = pygame.time.Clock()

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
selected_color = (50, 150, 255)
unselected_color = (200, 200, 200)
hover_color = (255, 255, 0)  # Nuevo color para cuando el cursor está sobre la celda
click_color = (255, 0, 0)   # Nuevo color al hacer clic en la celda

# Crear matriz de celdas
matrix = [[0 for _ in range(n)] for _ in range(n)]
num_mines = (n * n * porcentaje_minas) // 100

mine_indices = random.sample(range(n * n), num_mines)

# Asignar el valor -1 en las celdas seleccionadas como minas
for idx in mine_indices:
    row = idx // n
    col = idx % n
    matrix[row][col] = -1
def draw_grid():
    for y in range(n):
        for x in range(n):
            color = selected_color if matrix[y][x] else unselected_color
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect, 0)
            pygame.draw.rect(screen, black, rect, 1)

def toggle_cell(x, y):
    matrix[y // cell_size][x // cell_size] = not matrix[y // cell_size][x // cell_size]

# Bucle principal del juego
running = True
while running:
    screen.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                toggle_cell(*pygame.mouse.get_pos())

    # Obtener la posición del mouse
    mouse_pos = pygame.mouse.get_pos()

    for y in range(n):
        for x in range(n):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            # Si el mouse está encima de la celda
            if rect.collidepoint(mouse_pos):
                # Si se hace clic, cambia al color al hacer clic
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.rect(screen, selected_color, rect, 0)
                else:
                    # Si no se hace clic, cambia al color al pasar el mouse
                    pygame.draw.rect(screen, hover_color, rect, 0)
            else:
                # Si no se encuentra el mouse sobre la celda, usa el color normal
                color = selected_color if matrix[y][x] else unselected_color
                pygame.draw.rect(screen, color, rect, 0)
            pygame.draw.rect(screen, black, rect, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
