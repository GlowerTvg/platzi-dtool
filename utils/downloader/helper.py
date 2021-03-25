import os
# import json
# from time import sleep
from utils.string.p_print import print_dialog
import utils.string.style as style
import utils.string.p_print as p_print
from utils.extractor.url_tool import make_requests
import utils.tools as tools
# import requests
import re


def download_page(url, target_path, name):
    tools.check_path(target_path)
    p_print.line_char("-", "yellow", 2)
    print(style.string_color("    Step 1: Downloading Webpage\n", "blue"))

    r = make_requests(url)
    if not os.path.exists(target_path + '/' + name):
        with open(f"{target_path}/{name}", "w") as page:
            page.writelines(r.content.decode("UTF-8"))
            print_dialog("\n", "Webpage downloaded", 3)
    else:
        print_dialog("\n", "File already exists, skipping", 2)


def download_video(url, target_path, name):
    print(url)
    sp, q = ' ', '"'  # special values to create command line arguments and options
    if "www.youtube.com" not in url:
        cli_components = ['youtube-dl', "--cookies" + sp + q + tools.get_cookie_file() + q,
                          '-o' + sp + q + target_path + '/' + name + '.mp4' + q, url]
        print()
    else:
        cli_components = ['youtube-dl',
                          '-o' + sp + q + target_path + '/' + name + q, url]

    command = sp.join(cli_components)
    os.system(command)


def download_lesson(data):
    tools.check_path(data["path"])

    if data["type"] == "material":
        download_page(data["url"], data["path"], data["name"] + ".html")

    if data["type"] == "video":
        download_page(data["url"], data["extra_path"], data["webpage"])

        youtube_url = ""
        with open(f"{data['extra_path']}/{data['webpage']}", "r") as file:
            for line in file.readlines():
                current_line = line

                x = re.search("(www.youtube.com|youtu.?be)/embed/.+$", current_line)
                try:
                    if len(x.group()) > 20:
                        for letter in x.group():
                            if letter != '"':
                                youtube_url += letter
                            else:
                                break
                        break

                except AttributeError:
                    continue

        youtube_url = "https://" + youtube_url[:len(youtube_url) - 1]
        if "youtube.com" in youtube_url:
            data["url"] = youtube_url
        else:
            with open(f"{data['extra_path']}/{data['webpage']}", "r") as file:
                for line in file.readlines():
                    current_line = line
                    platzi_url = ""
                    x = re.search("(mdstrm.com)/video/.+$", current_line)
                    try:
                        if len(x.group()) > 20:
                            for letter in x.group():
                                if letter != '"':
                                    platzi_url += letter
                                else:
                                    break
                            break

                    except AttributeError:
                        continue

                platzi_url = "https://" + platzi_url
            data["url"] = platzi_url

        download_video(data["url"], data["path"], data["name"])
