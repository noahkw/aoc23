adjacent_char_offets = [[-1, -1], [-1, 0], [-1, 1],
                        [0, -1], [0, 1],
                        [1, -1], [1, 0], [1, 1]]


def is_special_char(c: str) -> bool:
    return not c.isnumeric() and c != '.'


def read_input() -> list[str]:
    with open('input.txt') as f:
        lines = f.readlines()

    return [line.strip() for line in lines]


def has_adjacent_special_char(lines: list[str], line_index: int, char_index: int) -> bool:
    line_limit = len(lines)
    char_limit = len(lines[0])

    for offset in adjacent_char_offets:
        new_line_index = line_index + offset[0]
        new_char_index = char_index + offset[1]

        if new_line_index < 0 \
                or new_line_index >= line_limit \
                or new_char_index < 0 \
                or new_char_index >= char_limit:
            continue

        if is_special_char(lines[new_line_index][new_char_index]):
            return True

    return False


def get_decimal_place(line: str, char_index: int):
    places = 0

    for c in line[char_index + 1:]:
        if c.isnumeric():
            places += 1
        else:
            break

    return places


def has_right_neighbor_digit_with_adjacent_special_char(lines: list[str], line_index: int, char_index: int):
    line = lines[line_index]

    for idx, c in enumerate(line[char_index + 1:]):
        if not c.isnumeric():
            break

        if has_adjacent_special_char(lines, line_index, char_index + idx + 1):
            return True

    return False


def main():
    lines = read_input()

    sum_ = 0
    previous_char_relevant = False

    for line_index, line in enumerate(lines):
        for char_index, c in enumerate(line):
            print(f'line={line_index} char={char_index} c={c}'
                  f' has_adjacent_special_char={has_adjacent_special_char(lines, line_index, char_index)}'
                  f' decimal_place={get_decimal_place(line, char_index)}'
                  f' has_right_neighbor_digit_with_adjacent_special_char={has_right_neighbor_digit_with_adjacent_special_char(lines, line_index, char_index)}')

            if c.isnumeric() and (has_adjacent_special_char(lines, line_index, char_index)
                                  or has_right_neighbor_digit_with_adjacent_special_char(lines, line_index,
                                                                                         char_index)
                                  or previous_char_relevant):

                decimal_place = get_decimal_place(line, char_index)
                sum_ += int(c) * (10 ** decimal_place)
                previous_char_relevant = True
            else:
                previous_char_relevant = False

    print(sum_)


if __name__ == '__main__':
    main()
