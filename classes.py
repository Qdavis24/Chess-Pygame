import pygame


class Position:
    COLUMNS = 8
    ROWS = 8

    def __init__(self, width, height):
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
        self.row_bounds = [self.piece_height * i for i in range(self.ROWS + 1)]
        self.col_bounds = [self.piece_width * i for i in range(self.COLUMNS + 1)]

    def _create_position_matrix(self):

        curr_pos = [self.offset_x, self.offset_y]

        for i in range(self.ROWS):
            column = []
            for j in range(self.COLUMNS):
                column.append(tuple(curr_pos))
                curr_pos[0] += self.piece_width
            self.position_matrix.append(column)
            curr_pos[0] = self.offset_x
            curr_pos[1] += self.piece_height


class Events:
    def __init__(self, position, graph):
        self.position = position
        self.graph = graph
        self.select = True
        self.curr_node = None

    def handle_click(self, click_pos):
        if self.select:
            self.curr_node = self._get_node_from_click(click_pos)
            self.select = False
        else:
            to = self._get_node_from_click(click_pos)
            valid_to_nodes = self.curr_node.piece.valid_moves(self.curr_node)
            if to in valid_to_nodes:
                self.curr_node.piece.update(to.position)
                self.graph.update_node(self.curr_node, to)

                self.select = True
                self.curr_node = None

    def _get_node_from_click(self, click_pos):
        row = self._find_range_index(self.position.row_bounds, click_pos[1])
        col = self._find_range_index(self.position.col_bounds, click_pos[0])
        return self.graph.node_matrix[row][col]

    def _find_range_index(self, bounds, value):
        for i in range(1, len(bounds)):
            if bounds[i - 1] < value < bounds[i]:
                return i - 1


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

    def update_node(self, start_node, end_node):
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


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.color = color
        self.move_history = []
        self.number_move = 0

    def update(self, pos):
        self.rect.center = pos


class Pawn(Piece):
    def __init__(self, color, x, y, width, height):
        super().__init__(color, width, height)
        pygame.draw.rect(self.image, color, (0, 0, width, height))  # Fill
        pygame.draw.rect(self.image, "red", (0, 0, width, height), 2)
        self.update((x, y))

    def valid_moves(self, node):
        valid_moves_nodes = []
        for node in self._check_diagonals(node):
            valid_moves_nodes.append(node)
        valid_moves_nodes.append(self._check_forward_one(node))
        valid_moves_nodes.append(self._check_forward_two(node))
        return valid_moves_nodes

    def _check_diagonals(self, node):
        nodes = []
        if (node.up_left and node.up_left.piece) and node.up_left.piece.color != self.color:
            nodes.append(node.up_left)
        if (node.up_right and node.up_right.piece) and node.up_right.piece.color != self.color:
            nodes.append(node.up_right)
        return nodes

    def _check_forward_two(self, node):
        if not self.number_move == 0:
            return

        curr_node = node
        for i in range(2):
            if not curr_node.up or curr_node.up.piece:
                return
            curr_node = curr_node.up
        return curr_node

    def _check_forward_one(self, node):
        if not node.up or node.up.piece:
            return
        return node.up
