import string


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    sum_ = 0

    for line in lines:
        truncated_line = truncate_line(line)

        first_digit = int(truncated_line[0])
        last_digit = int(truncated_line[-1])

        sum_ += first_digit * 10 + last_digit

    print(sum_)


def truncate_line(line):
    truncated_line = line.lstrip(string.ascii_lowercase)
    truncated_line = truncated_line.rstrip()
    truncated_line = truncated_line.rstrip(string.ascii_lowercase)
    return truncated_line


def main2():
    digit_map = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    with open('input.txt') as f:
        lines = f.readlines()

    sum_ = 0
    results = []

    for line in lines:
        parsed_line = line.rstrip()

        done = False
        for i, c in enumerate(parsed_line):
            current_substring = parsed_line[i:]

            if current_substring[0].isnumeric():
                break

            for key, value in digit_map.items():
                if current_substring.startswith(key):
                    parsed_line = parsed_line.replace(key, str(value), 1)
                    done = True
                    break

            if done:
                break

        reversed_parsed_line = parsed_line[::-1]

        for i, c in enumerate(reversed_parsed_line):
            current_substring = reversed_parsed_line[i:]

            if current_substring[0].isnumeric():
                break

            for key, value in digit_map.items():
                if current_substring.startswith(key[::-1]):
                    reversed_parsed_line = reversed_parsed_line.replace(key[::-1], str(value), 1)
                    break

        reversed_parsed_line = truncate_line(reversed_parsed_line)

        first_digit = int(reversed_parsed_line[-1])
        last_digit = int(reversed_parsed_line[0])
        print(f"'{line.rstrip()}' {first_digit * 10 + last_digit}")

        result = first_digit * 10 + last_digit
        results.append(str(result))

        sum_ += result

    print(sum_)

    with open('task2_results.txt', 'w') as f:
        f.write('\n'.join(results))


def compare():
    with open('task2_results.txt') as f:
        task2_results = f.readlines()

    with open('output.txt') as f:
        output = f.readlines()

    with open('input.txt') as f:
        input_ = f.readlines()

    for i, line in enumerate(task2_results):
        output_line = output[i]

        if line != output_line:
            print(f"{i} res:{line.rstrip()} maj:{output_line.rstrip()} in:{input_[i]}")


if __name__ == '__main__':
    main()
    main2()
    # compare()
