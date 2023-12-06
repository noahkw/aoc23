import re


def read_input() -> list[str]:
    with open('input.txt') as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def parse_number_line(line: str) -> list[int]:
    return [int(num) for num in re.findall(r'\d+', line)]


class NumberMapEntry:
    dest_range_start: int
    source_range_start: int
    range_len: int

    def __init__(self, dest_range_start: int, source_range_start: int, range_len: int):
        self.dest_range_start = dest_range_start
        self.source_range_start = source_range_start
        self.range_len = range_len

    def map_number(self, num: int) -> int | None:
        r = range(self.source_range_start, self.source_range_start + self.range_len)

        if num not in r:
            return None

        diff = abs(num - self.source_range_start)
        return self.dest_range_start + diff

    @staticmethod
    def parse(line: str):
        numbers = parse_number_line(line)
        assert len(numbers) == 3

        return NumberMapEntry(*numbers)

    def __str__(self):
        return f'{self.dest_range_start} {self.source_range_start} {self.range_len}'


class NumberMap:
    entries: list[NumberMapEntry]

    def __init__(self):
        self.entries = []

    @staticmethod
    def parse(lines: list[str]):
        number_map = NumberMap()

        for line in lines[1:]:
            assert line.replace(' ', '').isnumeric()

            number_map.entries.append(NumberMapEntry.parse(line))

        return number_map

    def map_number(self, num: int) -> int:
        val = None
        for entry in self.entries:
            val = entry.map_number(num) or val

        return val or num

    def __str__(self):
        return "\n".join([str(entry) for entry in self.entries])


def parse_seeds(line: str) -> list[range]:
    seeds = parse_number_line(line)
    seed_ranges = []

    for start, length in zip(seeds[0::2], seeds[1::2]):
        seed_ranges.append(range(start, start + length))

    return seed_ranges


def main():
    lines = read_input()

    seeds_ranges = parse_seeds(lines[0])
    print(f"Starting seeds: {seeds_ranges}")

    maps: list[NumberMap] = []

    grouped_lines: list[list[str]] = [[]]
    current_idx = -1

    for line in lines[1:]:
        if len(line) == 0:
            current_idx += 1
            grouped_lines.append([])
            continue

        grouped_lines[current_idx].append(line)

    for group in grouped_lines:
        if len(group) == 0:
            continue

        maps.append(NumberMap.parse(group))

    print('\n\n'.join(str(map) for map in maps))

    print('\n\n')

    assert len(maps) == 7

    seeds_out = []

    for seed_range in seeds_ranges:
        for seed in seed_range:
            seed_out = seed

            for idx, map in enumerate(maps):
                print(f'seed map {idx}, {seed_out}')
                seed_out = map.map_number(seed_out)

            seeds_out.append(seed_out)

    print(f'Seeds out: {seeds_out}, Result: {min(seeds_out)}')

if __name__ == '__main__':
    main()