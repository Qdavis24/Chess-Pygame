import pygame


class Position:
    COLUMNS = 8
    ROWS = 8

    def __init__(self, start_x, start_y, width, height):
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.height = height
        self.piece_width = None
        self.piece_height = None
        self.offset_x = None
        self.offset_y = None
        self.row_bounds = None
        self.col_bounds = None

        self.position_matrix = []
        self._initialize_piece_dimensions()
        self._create_dimension_bounds()
        self._create_position_matrix()

    def _initialize_piece_dimensions(self):
        self.piece_width = self.width / self.COLUMNS
        self.piece_height = self.height / self.ROWS
        self.offset_x = self.piece_width / 2
        self.offset_y = self.piece_height / 2

    def _create_dimension_bounds(self):
        self.row_bounds = [self.piece_height * i + self.start_y for i in range(self.ROWS + 1)]
        self.col_bounds = [self.piece_width * i + self.start_x for i in range(self.COLUMNS + 1)]

    def _create_position_matrix(self):

        curr_pos = [self.offset_x + self.start_x, self.offset_y + self.start_y]

        for i in range(self.ROWS):
            column = []
            for j in range(self.COLUMNS):
                column.append(tuple(curr_pos))
                curr_pos[0] += self.piece_width
            self.position_matrix.append(column)
            curr_pos[0] = self.offset_x + self.start_x
            curr_pos[1] += self.piece_height


class Game:
    def __init__(self, position, graph):
        self.position = position
        self.graph = graph
        self.curr_node = None
        self.curr_player = "white"

    def handle_click(self, click_pos):
        print(f"{self.curr_player} | {self.curr_node}")
        clicked_node = self._get_node_from_click(click_pos)
        type_click = self._type_click(clicked_node)
        print(f"type : {type_click}")
        if type_click == "null":
            return
        elif type_click == "select":
            self._select_click(clicked_node)
        elif type_click == "move":
            to_node = self._get_node_from_click(click_pos)
            self._move_click(to_node)

    def _select_click(self, select_node):
        if self.curr_node:
            self.curr_node.piece.highlight(False)
        self.curr_node = select_node
        self.curr_node.piece.highlight(True)

    def _move_click(self, move_node):
        print(f"color : {self.curr_node.piece.color}\n"
              f"curr_piece pos : {self.curr_node.position}\n"
              f"valid moves : {self.curr_node.piece.valid_moves(self.curr_node)}\n"
              f"valid moves pos : {[node.position for node in self.curr_node.piece.valid_moves(self.curr_node)]}")
        if move_node in self.curr_node.piece.valid_moves(self.curr_node):
            print(f"in valid moves {move_node}"
                  f"piece? {move_node.piece}"
                  f"move position {move_node.position}"
                  f"curr position {self.curr_node.position}")
            if move_node.piece:
                move_node.piece.kill()
            self.curr_node.piece.highlight(False)
            self.curr_node.piece.update(move_node.position)
            self.graph.update_nodes(start_node=self.curr_node, end_node=move_node)
            self._change_player()

    def _get_node_from_click(self, click_pos):
        row = self._find_range_index(self.position.row_bounds, click_pos[1])
        col = self._find_range_index(self.position.col_bounds, click_pos[0])
        return self.graph.node_matrix[row][col]

    def _find_range_index(self, bounds, value):
        for i in range(1, len(bounds)):
            if bounds[i - 1] <= value <= bounds[i]:
                return i - 1

    def _type_click(self, node):
        if not self.curr_node and (not node.piece or node.piece.color != self.curr_player):
            return "null"
        if not node.piece or node.piece.color != self.curr_player:
            return "move"
        return "select"

    def _change_player(self):
        self.curr_player = "white" if self.curr_player == "black" else "black"
        self.curr_node = None


class Node:
    def __init__(self, pos):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.up_left = None
        self.up_right = None
        self.down_left = None
        self.down_right = None
        self.piece = None
        self.position = pos


class Graph:
    COLUMNS = 8
    ROWS = 8

    def __init__(self, position_matrix):
        self.position_matrix = position_matrix
        self.node_matrix = []
        self.top_left = None
        self._create_node_matrix()
        self._connect_nodes()

    def _create_node_matrix(self):
        for i in range(self.ROWS):
            column = []
            for j in range(self.COLUMNS):
                curr_pos = self.position_matrix[i][j]
                column.append(Node((curr_pos[0], curr_pos[1])))
            self.node_matrix.append(column)
        self.top_left = self.node_matrix[0][0]

    def _connect_nodes(self):
        bounds = [0, 7]
        directions = {}
        for i in range(len(self.node_matrix)):
            for j in range(len(self.node_matrix[i])):
                directions["left"] = [i, j - 1]
                directions["right"] = [i, j + 1]
                directions["up"] = [i - 1, j]
                directions["down"] = [i + 1, j]
                directions["up_left"] = [i - 1, j - 1]
                directions["up_right"] = [i - 1, j + 1]
                directions["down_left"] = [i + 1, j - 1]
                directions["down_right"] = [i + 1, j + 1]

                for direction, indexes in directions.items():
                    if bounds[0] <= indexes[0] <= bounds[1] and bounds[0] <= indexes[1] <= bounds[1]:
                        curr_node = self.node_matrix[i][j]
                        connected_node = self.node_matrix[indexes[0]][indexes[1]]
                        setattr(curr_node, direction, connected_node)

    def update_nodes(self, start_node, end_node):
        piece = start_node.piece
        start_node.piece = None
        end_node.piece = piece

    def print_nodes(self):
        curr_node = self.top_left
        while curr_node != None:
            while curr_node.right != None:
                print(curr_node.position, end=" ")
                curr_node = curr_node.right
            print(curr_node.position)
            curr_node = curr_node.down
            while curr_node.left != None:
                curr_node = curr_node.left


