import os
from utils.string import style
from time import sleep

# Terminal cols num
TERMINAL_COLS = os.get_terminal_size().columns


# Update terminal cols
def update_terminal_cols():
    global TERMINAL_COLS
    TERMINAL_COLS = os.get_terminal_size().columns


def line_char(char, color, spaces):
    """
    Print a line filled with characters from begin to end

    :param color: Color for chars
    :param char: Char to fill line
    :param spaces: Spaces at begin and the end
    """

    update_terminal_cols()

    if spaces == 0:
        str_output = char * TERMINAL_COLS
    else:
        str_output = char * (TERMINAL_COLS - (spaces * 2))
        str_output = ' ' * spaces + str_output + ' ' * spaces

    str_output = style.string_color(str_output, color)

    print(str_output)


def header(title, extra, color, pos, str_case, decoration, d_color, d_spaces):
    """
    Print a special header for current task

    :param title: Task title
    :param extra: Extra information about task
    :param color: Color title
    :param pos: Title position
    :param str_case: 1 upper case, all other is lower case
    :param decoration: Character to fill borders
    :param d_color: Borders color
    :param d_spaces: Spaces at begin and end of border
    :return:
    """

    str_title = ""

    if str_case == 1:
        for char in title:
            if char == " ":
                str_title += char * 2
                continue

            str_title += ' ' + char.upper()

        str_title = str_title[1:]

    str_title = style.string_position(str_title, pos, 0)
    str_title = style.string_color(str_title, color)

    line_char(decoration, d_color, d_spaces)
    print(str_title)

    if len(extra) > 0:
        if type(extra) == str:
            print(extra)
        else:
            for i in extra:
                print(i)
    line_char(decoration, d_color, d_spaces)


def menu_item(str_item, mode):

    sleep(style.line_sleep)
    if mode == 1:
        print((' ' * 8) + str_item)
    else:
        print('\n' + style.string_color((' ' * 4) + str_item, "blue"))


def print_dialog(pre_char, message, m_type):
    """
    Print a program dialog

    :param pre_char: Character to put at begin or message
    :param message: Text to show in dialog
    :param m_type: 1=error dialog, 2=warning dialog, 3=success dialog
    :return:
    """

    message = "        " + message
    if m_type == 1:
        print(style.string_color(pre_char + "    Error: " +
                                 "\n" + message, "red"))
    elif m_type == 2:
        print(style.string_color(pre_char + "    Warning: " +
                                 "\n" + message, "yellow"))
    else:
        print(style.string_color(pre_char + "    Success" +
                                 "\n" + message, "green"))
