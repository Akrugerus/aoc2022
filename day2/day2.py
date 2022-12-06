# The winner of the whole tournament is the player with the highest score.
# Your total score is the sum of your scores for each round.
# The score for a single round is the score for the shape you selected (1 for Rock,
# 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost,
# 3 if the round was a draw, and 6 if you won).

# 1 = rock
# 2 = paper
# 3 = scissors

rps_one = {
    "X": 1,
    "Y": 2,
    "Z": 3,
    "A": 1,
    "B": 2,
    "C": 3,
}

rps_two = {
    "X": -1,
    "Y": 0,
    "Z": 1,
    "A": 1,
    "B": 2,
    "C": 3,
}

# Part 2
# X = offset of -1
# Y = offset of 0
# Z = offset of 1


def round_from_turn(turn) -> int:
    # Return score of round
    choice_value = rps_one[turn[2]]
    score_value = round_score(rps_one[turn[0]], rps_one[turn[2]])
    return choice_value + score_value


def round_from_result(turn) -> int:
    # Return score of round
    # Opponent choice value, plus offset given by desired result, mod 3 plus 3
    our_choice = ((rps_two[turn[0]] + rps_two[turn[2]] + 2) % 3) + 1
    print(our_choice)
    score_value = round_score(rps_two[turn[0]], our_choice)
    return our_choice + score_value


def round_score(pla, opp) -> int:
    return ((opp + 4 - pla) % 3) * 3


if __name__ == "__main__":
    with open("day2/input.txt", "r") as file:
        assert round_from_turn("A Y") == 8
        assert round_from_result("A Y") == 4
        assert round_from_result("B X") == 1
        assert round_from_result("C Z") == 7

        turns = file.read().strip().split("\n")
        scores = [round_from_turn(x) for x in turns]
        scores_pt2 = [round_from_result(x) for x in turns]

        print(len(scores))
        print(sum(scores))
        print(sum(scores_pt2))
