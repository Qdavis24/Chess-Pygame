import pygame
from classes import Graph, Position, Game, Pawn, GameStatusBar

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 950

BOARD_WIDTH = 800
BOARD_HEIGHT = 800

START_X = CANVAS_WIDTH - BOARD_WIDTH
START_Y = CANVAS_HEIGHT - BOARD_HEIGHT


position = Position(START_X, START_Y, BOARD_WIDTH, BOARD_HEIGHT)
graph = Graph(position.position_matrix)
game = Game(position, graph)

pygame.init()

whites = pygame.sprite.Group()
blacks = pygame.sprite.Group()

game_status_bar = GameStatusBar(BOARD_WIDTH, START_Y)

for i in range(8):
    pos = position.position_matrix[0][i]
    new_pawn = Pawn("black", pos[0], pos[1], position.piece_width, position.piece_height)
    blacks.add(new_pawn)
    graph.node_matrix[0][i].piece = new_pawn

for i in range(8):
    pos = position.position_matrix[7][i]
    new_pawn = Pawn("white", pos[0], pos[1], position.piece_width, position.piece_height)
    whites.add(new_pawn)
    graph.node_matrix[7][i].piece = new_pawn

screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(pygame.mouse.get_pos())
            game_status_bar.update(game.curr_player)


    screen.fill("green")

    whites.draw(screen)
    blacks.draw(screen)
    screen.blit(game_status_bar.image, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
