from flask import Flask, jsonify, redirect, url_for

from api.route.host import host
from api.route.translate import translate

app = Flask(__name__)
app.register_blueprint(host, url_prefix='/host/')
app.register_blueprint(translate, url_prefix='/translate/')


@app.route('/')
def index():
    return redirect(url_for('ping'))


@app.route('/ping/')
def ping():
    response = {
        "response": "I am alive!"
    }
    return jsonify(response)


@app.route("/urls/")
def urls():
    print(app.url_map)
    return jsonify(app.url_map)
    # todo: fix this


if __name__ == '__main__':
    app.run()
