import math


class Monkey:
    def __init__(self, items_list: list[int], op, test: int, true: int, false: int):
        self.items = items_list
        self.op = op
        self.divisor = test
        self.true = true
        self.false = false
        self.total_inspected = 0

    def __repr__(self) -> str:
        return f"total={self.total_inspected}, items={self.items}"


class Day11Runner:
    def __init__(self, page):
        self.monkeys: list[Monkey] = list()
        self._turns = 0
        for monke in page.split("\n\n"):
            self.monkeys.append(self.monkey_feed(monke))

    def monkey_feed(self, monkey_blob: str) -> Monkey:
        lines = monkey_blob.split("\n")
        return Monkey(
            items_list=list(map(int, lines[1].split(":")[1].split(","))),
            op=lambda old, op=lines[2].split("=")[1]: eval(op),
            test=int(lines[3].split(" ")[-1]),
            true=int(lines[4].split(" ")[-1]),
            false=int(lines[5].split(" ")[-1]),
        )

    def play(self, turns):
        for _ in range(turns):
            for monkey in self.monkeys:
                for i in monkey.items:
                    # apply operation to item
                    monkey.total_inspected += 1
                    i = monkey.op(i)
                    # decrease worry level
                    i = i // 3
                    if i % monkey.divisor == 0:
                        self.monkeys[monkey.true].items.append(i)
                    else:
                        self.monkeys[monkey.false].items.append(i)
                monkey.items = []

    @property
    def lcm(self):
        return math.lcm(*[monk.divisor for monk in self.monkeys])

    def play_pt2(self, turns):
        # find lcm to reduce numbers as theyre generated
        lcm = math.lcm(*[monk.divisor for monk in self.monkeys])
        for _ in range(turns):
            for monkey in self.monkeys:
                for i in monkey.items:
                    # apply operation to item
                    monkey.total_inspected += 1
                    i = monkey.op(i)
                    # reduce
                    i = i % lcm
                    if i % monkey.divisor == 0:
                        self.monkeys[monkey.true].items.append(i)
                    else:
                        self.monkeys[monkey.false].items.append(i)
                monkey.items = []

    @property
    def monkey_business(self) -> int:
        s = sorted(self.monkeys, key=lambda x: x.total_inspected)
        print(s)
        return s[-2].total_inspected * s[-1].total_inspected

    @property
    def total_items(self):
        return sum(len(x.items) for x in self.monkeys)


if __name__ == "__main__":
    with open("day11/test.txt", "r") as file:
        page = file.read()
        test = Day11Runner(page)
        test.play(20)
        assert test.monkey_business == 10605
        testpt2 = Day11Runner(page)
        testpt2.play_pt2(10000)
        assert testpt2.monkey_business == 2713310158
    with open("day11/input.txt", "r") as file:
        page = file.read()
        d11 = Day11Runner(page)
        d11.play(20)
        print(d11.monkey_business)
        d11pt2 = Day11Runner(page)
        d11pt2.play_pt2(10000)
        print(d11pt2.lcm)
        print(d11pt2.monkey_business)
