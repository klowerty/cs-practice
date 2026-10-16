import sys

from stats import average_by_city, read_valid, warmest_city


def main() -> None:
    lines = sys.stdin.read().splitlines()
    non_empty = [line for line in lines if line.strip()]
    records = read_valid(non_empty)
    print(len(records))
    print(len(non_empty) - len(records))
    best = warmest_city(records)
    print(f"{average_by_city(records)[best]:.1f}" if best else "0.0")


if __name__ == "__main__":
    main()