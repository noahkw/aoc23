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

    def __index__(self):
        return self.value

    @staticmethod
    def from_label(label: str):
        if label == 'A':
            return Card(14, label)
        elif label == 'K':
            return Card(13, label)
        elif label == 'Q':
            return Card(12, label)
        elif label == 'J':
            return Card(1, label)
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


CARDS_WITHOUT_JOKER = [
                          Card.from_label('A'),
                          Card.from_label('K'),
                          Card.from_label('Q'),
                          Card.from_label('T'),
                      ] + [Card.from_label(str(val)) for val in range(2, 9 + 1)]


def resolve_first_joker(hand: 'Hand') -> list['Hand']:
    possible_hands: list['Hand'] = []

    for idx, card in enumerate(hand.cards):
        if card.value != 1:
            continue

        for c in CARDS_WITHOUT_JOKER:
            new_hand = Hand(hand.cards[:], hand.bid)
            new_hand.cards[idx] = c
            possible_hands.append(new_hand)

        break

    return possible_hands


class Hand:
    cards: list[Card]
    bid: int

    def __init__(self, cards: list[Card], bid: int):
        self.cards = cards
        self.bid = bid

    def __repr__(self):
        return ''.join(str(card) for card in self.cards) + f' {self.bid}'

    def number_jokers(self) -> int:
        return sum(1 for card in self.cards if card.value == 1)

    def generate_possible_hands(self) -> list['Hand']:
        possible_hands: list['Hand'] = [self]

        for _ in range(self.number_jokers()):
            for hand in possible_hands:
                new_hands = resolve_first_joker(hand)
                possible_hands.extend(new_hands)

        return possible_hands

    def evaluate_hand_strength(self, evaluators: list['HandEvaluator']) -> int:
        if Card.from_label('J') in self.cards:
            # shortcut for very jokery hands
            if evaluators[0].evaluate(self) or self.cards.count(Card.from_label('J')) == 4:
                # five of a kind with jokers
                # four of a kind with jokers becomes a five of a kind too
                return 6

            hands = self.generate_possible_hands()
            return max(hand.evaluate_single_hand(evaluators) for hand in hands)

        return self.evaluate_single_hand(evaluators)

    def evaluate_single_hand(self, evaluators: list['HandEvaluator']) -> int:
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
        hand_strength = hand.evaluate_hand_strength(evaluators)
        print(f'{hand}, strength: {hand_strength}')
        hand_buckets[hand_strength].append(hand)

    total_order = []

    for hand_bucket in reversed(hand_buckets.values()):
        sorted_within_bucket = sorted(hand_bucket, reverse=True)
        total_order.extend(sorted_within_bucket)

    winnings = 0

    for idx, hand in enumerate(total_order):
        rank = len(total_order) - idx
        print(f'{hand}, Rank: {rank}')
        winnings += rank * hand.bid

    print(f'Total winnings: {winnings}')


if __name__ == '__main__':
    main()
