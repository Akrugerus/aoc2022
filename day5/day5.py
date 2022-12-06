class Game:
    board: list[list[str]]

    def __init__(self, lines):
        # set board
        self.board = list()
        # calc num of columns
        legend_line = lines[:-1]
        columns = len(legend_line.split())

        # for each column
        for i in range(1, len(legend_line), 3):
            # try to ascend towards the top of the page in that column
            for j in range(len(lines), 0, -1):
                try:
                    print(lines[j][i])
                # append values as you go

                # until indexoutofbound or space
                except IndexError:
                    pass

        lines.split("\n")

    def playall(self, *args):
        map(self.play, args)

    def play(self, command):
        cmd_parts = command.split(" ")
        amount = cmd_parts[2]
        frm = cmd_parts[4] - 1
        to = cmd_parts[6] - 1
        self.move(amount, frm, to)

    def move(self, amount: int, frm: int, to: int):
        for _ in range(0, amount):
            i = self.board[frm].pop()
            self.board[to].append(i)

    def collect(self):
        return "".join(self.board[i].pop() for i in range(0, len(self.board)))


if __name__ == "__main__":
    with open("day5/input.txt", "r") as file:
        sections = file.read().strip().split("\n\n")
        game = Game(sections[0])
        commands = sections[1].split("\n")
        game.playall(commands)
        print(game.collect())
