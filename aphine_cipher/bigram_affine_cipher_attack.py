# Oleksii Shevchenko

import sys
import math
import os


def affine_cipher_attack(cipher_text: str, distribution: str, bigram_distribution: str, directory: str):
    cipher_text = cleaning(load_source(cipher_text))
    distribution = load_source(distribution).split(" ")
    bigram_distribution = load_source(bigram_distribution).split(" ")
    for i in range(len(distribution)):
        distribution[i] = float(distribution[i])
    for i in range(len(bigram_distribution)):
        bigram_distribution[i] = float(bigram_distribution[i])

    entropy = compute_entropy(distribution)
    bigram_frequency = compute_bigram_frequency(cipher_text)
    pairs = make_bigram_pairs(arg_max(bigram_distribution, 6), arg_max(bigram_frequency, 6))
    key_brute_force(cipher_text, pairs, distribution, bigram_distribution, entropy, directory)


def load_source(path: str) -> str:
    source_file = open(path, encoding="utf8")
    data = source_file.read()
    source_file.close()
    return data


def build_dictionary() -> dict:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
    dictionary = dict()
    for i in range(len(letters)):
        dictionary[letters[i]] = i
    return dictionary


def encryption(message: str, a: int, b: int) -> str:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

    dictionary = build_dictionary()
    alphabet_len = len(dictionary.keys())

    cipher_text = ""
    for i in range(0, len(message) - (len(message) % 2), 2):
        x = alphabet_len * dictionary[message[i]] + dictionary[message[i + 1]]
        y = encrypt_function(x, a, b, alphabet_len)
        cipher_text += letters[int(y / alphabet_len)]
        cipher_text += letters[y % alphabet_len]
    return cipher_text


def encrypt_function(x: int, a: int, b: int, n: int) -> int:
    return (a * x + b) % (n ** 2)


def decryption(cipher_text: str, a: int, b: int) -> str:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

    dictionary = build_dictionary()
    alphabet_len = len(dictionary.keys())

    message = ""
    inv_a = inverse(a, len(letters) ** 2)
    inv_b = len(letters) ** 2 - b

    for i in range(0, len(cipher_text) - (len(cipher_text) % 2), 2):
        y = alphabet_len * dictionary[cipher_text[i]] + dictionary[cipher_text[i + 1]]
        x = encrypt_function(y, inv_a, inv_a * inv_b, alphabet_len)
        message += letters[int(x / alphabet_len)]
        message += letters[int(x % alphabet_len)]
    return message


def key_brute_force(text: str, pairs: list, distribution: list, bigram_distribution: list, entropy: float, directory: str):
    keys = []
    for i in range(len(pairs)):
        k = congruence_system(pairs[i][0][1], pairs[i][0][0], pairs[i][1][1], pairs[i][1][0], 31 ** 2)
        if len(k) == 0:
            continue
        for j in range(len(k[0])):
            if gcd(k[0][j], 31 ** 2) != 1:
                continue
            if [k[0][j], k[1][j]] in keys:
                continue
            if natural_language_processing(decryption(text, k[0][j], k[1][j]), distribution, bigram_distribution, entropy):
                keys.append([k[0][j], k[1][j]])
    write_digest(directory, keys, text)


def write_digest(directory: str, keys: list, text: str):
    if not os.path.exists(directory):
        os.mkdir(directory)
    digest = open(directory + "/digest.txt", 'w', encoding="utf8")
    for i in range(len(keys)):
        path = directory + "/" + str(i)
        os.mkdir(path)
        file = open(path + "/message.txt", 'w', encoding="utf8")
        file.write(decryption(text, keys[i][0], keys[i][1]))
        file.close()
        file = open(path + "/key.txt", 'w', encoding="utf8")
        file.write("a = " + str(keys[i][0]) + " b = " + str(keys[i][1]))
        file.close()
        m = decryption(text, keys[i][0], keys[i][1])[0:70]
        digest.write("[" + str(i) + "] (" + str(keys[i][0]) + ", " + str(keys[i][1]) + "): " + m + "\n")
    digest.close()


def natural_language_processing(text: str, distribution: list, bigram_distribution: list, entropy: float) -> bool:
    frequency = compute_frequency(text)
    if frequency_criteria(frequency, distribution, 0.025) and entropy_criteria(entropy, frequency, 0.06):
        bigram_frequency = compute_bigram_frequency(text)
        return bigram_frequency_criteria(bigram_frequency, bigram_distribution, 0.0072) \
               and banned_bigram_criteria(bigram_frequency, bigram_distribution)
    else:
        return False


