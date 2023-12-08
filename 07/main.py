import abc
from collections import Counter
from functools import total_ordering


@total_ordering
class Card:
    value: int
    label: str

    def __init__(self, value: int, label: str):
        self.value = value
        self.label = label

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return self.label

    @staticmethod
    def from_label(label: str):
        if label == 'A':
            return Card(14, label)
        elif label == 'K':
            return Card(13, label)
        elif label == 'Q':
            return Card(12, label)
        elif label == 'J':
            return Card(11, label)
        elif label == 'T':
            return Card(10, label)
        else:
            val = int(label)

            assert val in range(2, 9 + 1)

            return Card(val, label)

    def __lt__(self, other: 'Card'):
        return self.value < other.value

    def __eq__(self, other: 'Card'):
        return self.value == other.value


class Hand:
    cards: list[Card]
    bid: int

    def __init__(self, cards: list[Card], bid: int):
        self.cards = cards
        self.bid = bid

    def __repr__(self):
        return ''.join(str(card) for card in self.cards) + f' {self.bid}'

    def evaluate_hand_strength(self, evaluators: list['HandEvaluator']) -> int:
        for evaluator in evaluators:
            result = evaluator.evaluate(self)

            if result is not None:
                return result

        assert False, f'The hand "{self}" evaluates to nothing? unlucky'

    def __eq__(self, other: 'Hand') -> bool:
        for card, other_card in zip(self.cards, other.cards):
            if card != other_card:
                return False

        return True

    def __lt__(self, other: 'Hand') -> bool:
        for card, other_card in zip(self.cards, other.cards):
            if card == other_card:
                continue

            return card < other_card

    @staticmethod
    def from_str(s: str, bid: int):
        assert len(s) == 5
        hand = Hand([Card.from_label(label) for label in s], bid)
        return hand


class HandEvaluator(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, hand: Hand) -> int:
        pass


class FiveOfAKind(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        return 6 if len(set(hand.cards)) == 1 else None


class FourOfAKind(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        counter = Counter(hand.cards)
        most_common_card, most_common_card_amount = counter.most_common()[0]
        return 5 if most_common_card_amount == 4 else None


class FullHouse(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        counter = Counter(hand.cards)
        most_common_card, most_common_card_amount = counter.most_common()[0]
        second_most_common_card, second_most_common_card_amount = counter.most_common()[1]
        return 4 if most_common_card_amount == 3 and second_most_common_card_amount == 2 else None


class ThreeOfAKind(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        counter = Counter(hand.cards)
        most_common_card, most_common_card_amount = counter.most_common()[0]
        return 3 if most_common_card_amount == 3 else None


class TwoPair(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        counter = Counter(hand.cards)
        most_common_card, most_common_card_amount = counter.most_common()[0]
        second_most_common_card, second_most_common_card_amount = counter.most_common()[1]
        return 2 if most_common_card_amount == 2 and second_most_common_card_amount == 2 else None


class OnePair(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        counter = Counter(hand.cards)
        most_common_card, most_common_card_amount = counter.most_common()[0]
        return 1 if most_common_card_amount == 2 else None


class Nothing(HandEvaluator):
    def evaluate(self, hand: Hand) -> int:
        return 0


def read_input() -> list[str]:
    with open('input.txt') as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def main():
    evaluators = [FiveOfAKind(), FourOfAKind(), FullHouse(), ThreeOfAKind(), TwoPair(), OnePair(), Nothing()]
    lines = read_input()
    hands = []

    for line in lines:
        tokens = line.split(' ')
        assert len(tokens) == 2

        cards, bid = tokens
        hands.append(Hand.from_str(cards, int(bid)))

    hand_buckets: dict[int, list[Hand]] = {k: [] for k in range(len(evaluators))}

    for hand in hands:
        hand_buckets[hand.evaluate_hand_strength(evaluators)].append(hand)

    total_order = []

    for hand_bucket in reversed(hand_buckets.values()):
        sorted_within_bucket = sorted(hand_bucket, reverse=True)
        total_order.extend(sorted_within_bucket)

    winnings = 0

    for idx, hand in enumerate(total_order):
        rank = len(total_order) - idx
        winnings += rank * hand.bid

    print(f'Total winnings: {winnings}')


if __name__ == '__main__':
    main()
