test_case = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class File:
    def __init__(self, size, name):
        self._name = name
        self._size = int(size)

    @property
    def size(self):
        return self._size

    @property
    def name(self):
        return self._name

    def __str__(self) -> str:
        return f"{self._size} {self._name}"

    def __repr__(self):
        return str(self)


class Dir:
    def __init__(self, name, parent=None) -> None:
        self.name = name
        self._children: list[Dir | File] = list()
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return [c for c in self._children]

    def add_child(self, child):
        self._children.append(child)

    @property
    def size(self):
        return sum([c.size for c in self._children])

    # Returns all children of self that are of type Dir, including subchildren
    def dirs(self) -> list:
        out = []
        for c in self._children:
            if isinstance(c, Dir):
                out.append(c)
                out.extend(c.dirs())

        return out

    # Find returns a child item from a given string by matching the name field
    def find(self, name):
        for c in self._children:
            if c.name == name:
                return c
        raise Exception(f"Unable to find {name}")

    def __str__(self) -> str:
        return f"{self.name} {[c.name for c in self._children]}"

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        return self.size < other.size


class Day7Runner:
    head: Dir

    def __init__(self, body):
        self.head = Dir("/")
        for line in body.split("\n"):
            self.line_feed(line)

    def line_feed(self, line):
        # If the line starts with a $, interpret the line as a command
        if line.startswith("$"):
            self.command(line)
        # This is a cheat because the only command output is from ls
        else:
            self.extend(line)

    def command(self, cmd):
        if cmd.split(" ")[1] == "cd":
            self.cd(cmd.split(" ")[2])

    def cd(self, dir):
        if dir == "..":
            # I love santized input!
            self.head = self.head.parent
        elif dir == "/":
            pass
        else:
            # I am choosing to ignore this error because my input is guaranteed to never try to cd into a file!
            # If only i was so smart!
            self.head = self.head.find(dir)

    def extend(self, child):
        if child.startswith("dir"):
            self.head.add_child(Dir(child.split(" ")[1], parent=self.head))
        else:
            self.head.add_child(File(child.split(" ")[0], child.split(" ")[1]))

    # Rewind the head back to root
    def rewind(self):
        while self.head.parent is not None:
            self.head = self.head.parent

    # Given a checking function, return elements in the tree
    def find(self, check):
        self.rewind()
        return filter(check, self.head.dirs())


test = Day7Runner(test_case)
f = [d for d in test.find(lambda x: x.size < 100000)]
assert sum([d.size for d in f]) == 95437
print(sum([d.size for d in f]))

with open("day7/input.txt", "r") as file:
    d7 = Day7Runner(file.read())
    print(sum([d.size for d in d7.find(lambda x: x.size < 100_000)]))
    current_space = 70_000_000 - d7.head.size
    delta_space = 30_000_000 - current_space
    print(min(d7.find(lambda x: x.size >= delta_space)).size)