def frequency_criteria(frequency: list, distribution: list, tol: float) -> bool:
    var = 0.0
    for i in range(len(distribution)):
        var += ((frequency[i] - distribution[i]) ** 2)
    return var <= tol


def bigram_frequency_criteria(bigram_frequency: list, bigram_distribution: list, tol: float) -> bool:
    var = 0.0
    for i in range(len(bigram_distribution)):
        var += ((bigram_frequency[i] - bigram_distribution[i]) ** 2)
    return var <= tol


def entropy_criteria(entropy: float, frequency: list, tol: float) -> bool:
    h = compute_entropy(frequency)
    return ((h - entropy) ** 2) <= tol


def banned_bigram_criteria(bigram_frequency: list, bigram_distribution: list) -> bool:
    for i in range(len(bigram_distribution)):
        if bigram_distribution[i] == 0:
            if bigram_frequency[i] != 0:
                return False
    return True


def compute_entropy(frequency: list) -> float:
    h = 0.0
    for i in range(len(frequency)):
        if frequency[i] != 0:
            h -= frequency[i] * math.log2(frequency[i])
    return h


def compute_frequency(text: str) -> list:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
    res = []
    for i in range(len(letters)):
        res.append(float(text.count(letters[i])) / len(text))
    return res


def compute_bigram_frequency(text: str) -> list:
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
    dictionary = dict()
    res = []
    for i in range(len(letters)):
        for j in range(len(letters)):
            dictionary[str(letters[i] + letters[j])] = i * len(letters) + j
            res.append(0.0)
    N = len(text) - (len(text) % 2)
    for i in range(0, N, 2):
        res[dictionary[text[i:i + 2]]] += 1.0
    for i in range(len(res)):
        res[i] = res[i] / (N / 2)
    return res


def arg_max(sequence: list, n: int) -> list:
    sorted_sequence = sequence.copy()
    sorted_sequence.sort(reverse=True)
    sorted_sequence = sorted_sequence[0:n]
    res = []
    for i in range(len(sequence)):
        if sequence[i] in sorted_sequence:
            res.append(i)
    return res


def make_bigram_pairs(x: list, y: list) -> list:
    x_pairs = []
    y_pairs = []
    for i in range(len(x)):
        for j in range(len(x)):
            if i != j:
                x_pairs.append([x[i], x[j]])
                y_pairs.append([y[i], y[j]])
    pairs = []
    for i in range(len(x_pairs)):
        for j in range(len(y_pairs)):
            pairs.append([[x_pairs[i][0], y_pairs[j][0]], [x_pairs[i][1], y_pairs[j][1]]])
    return pairs


def cleaning(text: str) -> str:
    text = text.lower()
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']
    result = ""
    for i in range(len(text)):
        if text[i] in letters:
            result += text[i]
    return result


def gcd(a: int, b: int) -> int:
    r = a % b
    while r != 0:
        a = b
        b = r
        r = a % b
    return int(b)


def inverse(a: int, n: int) -> int:
    if gcd(a, n) != 1:
        return 0
    if a == 1:
        return 1
    c = a
    d = n
    temp = 0
    aux = 1
    i = 0
    while True:
        r = d % c
        q = int((d - r) / c)
        d = c
        c = r
        res = temp + aux * q
        temp = aux
        aux = res
        i += 1
        if r == 1:
            break
    if i % 2 == 0:
        return int(res)
    else:
        return int(n - res)


def linear_congruence(a: int, b: int, n: int) -> list:
    d = gcd(a, n)
    if d == 1:
        return [(inverse(a, n) * b) % n]
    if gcd(b, d) == d:
        x = (inverse(int(a / d), int(n / d)) * int(b / d)) % int(n / d)
        res = []
        for i in range(d):
            res.append((x + int(n / d) * i))
        return res
    else:
        return []


def congruence_system(y1: int, x1: int, y2: int, x2: int, n: int) -> list:
    X = x1 - x2
    if X < 0:
        X = n + X
    Y = y1 - y2
    if Y < 0:
        Y = n + Y
    A = linear_congruence(X, Y, n)
    if len(A) == 0:
        return []
    B = []
    for i in range(len(A)):
        temp = y1 - ((A[i] * x1) % n)
        if temp >= 0:
            B.append(int(temp))
        else:
            B.append(int(n + temp))
    return [A, B]


if __name__ == "__main__":
    affine_cipher_attack(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
