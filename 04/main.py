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
        return (f"Card {self.id}: {' '.join([str(n) for n in self.winning_numbers])}"
                f" | {' '.join([str(n) for n in self.scratched_numbers])} --> Value: {self.value()},"
                f" Number winners: {self.number_winners()}")

    def winners(self) -> set[int]:
        return self.winning_numbers.intersection(self.scratched_numbers)

    def value(self) -> int:
        winners = self.winners()

        return 0 if len(winners) == 0 else 2 ** (len(winners) - 1)

    def number_winners(self) -> int:
        return len(self.winners())

    @staticmethod
    def parse(line: str) -> 'ScratchCard':
        scratch_card = ScratchCard()

        tokens = line.strip().split(':')
        scratch_card.id = int(tokens[0][5:])

        lists = tokens[1].split('|')

        scratch_card.winning_numbers = set(parse_number_str(lists[0]))
        scratch_card.scratched_numbers = set(parse_number_str(lists[1]))

        return scratch_card


class Scratcher:
    cards: list[ScratchCard]
    card_amounts: dict[int, int] = dict()

    def __init__(self, cards: list[ScratchCard]):
        self.cards = cards

    def run(self):
        for card in self.cards:
            self.card_amounts[card.id] = 1

        for card in self.cards:
            card_amount = self.card_amounts[card.id]

            for i in range(card.number_winners()):
                self.card_amounts[card.id + i + 1] += card_amount

        total_cards = sum(self.card_amounts.values())
        print(f"Amount of cards: {total_cards}")


def main():
    lines = read_input()

    sum_of_points = 0
    cards = []

    for line in lines:
        scratch_card = ScratchCard.parse(line)
        cards.append(scratch_card)
        print(scratch_card)
        sum_of_points += scratch_card.value()

    print(f"Sum of points: {sum_of_points}")

    scratcher = Scratcher(cards)
    scratcher.run()


if __name__ == '__main__':
    main()
