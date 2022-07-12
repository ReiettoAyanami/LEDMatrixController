import json

errors:dict = {}

with open('configs/errors.json', 'r') as j:
    errors = json.load(j)