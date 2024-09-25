import pyperclip
from random_username.generate import generate_username
from string import digits
import re


def trim_after_capital(word):
    # Use regular expression to find the first occurrence of a capital letter and trim the string
    return re.split(r'(?=[A-Z])', word)[0]

initial = generate_username(1)[0]

initial_part = trim_after_capital(initial)
# print(initial_part)

user = generate_username(1)[0]

remove_digits = str.maketrans('', '', digits)
username = user.translate(remove_digits).lower()
pyperclip.copy(initial_part+username)
# print(username)
final_username = initial_part+username
print(final_username)