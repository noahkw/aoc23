import string

def main():
    with open('input.txt') as f:
        lines = f.readlines()

    sum_ = 0

    for line in lines:
        truncated_line = line.lstrip(string.ascii_lowercase)
        truncated_line = truncated_line.rstrip()
        truncated_line = truncated_line.rstrip(string.ascii_lowercase)

        # if len(truncated_line) < 1:
        #     continue

        first_digit = int(truncated_line[0])
        last_digit = int(truncated_line[-1])

        sum_ += first_digit * 10 + last_digit

    print(sum_)


if __name__ == '__main__':
    main()
