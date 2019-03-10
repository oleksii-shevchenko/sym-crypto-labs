# Oleksii Shevchenko

import sys


def compute_frequency(plain_text_model: str, frequency: str, bigram_frequency: str):
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

    text = cleaning(load_source(plain_text_model))

    frequency_table = normalize_table(compute_frequency_table(init_table(letters), text, 1), len(text))
    bigram_frequency_table = normalize_table(compute_frequency_table(init_table(gen_alphabet(letters)), text, 2), len(text) - 1)

    write_table_values(frequency_table, frequency)
    write_table_values(bigram_frequency_table, bigram_frequency)


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


def cleaning(text: str) -> str:
    text = text.lower()
    text = text.replace('ё', 'e')
    text = text.replace('ъ', 'ь')
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']
    result = ""
    for i in range(len(text)):
        if text[i] in letters:
            result += text[i]
    return result


def init_table(keys: list) -> dict:
    table = dict()
    for x in keys:
        table[x] = 0
    return table


def gen_alphabet(letters: list) -> list:
    bigram = list()
    for i in range(len(letters)):
        for j in range(len(letters)):
            bigram.append(letters[i] + letters[j])
    return bigram


def compute_frequency_table(table: dict, data: str, shift: int) -> dict:
    for y in range(1, len(data) - shift + 1):
        table[data[y:y + shift]] += 1
    return table


def normalize_table(table: dict, size: int) -> dict:
    probability = dict()
    for x in table.keys():
        probability[x] = float(table[x]) / size
    return probability


def write_table_values(table: dict, path: str):
    file = open(path, 'w', encoding="utf8")
    for x in table.values():
        file.write(x + " ")
    file.close()


if __name__ == "__main__":
    compute_frequency(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))