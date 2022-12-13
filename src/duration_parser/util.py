import re


def split_flot_string_gen(string_value: str) -> [str, float]:
    for float_part, string_part in re.findall(r"([\d.]+)|([^\d.]+)", string_value):
        if float_part:
            float(float_part)
            yield float_part
        else:
            yield string_part


def rename_dict(old_dict, keymap) -> dict:
    new_dict = {}
    for key, value in keymap.items():
        if key in old_dict:
            new_key = keymap.get(key)
            new_dict[new_key] = old_dict.get(key)
    return new_dict


def convert_to_dict(string_list: list) -> dict:
    """
    split 3M to {M:3}
    :param string_list:
    :return: dictionary
    """
    dikt = {}
    for string in string_list:
        value, symbol = split_flot_string_gen(string)
        dikt[symbol] = int(value)
    return dikt
