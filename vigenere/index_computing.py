# Oleksii Shevchenko

import sys


def index_computing(text: str, info: str):
    res = mean_index(load_source(text))

    file = open(info, 'w', encoding="utf8")
    for y in res.keys():
        file.write("[Block size " + str(y + 2) + "]: " + str(res[y]) + "\n")
    file.close()


def mean_index(cipher_text: str) -> dict:
    result = dict()
    for r in range(2, 30):
        mi = 0.0
        for x in range(int(len(cipher_text) / r)):
            t = cipher_text[r * x: r * (x + 1)]
            mi += index(t)
        mi = mi / (int(len(cipher_text) / r))
        result[r] = mi
    return result


def index(t: str) -> float:
    res = 0.0
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    for x in range(len(letters)):
        res += (t.count(letters[x]) * (t.count(letters[x]) - 1))
    res /= (len(t) * (len(t) - 1))
    return res


def vigenere_direct_encryption(message: str, key: str) -> str:
    dictionary = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9,
                  'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18,
                  'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27,
                  'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    cipher_text = str()
    for x in range(len(message)):
        cipher_text = cipher_text + letters[(dictionary[message[x]] + dictionary[key[x % len(key)]]) % len(letters)]
    return cipher_text


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


if __name__ == "__main__":
    index_computing(str(sys.argv[1]), str(sys.argv[2]))