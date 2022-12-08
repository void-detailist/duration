import re


def split_flot_string_gen(string_value: str) -> [str, float]:
    for float_part, string_part in re.findall(r"([\d.]+)|([^\d.]+)", string_value):
        if float_part:
            float(float_part)
            yield float_part
        else:
            yield string_part


def rename(old_dict, keymap) -> dict:
    new_dict = {}
    for key, value in zip(keymap.keys(), old_dict.values()):
        new_key = keymap.get(key, key)
        new_dict[new_key] = old_dict[key]
    return new_dict


def convert_to_dict(string_list: list, add_letter: str) -> dict:
    """
    split 3M to {M:3}
    :param add_letter:
    :param string_list:
    :return: dictionary
    """
    dikt = {}
    for string in string_list:
        value, symbol = split_flot_string_gen(string)
        dikt[add_letter + symbol] = int(value)
    return dikt
