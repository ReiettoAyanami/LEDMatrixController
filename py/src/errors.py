import json

errors:dict = {}

with open('py/configs/errors.json', 'r') as j:
    errors = json.load(j)