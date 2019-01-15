from django.utils.text import slugify


def create_slug(title, number):
    if number:
        title = title + ' ' + str(number)

    return slugify(title)


# TODO : Develop algorithm to calculate read time
def get_read_time(html_string):
    return 0
