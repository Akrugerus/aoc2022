test_case_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def generate_frames(input: str, step: int):
    for i in range(0, len(input) - step):
        yield i + step, input[i : i + step]


def find_frame_marker(input: str) -> int:
    for index, frame in generate_frames(input, 4):
        if len(frame) == len(set(frame)):
            return index
    return 0


def find_message_marker(input: str) -> int:
    for index, frame in generate_frames(input, 14):
        if len(frame) == len(set(frame)):
            return index
    return 0


if __name__ == "__main__":
    assert find_frame_marker(test_case_1) == 7
    assert find_message_marker(test_case_1) == 19
    with open("day6/input.txt") as file:
        input = file.read().strip()
        print(find_frame_marker(input))
        print(find_message_marker(input))
