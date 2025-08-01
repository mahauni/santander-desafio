from flask import Flask, send_file
import io
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get_image")
def get_image():
    with open("./image/graph.gv.jpg", 'rb') as f:
        image_data = f.read()

    return send_file(io.BytesIO(image_data), mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)