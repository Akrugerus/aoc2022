test_case = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

# Unicode values
# a = z: 97 - 122
# A - Z: 65 - 90


# use unicode and offset to map priorities
def priority(char) -> int:
    if ord(char) <= ord("Z"):
        return ord(char) - 38
    else:
        return ord(char) - 96


class backpack:
    def __init__(self, line):
        half: int = int(len(line) / 2)
        self.left_side = line[:half]
        self.right_side = line[half:]
        assert len(self.left_side) == len(self.right_side)

    def difference(self) -> str:
        i = set(self.left_side).intersection(set(self.right_side))
        return "".join(i)


def echo(a):
    print(a)
    return a


def intersecting_item(*args):
    return "".join(set.intersection(*map(set, *args)))


# Takes a list of bags in a group and returns the priority of the group item
def groupprio(group: list):
    return priority(intersecting_item(group))


def group_iterator(all_bags, group_size):
    for i in range(0, len(all_bags), group_size):
        yield [all_bags[i], all_bags[i + 1], all_bags[i + 2]]


if __name__ == "__main__":
    test_list = test_case.split("\n")
    assert sum([priority(backpack(line).difference()) for line in test_list]) == 157
    assert sum([groupprio(group) for group in group_iterator(test_list, 3)]) == 70

    with open("day3/input.txt", "r") as file:
        lines = file.read().strip().split("\n")
        print(sum([priority(backpack(line).difference()) for line in lines]))
        print(sum([groupprio(group) for group in group_iterator(lines, 3)]))
