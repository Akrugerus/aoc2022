test_case = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


class Game:
    board: list[list[str]]

    def __init__(self, board):
        board_lines: list[str] = board.split("\n")
        self.board = list()
        legend_line = board_lines[-1]

        # Move from left to right, stopping at the column with the stack
        for i in range(1, len(legend_line), 4):
            container = list()
            # In the stack column, move from the bottom of the stack to the top, appending values in the correct order
            for j in range(len(board_lines) - 2, -1, -1):
                try:
                    if board_lines[j][i] == " ":
                        raise IndexError
                    container.append(board_lines[j][i])
                # If we get an IndexError, there should be no more values for this stack
                except IndexError:
                    break

            # Append the stack to the board list
            self.board.append(container)

    def playall(self, cmds: str):
        [self.play(c) for c in cmds.split("\n")]

    def playalltwo(self, cmds: str):
        [self.playtwo(c) for c in cmds.split("\n")]

    def play(self, cmd):
        c = cmd.split(" ")
        amount = int(c[1])
        frm = int(c[3])
        to = int(c[5])
        self.move(amount, frm, to)

    def playtwo(self, cmd):
        c = cmd.split(" ")
        amount = int(c[1])
        frm = int(c[3])
        to = int(c[5])
        self.move_new(amount, frm, to)

    def move(self, amount: int, frm: int, to: int):
        # The commands in the input are not 0 indexed so we need to add 1
        for _ in range(0, amount):
            i = self.board[frm - 1].pop()
            self.board[to - 1].append(i)

    def move_new(self, amount: int, frm: int, to: int):
        split = len(self.board[frm - 1]) - amount
        swap = self.board[frm - 1][split:]
        self.board[frm - 1] = self.board[frm - 1][:split]
        self.board[to - 1].extend(swap)

    def read(self):
        return "".join([x[-1] for x in self.board])


if __name__ == "__main__":
    test_sections = test_case.split("\n\n")
    # Test part 1
    game = Game(test_sections[0])
    game.playall(test_sections[1])
    print(game.read())
    assert game.read() == "CMZ"

    # Test part 2
    game = Game(test_sections[0])
    game.playalltwo(test_sections[1])
    print(game.read())
    assert game.read() == "MCD"

    with open("day5/input.txt") as file:
        lines = file.read().split("\n\n")
        game = Game(lines[0])
        game.playall(lines[1])
        print(game.read())

        game = Game(lines[0])
        game.playalltwo(lines[1])
        print(game.read())
