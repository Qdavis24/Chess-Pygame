import pygame
from classes import Graph, Position, Events, Pawn

WIDTH = 800
HEIGHT = 800

position = Position(WIDTH, HEIGHT)
graph = Graph(position.position_matrix)
events = Events(position, graph)

pygame.init()

whites = pygame.sprite.Group()
blacks = pygame.sprite.Group()

for i in range(8):
    pos = position.position_matrix[0][i]
    new_pawn = Pawn("white", pos[0], pos[1], position.piece_width, position.piece_height)
    whites.add(new_pawn)
    graph.node_matrix[0][i].piece = new_pawn

for i in range(8):
    pos = position.position_matrix[7][i]
    new_pawn = Pawn("black", pos[0], pos[1], position.piece_width, position.piece_height)
    blacks.add(new_pawn)
    graph.node_matrix[7][i].piece = new_pawn








screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            events.handle_click(pygame.mouse.get_pos())
    screen.fill("green")


    whites.draw(screen)
    blacks.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()