import requests

files = {'file': ('client.jpg', open('images/blue_devil.jpeg', 'rb'))}

r = requests.post("http://127.0.0.1:5000/receive_image", files=files)
print(r)
print(r.text)
