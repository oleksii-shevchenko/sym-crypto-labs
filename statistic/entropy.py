# Oleksii Shevchenko

import sys
import math


def entropy(resource: str, alphabet: str, result: str, probability: str, n: int):
    letters = load_source(alphabet).split(" ")
    data = load_source(resource)

    table = compute_frequency(init_table(letters), data, n)
    frequency = normalize_table(table, (len(data) - n + 1))

    h = compute_entropy(frequency, n)
    r = compute_redundancy(h, len(letters))

    write_table(probability, frequency)

    file = open(result, 'w')
    file.write("H = " + str(h) + "\n")
    file.write("R = " + str(r) + "\n")
    file.close()


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


def init_table(keys: list) -> dict:
    table = dict()
    for x in keys:
        table[x] = 0
    return table


def compute_frequency(table: dict, data: str, shift: int) -> dict :
    for y in range(1, len(data) - shift + 1):
        table[data[y:y + shift]] += 1
    return table


def normalize_table(table: dict, size: int) -> dict :
    probability = dict()
    for x in table.keys():
        probability[x] = float(table[x]) / size
    return probability


def compute_entropy(frequency: dict, ngram: int) -> float :
    h = 0.0
    for x in frequency.keys():
        if frequency[x] != 0.0:
            h += h - frequency[x] * math.log2(frequency[x])
    return h / ngram


def write_table(path: str, table: dict):
    file = open(path, 'w')
    for x in table.keys():
        file.write("[key = %s, value = %s]%n".format(x, table[x]))
    file.close()


def compute_redundancy(h: float, size: int) -> float:
    return 1 - h / math.log2(size)


if __name__ == "__main__":
    entropy(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), int(sys.argv[5]))