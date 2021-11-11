import base64
import requests
import os

server_name = "http://vcm-21170.vm.duke.edu"


def send_image_to_server(filename):
    b64_string = convert_image_file_to_b64_string(filename)
    reply = send_b64_string_to_server(b64_string)
    return reply


def convert_image_file_to_b64_string(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def send_b64_string_to_server(b64_string):
    out_json = {"image": b64_string,
                "net_id": "daw74",
                "id_no": 1}
    r = requests.post(server_name+"/add_image",
                      json=out_json)
    if r.status_code != 200:
        print(r.text)
        return False
    else:
        print(r.text)


def get_image_from_server(net_id, id_no):
    r = requests.get(server_name+"/get_image/{}/{}".format(net_id, id_no))
    b64_string = r.text
    image_bytes = base64.b64decode(b64_string)
    with open("new_img.jpg", "wb") as out_file:
        out_file.write(image_bytes)


if __name__ == '__main__':
    fn = os.path.join("images", "blue_devil.jpeg")
    send_image_to_server(fn)

    get_image_from_server("daw74", 1)
