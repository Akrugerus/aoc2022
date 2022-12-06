def day1():
    with open("day1/input.txt", "r") as file:
        largest = -1
        placeholder = 0
        for line in file.readlines():
            if line != "\n":
                placeholder += int(line.strip())
            else:
                if placeholder > largest:
                    largest = placeholder
                placeholder = 0
        print(largest)


def day1pt2():
    values = []
    with open("day1/input.txt", "r") as file:
        for section in file.read().strip().split("\n\n"):
            total = sum(int(x) for x in section.split("\n"))
            values.append(total)
    values = sorted(values)[-3:]
    print(sum(values))


if __name__ == "__main__":
    day1()
    day1pt2()
