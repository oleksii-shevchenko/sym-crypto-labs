# Oleksii Shevchenko

import re
import sys


def cleaning_with_space(resource: str, result: str):
    file = open(resource, encoding="utf8")
    text = file.read()
    text = text.lower()
    text = text.replace(' ', '_')
    text = text.replace('ё', 'e')
    text = text.replace('ъ', 'ь')
    letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н',
               'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я',
               '_']
    res = ""
    for i in range(len(text)):
        if text[i] in letters:
            res = res + text[i]
        else:
            res = res + "_"
    res = re.sub('_+', '_', res)
    file = open(result, 'w', encoding="utf8")
    file.write(res)
    file.close()


if __name__ == "__main__":
    cleaning_with_space(str(sys.argv[1]), str(sys.argv[2]))