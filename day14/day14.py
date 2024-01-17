class Board:
    def __init__(self):
        # This node corresponds to 500,0
        self.x_offset = 0
        self._board = [[None]]

    def convert_coords(self, x, y):
        nx = x - 500 + self.x_offset
        ny = y
        return nx, ny

    def set(self, x, y, v):
        # Convert the coordinates
        nx, ny = self.convert_coords(x, y)

        self._board[nx][ny] = v

    def set_sand(self, x, y):
        # Convert the coordinates
        nx, ny = self.convert_coords(x, y)

        self._board[nx][ny] = "o"

    def set_rock(self, x, y):
        # Convert the coordinates
        nx, ny = self.convert_coords(x, y)

        self._board[nx][ny] = "#"
        # print(self.show_board())

    def in_bounds(self, x, y):
        x, y = self.convert_coords(x, y)
        return 0 <= x < len(self._board) and 0 <= y < len(self._board[x])

    def expand_board(self, walls):
        ymax = 0
        xmax = 0
        xmin = 0
        for wall in walls:
            for x, y in wall:
                x, y = self.convert_coords(x, y)
                ymax = max(ymax, y)
                xmax = max(xmax, x)
                xmin = min(xmin, x)
        self.x_offset = abs(xmin)
        print(f"Expanding board to {xmin}, {xmax}, {ymax}")
        print(self.x_offset)

        def expand(x, y):
            if x < 0:
                for _ in range(abs(x)):
                    self._board.insert(0, [None for _ in range(len(self._board[0]))])
                x = 0
            if x >= len(self._board):
                for _ in range(x - len(self._board) + 1):
                    self._board.append([None for _ in range(len(self._board[0]))])
            if y >= len(self._board[x]):
                for row in self._board:
                    for _ in range(y - len(row) + 1):
                        row.append(None)

        expand(xmax, ymax)
        expand(xmin, ymax)
        # print(self.show_board())
        self._board[self.x_offset][0] = "+"

    def get(self, x, y):
        nx, ny = self.convert_coords(x, y)
        return self._board[nx][ny]

    def show_board(self):
        out = ""
        for i in range(len(self._board[0])):
            for j in range(len(self._board)):
                out += str(self._board[j][i]) if self._board[j][i] is not None else "."
            out += "\n"

        return out


class Sand:
    def __init__(self, board: Board):
        self.resting = False
        self.board = board
        self.x = 500
        self.y = 0

    def move_down(self):
        # Move down
        if not self.board.in_bounds(self.x, self.y + 1):
            return False
        if self.board.get(self.x, self.y + 1) is None:
            self.y += 1
            return True

        # Move down left
        if not self.board.in_bounds(self.x - 1, self.y + 1):
            return False
        if self.board.get(self.x - 1, self.y + 1) is None:
            self.x -= 1
            self.y += 1
            return True

        # Move down right
        if not self.board.in_bounds(self.x + 1, self.y + 1):
            return False
        if self.board.get(self.x + 1, self.y + 1) is None:
            self.x += 1
            self.y += 1
            return True
        # If no move down, set resting to True
        self.board.set_sand(self.x, self.y)
        self.resting = True
        return True


class Day14Runner:
    def __init__(self, lines: list, floor=False):
        self.lines = lines
        self.board = Board()
        self.total_resting = 0
        self.draw_walls(floor)

        print(self.board.show_board())

    def floor(self, walls):
        # Find the min and max x and y
        minx = min([min([x for x, y in wall]) for wall in walls])
        maxx = max([max([x for x, y in wall]) for wall in walls])
        maxy = max([max([y for x, y in wall]) for wall in walls])

        print(f"Flooring from {minx}, {maxx}, {maxy}")

        y = maxy + 2

        return [[500 + y, y], [500 - y, y]]

    def draw_walls(self, floor):
        walls = [
            [list(map(int, points.split(","))) for points in line.split(" -> ")]
            for line in self.lines
        ]

        if floor:
            walls.append(self.floor(walls))

        self.board.expand_board(walls)
        print("board set")
        # print(self.board.show_board())

        for coords in walls:
            for i in range(len(coords) - 1):
                startx, starty = coords[i]
                endx, endy = coords[i + 1]

                for x, y in self.line_coords((startx, starty), (endx, endy)):
                    print(f"Setting rock at {x}, {y}")
                    self.board.set_rock(x, y)

    def line_coords(self, pos1, pos2):
        print(f"Drawing line from {pos1} to {pos2}")
        # Return all the positions from pos1 to pos2
        xs = min(pos1[0], pos2[0])
        xm = max(pos1[0], pos2[0])
        ys = min(pos1[1], pos2[1])
        ym = max(pos1[1], pos2[1])
        return [(x, y) for x in range(xs, xm + 1) for y in range(ys, ym + 1)]

    def simulate(self):
        while self.place_sand() is None:
            self.total_resting += 1

    def place_sand(self):
        if self.board.get(500, 0) != "+":
            return "failed"
        piece = Sand(self.board)
        while not piece.resting:
            res = piece.move_down()
            # print(f"Piece moved {res}")
            if not res:
                return "failed"

    def find_total_resting(self):
        self.simulate()
        print(self.board.show_board())
        return self.total_resting


if __name__ == "__main__":
    with open("day14/test.txt", "r") as file:
        lines = file.readlines()
        test = Day14Runner(lines)
        assert test.find_total_resting() == 24

    with open("day14/input.txt", "r") as file:
        lines = file.readlines()
        run = Day14Runner(lines)
        print(run.find_total_resting())

    with open("day14/test.txt", "r") as file:
        lines = file.readlines()
        test = Day14Runner(lines, floor=True)
        assert test.find_total_resting() == 93

    with open("day14/input.txt", "r") as file:
        lines = file.readlines()
        run = Day14Runner(lines, floor=True)
        print(run.find_total_resting())
