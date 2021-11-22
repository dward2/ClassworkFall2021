from flask import Flask, request


app = Flask(__name__)


@app.route("/receive_image", methods=["POST"])
def receive_image():
    f = request.files['file']
    new_filename = "ser rec {}".format(f.filename)
    f.save(new_filename)
    return "Good"


if __name__ == '__main__':
    app.run()
