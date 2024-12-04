import re

def email_validator(email):
  pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
  result = re.match(pattern, email)
  if result:
    return True
  else: False