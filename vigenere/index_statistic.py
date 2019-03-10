# Oleksii Shevchenko

import sys


def statistic(text_model: str, info: str):
    text = clean(load_source(text_model))

    write_data("clean_text.txt", text)

    file = open(info, 'w')
    file.write("Plain text: MI = " + str(sqr_mean(list(compute_frequency(text).values()))) + "\n")
    for x in range(2, 30):
        file.write("Key length " + str(x) + ": MI = " + str(sqr_mean(list(compute_frequency(vigenere_direct_encryption(text, text[0:x])).values()))) + "\n")
    file.close()


def sqr_mean(values: list) -> float:
    res = 0.0
    for x in values:
        res += (x ** 2)
    return res / len(values)


def compute_frequency(text: str) -> dict:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    table = dict()
    for x in range(len(letters)):
        table[x] = (float(text.count(letters[x]))) / len(text)
    return table


def clean(text: str) -> str:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    res = ""
    for x in range(len(text)):
        if text[x] in letters:
            res += text[x]
    return res


def vigenere_direct_encryption(message: str, key: str) -> str:
    dictionary = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9,
                  'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18,
                  'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27,
                  'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    cipher_text = ""
    for x in range(len(message)):
        cipher_text = cipher_text + letters[(dictionary[message[x]] + dictionary[key[x % len(key)]]) % len(letters)]
    return cipher_text


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


def write_data(path: str, data: str) :
    file = open(path, 'w', encoding="utf8")
    file.write(data)
    file.close()


if __name__ == "__main__":
    statistic(str(sys.argv[1]), str(sys.argv[2]))