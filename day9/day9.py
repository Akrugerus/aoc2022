test_case = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


class spot:
    _x: int
    _y: int

    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, int):
        self._x = int

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, int):
        self._y = int

    def __repr__(self):
        return self.hash()

    def move(self, y, x):
        print(self.y, self.x, "  ->  ", self.y + y, self.x + x)
        self.x += x
        self.y += y

    def hash(self):
        return f"{self.x},{self.y}"

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def delta(self, other):
        return self.y - other.y, self.x - other.x

    def delta_x(self, other):
        print(f"x delta self -> {self} other -> {other} is {self.x-other.x}")
        return self.x - other.x

    def delta_y(self, other):
        print(f"y delta self -> {self} other -> {other} is {self.y-other.y}")
        return self.y - other.y

    def adjacent(self, other):
        if self.distance(other) < 2:
            return True
        elif abs(self.delta_x(other)) == 1 and abs(self.delta_y(other)) == 1:
            return True
        return False

    def chase_direction(self, head):
        def clamp(x):
            if x > 1:
                return 1
            if x < -1:
                return -1
            return x

        y, x = head.delta(self)
        return clamp(y), clamp(x)

    def chase_spot(self, head):
        if not self.adjacent(head):
            self.move(*self.chase_direction(head))


class spotlist:
    _list: list[spot]

    def __init__(self, length):
        self._list = [spot() for _ in range(0, length)]

    def move(self, y, x):
        self._list[0].move(y, x)
        self.follow_head()

    @property
    def tail(self):
        return self._list[-1]

    def follow_head(self):
        for i in range(1, len(self._list)):
            self._list[i].chase_spot(self._list[i - 1])


class Day9Runner:
    _tail_visits: dict

    def __init__(self, page, length):
        self._tail_visits = {}
        self.spots = spotlist(length)
        for line in page.split("\n"):
            self.line_feed(line)

    def line_feed(self, line):
        direction = line.split(" ")[0]
        x = line.split(" ")[1]

        for _ in range(0, int(x)):
            self.parse_move(direction)

    def move(self, y, x):
        self.spots.move(y, x)
        self.record_tail()

    def record_tail(self):
        if self._tail_visits.get(self.spots.tail.hash(), None) is None:
            self._tail_visits[self.spots.tail.hash()] = 1

    def parse_move(self, direction):
        match direction:
            case "R":
                self.move(0, 1)
            case "L":
                self.move(0, -1)
            case "U":
                self.move(-1, 0)
            case "D":
                self.move(1, 0)

    @property
    def tail_visits(self):
        return len(self._tail_visits)


if __name__ == "__main__":
    test = Day9Runner(test_case, 2)
    assert test.tail_visits == 13
    test2 = Day9Runner(test_case, 10)
    print(test2.tail_visits)
    assert test2.tail_visits == 1
    with open("day9/input.txt", "r") as file:
        body = file.read()
        d9 = Day9Runner(body, 2)
        print(d9.tail_visits)

        d9_2 = Day9Runner(body, 10)
        print(d9_2.tail_visits)
