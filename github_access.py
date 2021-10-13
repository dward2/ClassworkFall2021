import requests

server_name = "https://api.github.com/"

r = requests.get(server_name +"repos/dward2/BME547/branches")

print(r)
print(type(r))
print(r.status_code)
print(r.text)

branches = r.json()
print(type(branches))
# print(branches)
# for branch in branches:
#     print(branch["name"])
