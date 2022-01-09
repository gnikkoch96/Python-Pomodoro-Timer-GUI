import json

f = open("json_file.json")

data = json.load(f)

print(data)

print(data['date']['01/08/22'])
print(data['total_mins'])
print(data['total_poms'])



