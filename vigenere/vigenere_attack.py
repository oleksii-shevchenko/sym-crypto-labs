# Oleksii Shevchenko

import sys


def vigenere_attack(cipher_text: str, message: str, info: str):
    text = clean(load_source(cipher_text))
    r = key_length(text, info)
    key = find_vigenere_cipher_key(text, r, info)
    write_data(message, vigenere_direct_dencryption(text, key))


def clean(text: str) -> str:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    res = ""
    for x in range(len(text)):
        if text[x] in letters:
            res += text[x]
    return res


def write_data(path: str, data: str):
    file = open(path, 'w', encoding="utf8")
    file.write(data)
    file.close()


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


def key_length(cipher_text: str, info: str) -> int:
    tol = 0.085
    u = 60
    D = []
    for x in range(2, u):
        n = 0.0
        for y in range(len(cipher_text) - u):
            if cipher_text[y] == cipher_text[y + x]:
                n += 1
        D.append(n / (len(cipher_text) - u))
    avr = []
    for x in range(2, u):
        n = 0.0
        d = 0.0
        for y in range(x - 2, len(D), x):
            n += 1
            d += D[y]
        avr.append(d / n)
    r = 0
    m = max(avr)
    for x in range(len(avr)):
        if abs(m - avr[x]) / m <= tol:
            r = x
            break
    file = open(info, 'a')
    file.write("Key length is " + str(r + 2) + "\n" + "D statistic: \n")
    for x in range(len(D)):
        file.write("[" + str(x) + "]: " + str(D[x]) + "\n")
    file.close()
    return r + 2


def vigenere_direct_dencryption(ciphertext: str, key: str) -> str:
    dictionary = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9,
                  'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18,
                  'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27,
                  'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    message = ""
    for x in range(len(ciphertext)):
        message += (letters[(dictionary[ciphertext[x]] + (len(letters) - dictionary[key[x % len(key)]])) % len(letters)])
    return message


def vigenere_direct_encryption(message: str, key: str) -> str:
    dictionary = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9,
                  'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18,
                  'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27,
                  'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    c = str()
    for x in range(len(message)):
        c = c + letters[(dictionary[message[x]] + dictionary[key[x % len(key)]]) % len(letters)]
    return c


def find_vigenere_cipher_key(cipher_text: str, r: int, info: str) -> str:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    dictionary = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9,
                  'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18,
                  'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ъ': 26, 'ы': 27,
                  'ь': 28, 'э': 29, 'ю': 30, 'я': 31}
    p = []
    zero = []
    for x in range(len(letters)):
        zero.append(0.0)
    for x in range(r):
        p.append(zero.copy())
    for x in range(len(cipher_text) - (len(cipher_text) % r)):
        p[x % r][dictionary[cipher_text[x]]] += 1
    key_signature = []
    for x in range(r):
        i = 0
        m = 0.0
        for y in range(len(letters)):
            if p[x][y] >= m:
                m = p[x][y]
                i = y
        key_signature.append(i)
    result = ""
    for x in range(len(key_signature)):
        if key_signature[x] - 14 >= 0:
            result += letters[key_signature[x] - 14]
        else:
            result += letters[32 + key_signature[x] - 14]
    file = open(info, 'a')
    file.write("The most likely key [" + result + "]\n")
    file.close()
    arg_max(p, info)
    return result


def arg_max(l: list, info: str):
    file = open(info, 'a')
    file.write("The most frequent letters: \n")
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    for x in range(len(l)):
        res = []
        f = list(l[x])
        sorted_f = f.copy()
        sorted_f.sort(reverse=True)
        for y in range(5):
            for k in range(len(f)):
                if f[k] == sorted_f[y]:
                    if k - 14 >= 0:
                        res.append(letters[k - 14])
                    else:
                        res.append(letters[32 + k - 14])
        file.write(str(x) + ": " + str(res) + '\n')
    file.close()


if __name__ == "__main__":
    vigenere_attack(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))