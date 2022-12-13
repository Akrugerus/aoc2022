class Item:
    def __init__(self, value):
        self._value: int = value

    @property
    def val(self):
        return self._value

    @val.setter
    def val(self, v):
        self._value = v

    def decrease_worry(self):
        # print(f"decreasing worry from {self.val}")
        self._value = self._value // 3
        # print(f"to {self.val}")

    def op(self, op_str: str):
        op = op_str
        if "old" in op:
            op = op.replace("old", "self.val")
        # print(f"inspecting item with worry level {self.val}")
        self.val = eval(op)
        # print(f"using {op} moves worry to {self.val}")

    def __repr__(self) -> str:
        return str(self.val)


class Monkey:
    def __init__(
        self, items_list: str, op, test: int, true: int, false: int, debug=False
    ):
        self.items: list[Item] = self.parse_items(items_list)
        self.op_str = op.strip()
        self.divisor = test
        self.true = true
        self.false = false
        self.total_inspected = 0
        self.debug = debug

    def parse_items(self, text) -> list[Item]:
        return list(map(Item, map(int, text.split(","))))

    # def operate(self, old: Item) -> Item:
    #     self.total_inspected += 1
    #     if "old * old" in self.op_str and self.debug:
    #         print(self.debug)
    #         print(old)
    #     return eval(self.op_str)

    def test(self, i: int) -> bool:
        # print(
        #     f"{i} {'is' if i % self.divisor == 0 else 'is not'  } divisible by {self.divisor}"
        # )
        return i % self.divisor == 0

    def take_turn(self) -> dict[int, list]:
        out_dict: dict[int, list[Item]] = {}
        for i in self.items:
            # apply operation to item
            self.total_inspected += 1
            i.op(self.op_str)
            # decrease worry level
            i.decrease_worry()
            dst = self.find_dest(i.val)
            if not out_dict.get(dst, None):
                out_dict[dst] = [i]
            else:
                out_dict[dst].append(i)
        self.items = []
        return out_dict

    def find_dest(self, i: int) -> int:
        return self.true if self.test(i) else self.false

    def __repr__(self) -> str:
        return f"total={self.total_inspected}, items={self.items}"


class Day11Runner:
    monkeys: list[Monkey] = list()

    def __init__(self, page, debug=False):
        self._turns = 0
        for monke in page.split("\n\n"):
            self.monkeys.append(self.monkey_feed(monke, debug))

    def monkey_feed(self, monkey_blob: str, debug) -> Monkey:
        lines = monkey_blob.split("\n")
        return Monkey(
            items_list=lines[1].split(":")[1],
            op=lines[2].split("=")[1],
            test=int(lines[3].split(" ")[-1]),
            true=int(lines[4].split(" ")[-1]),
            false=int(lines[5].split(" ")[-1]),
            debug=debug,
        )

    def play(self, turns):
        for _ in range(turns):
            self.round()

    def round(self):
        for monkey in self.monkeys:
            results = monkey.take_turn()
            self.move(results)
        print(self.monkeys)

    def move(self, move_dict: dict[int, list]):
        for key in move_dict.keys():
            self.monkeys[key].items.extend(move_dict[key])

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
        test = Day11Runner(file.read(), debug=True)
        test.play(20)
        assert test.monkey_business == 10605
    with open("day11/input.txt", "r") as file:
        d11 = Day11Runner(file.read())
        items_start = d11.total_items
        d11.play(5)
        assert items_start == d11.total_items
        d11.play(5)
        d11.play(5)
        d11.play(5)
        print(d11.monkeys)
        print(d11.monkey_business)
