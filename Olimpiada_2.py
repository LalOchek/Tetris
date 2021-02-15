import pygame
from copy import deepcopy
from random import choice, randrange

w, h = 10, 20
TILE = 50
pygame.init()
clock = pygame.time.Clock()
FPS = 60
size = (w * TILE, h * TILE)
screen = pygame.display.set_mode(size)

res = 750, 600
sc = pygame.display.set_mode(res)




FIG_COORDS = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]

speed_tetra, now_speed, limit_speed = 60, 0, 2000

tetr_map = [[0 for i in range(w)] for j in range(h)]


def tetro_fig(FIG_COORDS):  #figures
    squar = []
    for fig_cor in FIG_COORDS:
        tile = []
        for x, y in fig_cor:
            coor = [x + w // 2, y + 1]
            tile.append(coor)
        squar.append(tile)
    return squar


fig = deepcopy(choice(tetro_fig(FIG_COORDS)))


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, cell_size):
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(40, 40, 40),
                                 (x * self.cell_size,
                                  y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        c_x = (mouse_pos[0]) // self.cell_size
        c_y = (mouse_pos[1]) // self.cell_size
        if c_x < 0 or c_x >= self.width or c_y < 0 or c_y >= self.height:
            return None
        return c_x, c_y


class Figures(Board):
    def __init__(self, w, h):
        # значения по умолчанию
        super().__init__(w, h)

    def render(self, col, coords):
        x, y = coords
        pygame.draw.rect(screen, col,
            (x * self.cell_size,
             y * self.cell_size,
             self.cell_size - 2, self.cell_size - 2), 0)


def chek_board():
    if fig[i][0] < 0 or fig[i][0] == w:
        return True
    elif fig[i][1] > h - 1 or tetr_map[fig[i][1]][fig[i][0]]:
        return True
    return False


board = Board(w, h)
tet = Figures(w, h)
running = True
while running:
    dx, rotate = 0, False
    screen.fill((0, 0, 0))
    delta_x = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for i in range(4):
                    delta_x = -1
            elif event.key == pygame.K_RIGHT:
                for i in range(4):
                    delta_x = 1
            elif event.key == pygame.K_DOWN:
                limit_speed = 100
            elif event.key == pygame.K_UP:
                rotate = True
    now_speed += speed_tetra
    if now_speed > limit_speed:
        now_speed = 0
        old_fig = deepcopy(fig)
        for i in range(4):
            fig[i][1] += 1
            if chek_board():
                for i in range(4):
                    tetr_map[old_fig[i][1]][old_fig[i][0]] = pygame.Color('white')
                fig = deepcopy(old_fig)
                limit_speed = 2000
                break
    # вращение (rotate)
    mid = fig[0]
    old_fig = deepcopy(fig)
    if rotate:
        for i in range(4):
            x = fig[i][1] - mid[1]
            y = fig[i][0] - mid[0]
            fig[i][0] = mid[0] - x
            fig[i][1] = mid[1] + y
            if chek_board():
                fig = deepcopy(choice(tetro_fig(FIG_COORDS)))
                break
    last_ln = h - 1
    for row in range(h - 1, -1, -1):
        count = 0
        for i in range(w):
            if tetr_map[row][i]:
                count += 1
            tetr_map[last_ln][i] = tetr_map[row][i]
        if count < w:
            last_ln -= 1
    old_fig = deepcopy(fig)
    for i in range(4):
        fig[i][0] += delta_x
        if chek_board():
            fig = deepcopy(choice(tetro_fig(FIG_COORDS)))
            break
    board.render()
    for i in range(4):
        tet.render(pygame.Color('White'), fig[i])
    for y, raw in enumerate(tetr_map):
        for x, col in enumerate(raw):
            if col:
                tet.render(col, (x, y))
    pygame.display.flip()
    clock.tick(FPS)