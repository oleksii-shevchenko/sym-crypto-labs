# Oleksii Shevchenko

import sys


def vigenere_encryption(message: str, cipher_text: str, key: str):
    dictionary = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9,
                  'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18,
                  'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27,
                  'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

    plain_text = load_source(message)

    file = open(cipher_text, 'w', encoding="utf8")
    for x in range(len(plain_text)):
        file.write(letters[(dictionary[plain_text[x]] + dictionary[key[x % len(key)]]) % len(letters)])
    file.close()


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


if __name__ == "__main__":
    vigenere_encryption(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))