from lxml import html
# import requests
# import json
from time import sleep
# import http.cookiejar as cookiejar
import utils.downloader.helper as helper
from utils.string.p_print import header
import utils.string.p_print as p_print
import utils.extractor.url_tool as url_tool
import utils.string.style as style
from utils.string.style import string_color
import utils.tools as tools

mode = 2


def update_mode(new_mode):
    global mode

    mode = new_mode


def init():
    header("  scraper setup", "", "cyan", "left", 1, "-", "green", 0)

    print(style.string_color("  Base URL:", "blue"))

    while True:
        try:
            response = url_tool.get_base_url()
            if "/clases/" in response[0]:
                update_mode(1)

            with open("000 - Preview.html", "w") as page:
                page.writelines(response[1].content.decode("UTF-8"))

            if tools.continue_dialog():
                return

            break

        except (KeyboardInterrupt, EOFError):
            if tools.exit_dialog():
                return

    if mode == 2:
        try:
            scrape_courses(response[1])
        except (KeyboardInterrupt, EOFError):
            if tools.exit_dialog():
                return
    else:
        try:
            scrape_course("", response[1], response[0])
        except (KeyboardInterrupt, EOFError):
            if tools.exit_dialog():
                return


def scrape_courses(r_object):
    tools.clear_screen()
    em = "    Load and select courses to process"
    header("  scraper setup", em, "cyan", "left", 1, "-", "green", 0)
    print(style.string_color("  Course list:", "blue"))

    target_page = html.fromstring(r_object.content)
    course_list = []
    course_count = 0

    for course in target_page.xpath('//div[@class="RoutesList-items"]'):
        for link in course.xpath('a[@class="RoutesList-item"]/@href'):
            name = style.format_name_string(
                course.xpath('a[@href="' + link + '"]/h4/text()')[0]
            )

            url = url_tool.base_url + link

            course_list.append(
                {
                    "name": name, "url": url,
                    "index": course_count, "active": True
                }
            )

            course_count += 1

    # print info about data loaded from r_object
    sleep(0.2)
    print(string_color(f"\n    Total courses: {course_count}", "cyan"))

    print()
    p_print.line_char("-", "cyan", 2)
    for data in course_list:
        print(f"    Name: {string_color(data['name'], 'green')}")
        sleep(style.line_sleep)
        print(f"    URL: {string_color(data['url'], 'green')}")
        sleep(style.line_sleep)
        print(f"    Index: {string_color(data['index'], 'cyan')}")
        sleep(style.line_sleep)
        print()

    while True:
        try:
            exclude_list = input("\n  Courses to exclude (index) => ")
            if len(exclude_list) > 0:
                for index in exclude_list.split(" "):
                    if int(index) <= len(course_list) - 1:
                        course_list[int(index)]["active"] = False

                print(string_color("\n  Courses excluded from list: \n", "blue"))
                p_print.line_char("-", "red", 2)
                for i in course_list:
                    if not i["active"]:
                        print(f"    Name: {string_color(i['name'], 'red')}")
                        sleep(style.line_sleep)
                        print(f"    URL: {string_color(i['url'], 'red')}")
                        sleep(style.line_sleep)
                        print(f"    Index: {string_color(i['index'], 'red')}")
                        sleep(style.line_sleep)
                        print()
            break
        except (KeyboardInterrupt, EOFError):
            if tools.exit_dialog():
                return

    if tools.continue_dialog():
        return

    course_count = 1
    for i in course_list:
        if course_count > 9:
            cn = "0"
        else:
            cn = "00"

        if i["active"]:
            while True:
                r = url_tool.make_requests(i["url"])
                if r.status_code == 200:
                    scrape_course(f"{cn}{course_count}", r, i["url"])
                    course_count += 1
                    break
                else:
                    if not tools.retry_dialog():
                        break


def scrape_course(numeration, r_object, course_url):
    data = {}
    tools.clear_screen()

    target_page = html.fromstring(r_object.content)

    course_title = style.format_name_string(
        target_page.xpath('//h1[@class="CourseDetail-left-title"]/text()')[0]
    )

    if mode == 2:
        course_title = f"{numeration} - {course_title}"

    em = style.format_string(f"    Processing: {course_title}", 16)
    header("  downloading", em, "cyan", "left", 1, "-", "green", 0)

    print(style.string_color("  Course information: \n", "blue"))
    sleep(style.line_sleep)
    print(style.format_string(f"    Course: {course_title}", 12))

    # Download course page
    helper.download_page(course_url, course_title, "000 - Preview.html")
    course_url = course_url.replace("/clases/", "/cursos/")
    helper.download_page(course_url, course_title, "Course Details.html")

    sections = target_page.xpath('//div[@class="Material-concept"]')
    s_count = 1

    for s in sections:

        sn = "00"
        if s_count > 9:
            sn = "0"

        s_title = s.xpath(
            'div[@class="Material-concept-edit"]'
            '/h3[@class="Material-title"]/text()')[0]

        s_title = f"{sn}{s_count} - {style.format_name_string(s_title)}"

        # print()
        # p_print.line_char("-", "cyan", 2)
        # print(style.format_string(f"    Section: {s_title}\n", 13))

        l_count = 1
        for lesson in s.xpath('div[@class="MaterialItem-content"]'):

            ln = "00"
            if l_count > 9:
                ln = "0"

            lock_element = 'div/div[@class="MaterialItem-copy"]' \
                           '/div[@class="MaterialItem-copy-actions"]/div[' \
                           '@class="MaterialItem-copy-actions-anchor"]/i/@class '

            if not len(lesson.xpath(lock_element)) > 0:
                if len(lesson.xpath('div/div[@class="MaterialItem-video"]')) > 0:
                    # lesson_type = "[VIDEO_NAME]"
                    # course_data["type"] = "video"
                    l_type = "video"
                else:
                    # lesson_type = "[MATERIAL_NAME]"
                    # course_data["type"] = "material"
                    l_type = "material"

                l_title = lesson.xpath('div/div[@class="MaterialItem-copy"]'
                                       '/p[@class="MaterialItem-copy-title"]'
                                       '/text()')

                l_title = f"{ln}{l_count} - {style.format_name_string(l_title[0])}"
                # print(style.format_string(f"      Lesson: {l_title}", 14))

                l_url = lesson.xpath('a[@class="MaterialItem-anchor"]'
                                     '/@href')[0]

                l_url = url_tool.base_url + l_url
                # print(style.format_string(f"        URL: {l_url}", 13))

                # set data and start lesson download action
                data["path"] = course_title + '/' + s_title
                data["name"] = l_title
                data["url"] = l_url
                data["type"] = l_type
                if l_type == "video":
                    data["extra_path"] = f"{course_title}/{s_title}/"
                    data["extra_path"] += f"{ln}{l_count} - extra_files"
                    data["webpage"] = f"{ln}{l_count} - webpage.html"

                helper.download_lesson(data)
                tools.clear_screen()

            l_count += 1
        s_count += 1

    input("\n\n    Press enter to continue")
