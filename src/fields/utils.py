import re


emailRegex = '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'
textRegex = '[A-Z, a-z, ]*'
mobileRegex = '^\d{10}$'
noSpecialCharRegex = '[^A-Za-z0-9]+'


def to_upper_case_string(string):
    return re.sub(noSpecialCharRegex, ' ', string).title()
