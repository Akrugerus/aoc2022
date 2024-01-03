import enum
import json
from functools import cmp_to_key


class Status(enum.Enum):
    PASS = 0
    CONT = 1
    FAIL = 2


class Day13Runner:
    def __init__(self, lines):
        self.lines: str = lines

    def find_ordered_pairs(self):
        out = []
        for i, pair in enumerate(self.lines.split("\n\n")):
            left, right = pair.split("\n")
            left = json.loads(left)
            right = json.loads(right)
            comp = self.compare(left, right)
            if comp == Status.PASS:
                print(
                    f"Found correctly ordered pair {left} and {right} at index {i} "
                    f"so adding {i + 1}"
                )
                out.append(i + 1)
            elif comp == Status.CONT:
                raise Exception("Cannot exit with CONT status")
        return out

    def compare(self, left, right) -> Status:
        # Rule 1
        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                return Status.CONT
            elif left < right:
                print(f"{Status.PASS} {left} < {right}")
                return Status.PASS
            else:
                print(f"{Status.FAIL} {left} > {right}")
                return Status.FAIL

        # Rule 2
        elif isinstance(left, list) and isinstance(right, list):
            for i in range(len(left)):
                if i >= len(right):
                    print(f"{Status.FAIL} {left} > {right}")
                    return Status.FAIL
                comp = self.compare(left[i], right[i])
                if comp == Status.CONT:
                    continue
                else:
                    print(f"{comp} {left} {right}")
                    return comp
            if len(left) == len(right):
                return Status.CONT
            return Status.PASS

        # Rule 3
        elif isinstance(left, int):
            return self.compare([left], right)
        else:
            return self.compare(left, [right])

    def key_compare(self, x, y):
        comp = self.compare(x, y)
        if comp == Status.PASS:
            return -1
        return 1

    def sum_of_ordered_pairs(self):
        return sum(self.find_ordered_pairs())

    def sort_messages(self):
        lines = [
            json.loads(line.strip())
            for line in self.lines.split("\n")
            if line != "\n" and line != ""
        ]

        def comp(x, y):
            return self.key_compare(x, y)

        return sorted(lines, key=cmp_to_key(comp))

    def decoder_key(self):
        lines = self.sort_messages()
        one = lines.index([[2]]) + 1
        two = lines.index([[6]]) + 1
        return one * two


if __name__ == "__main__":
    with open("day13/test.txt", "r") as file:
        lines = file.read()
        test = Day13Runner(lines)
        assert test.sum_of_ordered_pairs() == 13

    with open("day13/input.txt", "r") as file:
        lines = file.read()
        runner = Day13Runner(lines)
        print(f"Sum of ordered pairs: {runner.sum_of_ordered_pairs()}")

    with open("day13/test.txt", "r") as file, open("day13/test2.txt", "r") as result:
        lines = file.read()
        lines += "\n[[2]]\n[[6]]"
        test = Day13Runner(lines)
        assert test.sort_messages() == [json.loads(line.strip()) for line in result]
        assert test.decoder_key() == 140

    with open("day13/input.txt", "r") as file:
        lines = file.read()
        lines += "\n[[2]]\n[[6]]"
        runner = Day13Runner(lines)
        print(f"Decoder key: {runner.decoder_key()}")
