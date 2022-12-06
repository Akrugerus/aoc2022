test_case = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def overlapping(line: str):
    rone, rtwo = line_to_set(line)
    if len(rone.intersection(rtwo)) != 0:
        return True
    return False


def contains(line: str):
    rone, rtwo = line_to_set(line)
    if rone.issubset(rtwo) or rtwo.issubset(rone):
        return True
    return False


def line_to_set(line):
    s = line.split(",")
    one = s[0].split("-")
    rone = set(list(range(int(one[0]), int(one[1]) + 1)))
    two = s[1].split("-")
    rtwo = set(list(range(int(two[0]), int(two[1]) + 1)))
    return rone, rtwo


if __name__ == "__main__":
    test_lines = [line for line in test_case.split("\n")]
    assert sum(map(contains, test_lines)) == 2
    assert sum(map(overlapping, test_lines)) == 4
    with open("day4/input.txt") as file:
        lines = file.read().strip().split("\n")
        print(sum(map(contains, lines)))
        print(sum(map(overlapping, lines)))
