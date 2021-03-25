#!/usr/bin/python3
from utils.string.p_print import header
from utils.string.p_print import menu_item
import utils.tools as tools
import utils.string.style as style
import os
from time import sleep
import utils.extractor.scraper as scraper

"""
    This script only works on Linux based system and MacOS
    Author: Devil64-Dev (devil64dev@gmail)
    GitHub: https://github.com/Devil64-Dev/platzi-dtool
    Created on: 15-02-2021

    Code conventions:
        -Max of 79 chars for line
        -Variables and function names in under score case.
"""
PROGRAM_TITLE = "Platzi Downloader Tool"


def menu():
    tools.clear_screen()
    work_dir = f"{' ' * 4}Directory: {os.getcwd()}"
    work_dir = style.string_position(work_dir, "center", 0)
    project_url = "GitHub Repo: https://github.com/Devil64-Dev/platzi-dtool"
    project_url = style.string_position(project_url, "center", 0)

    header(PROGRAM_TITLE, {work_dir, project_url}, "white", "center", 1, "=", "green", 0)

    menu_item("PROGRAM OPTIONS:", 2)
    # Show download options
    menu_item("1. Start download", 1)
    # Show program options
    menu_item("2. Exit program", 1)


def get_user_input(options):
    """
    :param options: list of valid options
    :return: validated user input, ready to use
    """
    sleep(style.line_sleep)
    option = input(style.string_color("\n    => Option number: ", "cyan"))

    if option not in options:
        print(style.string_color((' ' * 7)
                                 + f"Option {option} not valid", "red"))
        sleep(style.end_line_sleep)
        get_user_input(options)
    else:
        return option


def __main__():
    try:
        menu()
        try:
            op = get_user_input({"1", "2"})
        except EOFError:
            op = "2"

        if op == "1":
            tools.clear_screen()
            scraper.init()
        elif op == "2":
            if tools.exit_dialog():
                return

    except KeyboardInterrupt:
        if tools.exit_dialog():
            return

    __main__()


__main__()