class GameStatusBar:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont('Arial', 32)
        self.update("White")

    def update(self, player):
        pygame.draw.rect(self.image, "black", (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, "white", (10, 10, self.width - 20, self.height - 20))
        pos = self.rect.center
        text = self.font.render(f"{player}'s Turn!", True, "Black")
        pos = (pos[0] - text.get_rect().centerx, pos[1] - text.get_rect().centery)
        self.image.blit(text, pos)


class Piece(pygame.sprite.Sprite):
    def __init__(self, x, y, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.original_image = None  # initialize with value during construction of subclass
        self.rect = self.image.get_rect()
        self.update((x, y))
        self.color = color
        self.move_history = []
        self.number_move = 0

    def update(self, pos):
        self.rect.center = pos

    def valid_moves(self, node):
        valid_moves_nodes = []
        for n in self._check_diagonals(node):
            valid_moves_nodes.append(n)
        valid_moves_nodes.append(self._check_forward_one(node))
        valid_moves_nodes.append(self._check_forward_two(node))

        return [n for n in valid_moves_nodes if n]

    def _check_diagonals(self, node):
        nodes = []
        diag_l_node = getattr(node, self.move_color_codex[self.color]["dl"])
        diag_r_node = getattr(node, self.move_color_codex[self.color]["dr"])

        if (diag_l_node and diag_l_node.piece) and diag_l_node.piece.color != self.color:
            nodes.append(diag_l_node)
        if (diag_r_node and diag_r_node.piece) and diag_r_node.piece.color != self.color:
            nodes.append(diag_r_node)
        return nodes

    def _check_forward_one(self, node):
        forward_node = getattr(node, self.move_color_codex[self.color]["f"])
        if not forward_node or forward_node.piece:
            return
        return forward_node

    def highlight(self, active):

        overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        if active:
            overlay.fill((128, 128, 128, 128))
            self.image.blit(overlay, (0, 0))
        else:
            self.image = self.original_image.copy()


class Pawn(Piece):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color, width, height)
        image = pygame.image.load(f"./assets/imgs/pieces/chess_piece_2_{self.color}_pawn.png")
        image = pygame.transform.scale(image, (width, height))
        self.image.blit(image, (0, 0))
        self.original_image = self.image.copy()

        self.move_color_codex = {
            "white":
                {
                    "f": "up",
                    "dl": "up_left",
                    "dr": "up_right"
                },
            "black":
                {
                    "f": "down",
                    "dl": "down_left",
                    "dr": "down_right",
                }
        }

    def valid_moves(self, node):
        valid_moves_nodes = []
        for n in self._check_diagonals(node):
            valid_moves_nodes.append(n)
        valid_moves_nodes.append(self._check_forward_one(node))
        valid_moves_nodes.append(self._check_forward_two(node))

        return [n for n in valid_moves_nodes if n]

    def _check_diagonals(self, node):
        nodes = []
        diag_l_node = getattr(node, self.move_color_codex[self.color]["dl"])
        diag_r_node = getattr(node, self.move_color_codex[self.color]["dr"])

        if (diag_l_node and diag_l_node.piece) and diag_l_node.piece.color != self.color:
            nodes.append(diag_l_node)
        if (diag_r_node and diag_r_node.piece) and diag_r_node.piece.color != self.color:
            nodes.append(diag_r_node)
        return nodes

    def _check_forward_two(self, node):
        if not self.number_move == 0:
            return

        curr_node = node
        for i in range(2):
            forward_node = getattr(curr_node, self.move_color_codex[self.color]["f"])
            if not forward_node or forward_node.piece:
                return
            curr_node = forward_node
        return curr_node

    def _check_forward_one(self, node):
        forward_node = getattr(node, self.move_color_codex[self.color]["f"])
        if not forward_node or forward_node.piece:
            return
        return forward_node


class King(Piece):
    def __init__(self, x, y, color, width, height):
        super().__init__(color, width, height)
        image = pygame.image.load(f"./assets/imgs/pieces/chess_piece_2_{self.color}_king.png")
        image = pygame.transform.scale(image, (width, height))
        self.image.blit(image, (0, 0))
        self.original_image = self.image.copy()

        self.move_color_codex = {
            "white":
                {
                    "f": "up",
                    "b": "down",
                    "dl": "up_left",
                    "dr": "up_right"
                },
            "black":
                {
                    "f": "down",
                    "b": "up",
                    "dl": "down_left",
                    "dr": "down_right",
                }
        }
    def valid_moves(self, node):
