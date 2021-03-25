from colorama import Fore
from colorama import Style
import os

# Terminal cols num
TERMINAL_COLS = os.get_terminal_size().columns

# OUTPUT SLEEP DURATION
line_sleep = 0.02
end_line_sleep = 0.3


# Update terminal cols
def update_terminal_cols():
    global TERMINAL_COLS
    TERMINAL_COLS = os.get_terminal_size().columns


# Valid colors (Alacrity color scheme)
COLOR = {
    'black': Fore.BLACK,
    'blue': Fore.BLUE,
    'cyan': Fore.CYAN,
    'green': Fore.GREEN,
    'magneta': Fore.MAGENTA,
    'red': Fore.RED,
    'white': Fore.WHITE,
    'yellow': Fore.YELLOW
}


def string_color(string, color):
    """
    Apply special format to allow use colors in output

    :param string: String to apply color format
    :param color: Color to use in format

    :return: Colored string
    """
    return f"{COLOR[color]}{string}{Style.RESET_ALL}"


def string_position(string, position, spaces):

    update_terminal_cols()

    str_output = string

    if position == 'left':

        if spaces > 0:
            str_output = ' ' * spaces

        str_output = format_string(str_output, spaces)

    elif position == 'center':
        expression = ' ' * ((TERMINAL_COLS - len(str_output)) // 2)
        str_output = expression + str_output + expression

    else:
        expression = ' ' * ((TERMINAL_COLS - len(str_output)) - spaces)
        str_output = expression + str_output

        if spaces > 0:
            str_output += ' ' * spaces

    return str_output


def format_string(string, spaces):
    """
    Format string if len is more than TERMINAL_COLS, allows display string
    in two line

    :param string: String to format
    :param spaces: Spaces used at being of new line
    :return: Formatted string
    """

    expression = '\n'

    if spaces > 0:
        expression += ' ' * spaces

    if len(string) > TERMINAL_COLS:
        t_str = list(string)
        t_str[TERMINAL_COLS - 1] = t_str[TERMINAL_COLS - 1] + expression

        return ''.join(t_str)

    else:
        return string


def format_name_string(original_str):
    """
    Returns a string that only contains english alphabet

    :param original_str: Original string
    :return: formatted_str: str, formatted string,
     with special character of spanish language
    """

    # All know characters that no are valid for strings
    know_chars = [{'bad': 'ó', 'good': 'o'}, {'bad': 'á', 'good': 'a'},
                  {'bad': 'é', 'good': 'e'}, {'bad': 'í', 'good': 'i'},
                  {'bad': 'ú', 'good': 'u'}, {'bad': ':', 'good': ' -'},
                  {'bad': '/', 'good': '__'}, {'bad': '¿', 'good': ''},
                  {'bad': 'Á', 'good': 'A'}, {'bad': 'É', 'good': 'E'},
                  {'bad': 'Í', 'good': 'I'}, {'bad': 'Ó', 'good': 'O'},
                  {'bad': 'Ú', 'good': 'U'}, {'bad': 'à', 'good': 'a'},
                  {'bad': 'è', 'good': 'e'}, {'bad': 'ì', 'good': 'i'},
                  {'bad': 'ù', 'good': 'ù'}, {'bad': 'À', 'good': 'A'},
                  {'bad': 'È', 'good': 'E'}, {'bad': 'Ì', 'good': 'I'},
                  {'bad': 'Ù', 'good': 'Ù'}, {'bad': '`', 'good': ''}]

    formatted_str = original_str  # value to work

    # Find all coincidences into 'clean_str' and replace them
    for dict_char in know_chars:
        if dict_char['bad'] in original_str:
            # Replace 'bad' char with 'good' char
            formatted_str = formatted_str.replace(dict_char['bad'],
                                                  dict_char['good'])

    # if formatted_str ends with "." remove them
    if formatted_str[len(formatted_str) - 1] == ".":
        formatted_str = formatted_str[:len(formatted_str) - 1]

    # if formatted_str end with " " remove them
    if formatted_str[len(formatted_str) - 1] == " ":
        formatted_str = formatted_str[:len(formatted_str) - 1]

    if "\t" in formatted_str:
        formatted_str = formatted_str.replace("\t", "")

    return formatted_str

