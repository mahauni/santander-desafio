from flask import Flask, jsonify, send_file
import io
import logging
from flask_cors import CORS

from main import make_analisis

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/get_image")
def get_image():
    with open("./image/graph.gv.jpg", "rb") as f:
        image_data = f.read()

    return send_file(io.BytesIO(image_data), mimetype="image/jpeg")


@app.route("/get_analisis")
def get_analisis():
    result = make_analisis()

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
