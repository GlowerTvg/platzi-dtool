import requests
from utils.tools import get_cookies
from utils.string.p_print import print_dialog
base_url = "https://platzi.com"


def get_base_url():
    """
    Scan a url

    :return: requests_object
    """

    url = base_url + "/" + input("\n    URL => https://platzi.com/")

    if url == base_url + '/':
        print_dialog("\n", "URL is not allowed", 2)
    else:

        try:
            r = requests.get(url, cookies=get_cookies())

            if r.status_code == 200:
                print_dialog("\n", f"URL: '{url}' loaded", 3)
                return [url, r]

            elif r.status_code == 404:
                print_dialog("\n", f"URL: '{url}' not found", 2)
            elif r.status_code == "403":
                print_dialog("\n", f"Access denied to URL: '{url}'", 2)

        except requests.ConnectionError:
            print_dialog("\n", "Check internet connection", 1)

        except requests.RequestException:
            print_dialog("\n", "Something happened during the request", 2)

    get_base_url()


def make_requests(url):
    try:
        r = requests.get(url, cookies=get_cookies())

        if r.status_code == 200:
            print_dialog("\n", f"URL: '{url}' loaded", 3)
            return r

        elif r.status_code == 404:
            print_dialog("\n", f"URL: '{url}' not found", 2)
        elif r.status_code == "403":
            print_dialog("\n", f"Access denied to URL: '{url}'", 2)

    except requests.ConnectionError:
        print_dialog("\n", "Check internet connection", 1)

    except requests.RequestException:
        print_dialog("\n", "Something happened during the request", 2)
