class Day12Runner:
    def __init__(self, lines):
        self.board = [
            [0 for _ in range(len(lines[0].strip()))] for _ in range(len(lines))
        ]
        self.reset_visited()
        for i, line in enumerate(lines):
            for j, ch in enumerate(line.strip()):
                if ch == "S":
                    self.start = (i, j)
                    self.board[i][j] = 1
                elif ch == "E":
                    self.end = (i, j)
                    self.board[i][j] = 26
                else:
                    # return the ascii value of the char, offset so that a = 1
                    self.board[i][j] = ord(ch) - 96

    def reset_visited(self):
        self.visited = [
            [-1 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

    def find_shortest_path(self):
        self.visited[self.start[0]][self.start[1]] = 0
        q = [self.start]
        while q:
            r, c = q.pop(0)
            # print(pos)
            for dr, dc in (
                (r, c + 1),
                (r, c - 1),
                (r + 1, c),
                (r - 1, c),
            ):
                if not self.valid_move((r, c), (dr, dc)):
                    continue
                if (
                    self.visited[dr][dc] != -1
                    and self.visited[dr][dc] <= self.visited[r][c] + 1
                ):
                    continue
                self.visited[dr][dc] = self.visited[r][c] + 1
                if (dr, dc) == self.end:
                    print("Found end")
                    print(self.visited[dr][dc])
                    return self.visited[dr][dc]
                q.append((dr, dc))

    def shortest_from(self, start):
        results = []
        for i, line in enumerate(self.board):
            for j, ch in enumerate(line):
                if ch == ord(start) - 96:
                    self.start = (i, j)
                    path_length = self.find_shortest_path()
                    if path_length is not None:
                        results.append(path_length)
                    self.reset_visited()
        print(results)
        return min(results)

    def valid_move(self, pos, n):
        if n[0] < 0 or n[0] >= len(self.board):
            return False
        if n[1] < 0 or n[1] >= len(self.board[0]):
            return False
        # Height jumps of more than one are invalid
        if self.board[n[0]][n[1]] - 1 > self.board[pos[0]][pos[1]]:
            return False
        return True


if __name__ == "__main__":
    with open("day12/test.txt", "r") as file:
        lines = file.readlines()
        test = Day12Runner(lines)
        assert test.find_shortest_path() == 31

    with open("day12/input.txt", "r") as file:
        lines = file.readlines()
        runner = Day12Runner(lines)
        print(runner.find_shortest_path())

    with open("day12/test.txt", "r") as file:
        lines = file.readlines()
        test = Day12Runner(lines)
        assert test.shortest_from("a") == 29

    with open("day12/input.txt", "r") as file:
        lines = file.readlines()
        runner = Day12Runner(lines)
        print(runner.shortest_from("a"))
