test_case = open("day10/test.txt", "r").read()

# TODO cpu print to crt does not line up correctly


class CPU:
    def __init__(self):
        self.register: int = 1
        self.cycle_count = 0
        self.crt = ""

        self.sig_reg = 0
        self.sig_reg_triggers = list()

    def addx(self, V):
        # costs 2 cycles
        self.cycle()
        self.cycle()
        # add V to register
        self.register += V

    def noop(self):
        self.cycle()

    def cycle(self):
        self.print()
        self.cycle_count += 1
        self.handle_sig_reg()

    def handle_sig_reg(self):
        for r in self.sig_reg_triggers:
            if r(self):
                self.sig_reg += self.signal_strength
                print(self)

    def print(self):
        self.crt += self.current_character
        if self.cycle_count == 0:
            return
        if self.cycle_count % 40 == 0:
            self.crt += "\n"
        if self.cycle_count % 240 == 0:
            self.crt += "\n"

    def register_sig_trigger(self, trigger):
        self.sig_reg_triggers.append(trigger)

    @property
    def sprite_visible(self):
        # sprite is 3 characters wide
        # if the register is between current position -1 and current position +1 return true
        return (
            (self.cycle_count % 40 + 1) >= self.register >= (self.cycle_count % 40 - 1)
        )

    @property
    def signal_strength(self):
        return self.register * self.cycle_count

    @property
    def current_character(self) -> str:
        return "#" if self.sprite_visible else "."

    def __repr__(self):
        return f"V register: {self.register}, Cycle count: {self.cycle_count}"


class Day10Runner:
    def __init__(self, page):
        self.cpu = CPU()
        self.cpu.register_sig_trigger(
            lambda x: x.cycle_count in (20, 60, 100, 140, 180, 220)
        )
        for line in page.split("\n"):
            self.line_feed(line)

    def line_feed(self, line):
        if line == "noop":
            self.cpu.noop()
        elif line.startswith("addx"):
            self.cpu.addx(int(line.split(" ")[1]))


if __name__ == "__main__":
    test = Day10Runner(test_case)
    assert test.cpu.sig_reg == 13140
    print(test.cpu.crt)
    with open("day10/input.txt", "r") as file:
        day10 = Day10Runner(file.read())
        print(day10.cpu.sig_reg)
        print(day10.cpu.crt)
