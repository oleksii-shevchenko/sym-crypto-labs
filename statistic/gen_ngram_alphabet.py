# Oleksii Shevchenko

import sys


def gen_bigram_alphabet(path: str, bigram_alphabet: str):
    write_alphabet(bigram_alphabet, gen_alphabet(load_source(path).split(" ")))


def write_alphabet(path: str, alphabet: list):
    file = open(path, 'w')
    for x in alphabet:
        file.write(x + " ")
    file.close()


def gen_alphabet(letters: list) -> list:
    bigram = list()
    for i in range(len(letters)):
        for j in range(len(letters)):
            bigram.append(letters[i] + letters[j])
    return bigram


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


if __name__ == "__main__":
    gen_bigram_alphabet(str(sys.argv[1]), str(sys.argv[2]))