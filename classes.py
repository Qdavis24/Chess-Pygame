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
        self.value = None
        self.position = pos


class Graph:
    COLUMNS = 8
    ROWS = 8

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.node_matrix = []
        self.position_matrix = []
        self.top_left = None

        self._create_position_matrix()
        self._create_node_matrix()
        self._connect_nodes()


    def _create_position_matrix(self):
        cell_width = self.width / self.COLUMNS
        cell_height = self.height / self.ROWS
        mid_offset_x = cell_width / 2
        mid_offset_y = cell_height / 2

        curr_pos = [mid_offset_x, mid_offset_y]

        for i in range(self.ROWS):
            column = []
            for j in range(self.COLUMNS):
                column.append(tuple(curr_pos))
                curr_pos[0] += cell_width
            self.position_matrix.append(column)
            curr_pos[0] = mid_offset_x
            curr_pos[1] += cell_height

    def _create_node_matrix(self, rows, cols):
        for i in range(rows):
            column = []
            for j in range(cols):
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



graph = Graph(1000, 1000)
graph.create_position_matrix()
graph.create_matrix_nodes(8, 8)
graph.connect_nodes()
graph.print_nodes()
