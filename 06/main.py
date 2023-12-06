import re


class Race:
    time: int
    record_distance: int

    def __init__(self, time: int, record_distance: int):
        self.time = time
        self.record_distance = record_distance

    def __repr__(self):
        return f"Race: {self.time=} {self.record_distance=}"

    def get_distance_traveled(self, time: int) -> 0:
        if time == 0 or time == self.time:
            return 0

        speed = time
        time_to_move = self.time - time

        return time_to_move * speed

    def get_winning_times(self) -> list[int]:
        winning_times = []
        for time in range(self.time):
            distance = self.get_distance_traveled(time)

            if distance > self.record_distance:
                winning_times.append(time)

        return winning_times


def read_input() -> list[str]:
    with open('input.txt') as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def parse_number_line(line: str) -> list[int]:
    return [int(num) for num in re.findall(r'\d+', line)]


def main():
    lines = read_input()

    times = parse_number_line(lines[0])
    record_distances = parse_number_line(lines[1])

    product_number_winning_times = 1

    for time, record_distance in zip(times, record_distances):
        race = Race(time, record_distance)
        product_number_winning_times *= len(race.get_winning_times())

    print(f'Product of the number of ways to win each race: {product_number_winning_times}')


if __name__ == '__main__':
    main()
