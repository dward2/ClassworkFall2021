import requests

server_name = "http://vcm-7631.vm.duke.edu:5000/"

r = requests.get(server_name+"countries")
print(r.text)

request_json = {"one": "Afghanistan", "two": "Albania"}
r = requests.post(server_name + "compare", json=request_json)
print(r.text)
if r.status_code != 200:
    print(r.text)
else:
    print(r.json())
