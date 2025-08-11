import os

from flask import Flask
import logging
from flask_cors import CORS
from app import blueprint

template_dir = os.path.abspath("./app/templates")
static_dir = os.path.abspath("./app/static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(blueprint)

CORS(app)
app.logger.setLevel(logging.DEBUG)


def main():
    if not os.path.isdir("./dot"):
        os.makedirs("./dot")

    if not os.path.isdir("./image"):
        os.makedirs("./image")


if __name__ == "__main__":
    main()
    app.run(debug=True, use_reloader=True)
