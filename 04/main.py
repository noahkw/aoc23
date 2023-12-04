import re


def read_input() -> list[str]:
    with open('input.txt') as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def parse_number_str(number_str: str) -> list[int]:
    number_regex = r"\d+"

    matches = re.findall(number_regex, number_str)
    return [int(num) for num in matches]


class ScratchCard:
    winning_numbers: set[int]
    scratched_numbers: set[int]
    id: int

    def __str__(self):
        return (f"Card {self.id}: {' '.join([str(n) for n in self.winning_numbers])} "
                f"| {' '.join([str(n) for n in self.scratched_numbers])} --> Value: {self.value()}")

    def value(self) -> int:
        winners = self.winning_numbers.intersection(self.scratched_numbers)

        return 0 if len(winners) == 0 else 2 ** (len(winners) - 1)

    @staticmethod
    def parse(line: str) -> 'ScratchCard':
        scratch_card = ScratchCard()

        tokens = line.strip().split(':')
        scratch_card.id = int(tokens[0][5:])

        lists = tokens[1].split('|')

        scratch_card.winning_numbers = set(parse_number_str(lists[0]))
        scratch_card.scratched_numbers = set(parse_number_str(lists[1]))

        return scratch_card


def main():
    lines = read_input()

    sum_of_points = 0

    for line in lines:
        scratch_card = ScratchCard.parse(line)
        print(scratch_card)
        sum_of_points += scratch_card.value()

    print(f"Sum of points: {sum_of_points}")


if __name__ == '__main__':
    main()
