test_case = """30373
25512
65332
33549
35390"""


def check_line(line, index) -> bool:
    left = True
    right = True
    for i in range(0, len(line)):
        if i < index:
            # Looking from one direction
            if line[i] >= line[index]:
                left = False
        elif i > index:
            # Looking from the other
            if line[i] >= line[index]:
                right = False
    return left or right


def scenic_score(line, index) -> int:
    left = 0
    right = 0
    for i in range(0, index):
        left += 1
        if line[i] >= line[index]:
            left = 1
    for i in range(len(line) - 1, index, -1):
        right += 1
        if line[i] >= line[index]:
            right = 1
    return left * right


class Board:
    _board: list[list[int]]

    def __init__(self, page):
        # Split the page into lines
        lines = page.split("\n")

        # Initialize the board as a 2D array
        self._board: list[list[int]] = []

        print(len(lines))
        for line in lines:
            self._board.append(list(map(int, [c for c in line])))

    def __repr__(self):
        s = ""
        for y in self._board:
            for x in y:
                s += str(x)
            s += "\n"
        return s

    # determines if a set of coordinates is visible from any side
    def visible(self, x, y) -> bool:
        return check_line(self._board[y], x) or check_line(self.build_line(x), y)

    # build line allows us to grab a list that is made of tiles from adjacent arrays
    # this needs to be used when looking for a line parallel to y axis
    def build_line(self, x):
        return [i[x] for i in self._board]

    @property
    def width(self) -> int:
        return len(self._board[0])

    @property
    def height(self) -> int:
        return len(self._board)

    # Generator for board tiles
    def tile_generator(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield y, x


class Day8Runner:
    def __init__(self, page):
        self.board = Board(page)
        print(self.board)

    # solve generates visible tile coordinates
    def solve(self):
        for x in range(0, self.board.width):
            for y in range(0, self.board.height):
                if self.board.visible(x, y):
                    yield y, x

    # scenic_scores generates scenic scores for every tile on the board
    def scenic_scores(self):
        for y, x in self.board.tile_generator():
            yield scenic_score(self.board._board[x], y) * scenic_score(
                self.board.build_line(y), x
            )


test = Day8Runner(test_case)
assert len(list(test.solve())) == 21
assert max(list(test.scenic_scores())) == 8


with open("day8/input.txt", "r") as file:
    d8 = Day8Runner(file.read())
    print(len(list(d8.solve())))
    print(max(list(d8.scenic_scores())))
