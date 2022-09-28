from operator import concat
import string

def describe(message: string):
    print(concat("\n    - ", message))