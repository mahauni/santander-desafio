from flask import Blueprint


from flask import jsonify, render_template, send_file
import io

from app.graph_analysis import impact_on_remove, make_analysis

blueprint = Blueprint("app_blueprint", __name__)


@blueprint.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@blueprint.route("/analysis")
def analysis():
    return render_template("analysis_page.html")


@blueprint.route("/get_image")
def get_image():
    with open("./image/graph.gv.jpg", "rb") as f:
        image_data = f.read()

    return send_file(io.BytesIO(image_data), mimetype="image/jpeg")


@blueprint.route("/get_analysis")
def get_analysis():
    result = make_analysis()

    return jsonify(result)


@blueprint.route("/get_delete_analysis/<int:id>")
def get_delete_analysis(id):
    result = impact_on_remove(id)

    return jsonify(result)
