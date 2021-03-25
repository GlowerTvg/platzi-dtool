import os
import http.cookiejar as cookiejar
import utils.string.p_print as p_print

cookie_file = "/".join(os.path.abspath(__file__).split("/")[:-2])
cookie_file += "/cookies.txt"


def get_cookie_file():
    return cookie_file


def get_cookies():
    while True:
        if os.path.exists(cookie_file):
            cookies = cookiejar.MozillaCookieJar(cookie_file)
            cookies.load()
            break
        else:
            p_print.print_dialog("\n", "Cookie file not found, please put "
                                       "cookie file in project root path.", 1)

        input("\n    Press enter to retry.")

    return cookies


def exit_dialog():
    try:
        if input("\n    Do you want end task: [ENTER]y/N: ") == "":
            return True
        else:
            return False
    except (KeyboardInterrupt, EOFError):
        return True


def retry_dialog():
    try:
        if input("\n    Do you want retry task: [ENTER]y/N: ") == "":
            return True
        else:
            return False
    except (KeyboardInterrupt, EOFError):
        return False


def clear_screen():
    print('\033c')
    print('\033[2J\033[3J\033[1;1H')
    os.system('clear')


def continue_dialog():
    try:
        input("\n    Press enter to continue")
    except (KeyboardInterrupt, EOFError):
        if exit_dialog():
            return True
        else:
            return False


def check_path(target_path):
    if not os.path.exists(target_path):
        os.system(f"mkdir -p '{target_path}'")
