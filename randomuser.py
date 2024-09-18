import pyperclip
from random_username.generate import generate_username

user = generate_username(1)[0]

pyperclip.copy(user)