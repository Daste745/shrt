import requests
import json
import re
import shortuuid
import os
from flask import Flask, request, redirect, render_template, flash, url_for
from wtforms import Form, TextField, validators


with open("redirects.json", "r") as f:
    redirects = json.load(f)


def save_redirects() -> None:
    with open("redirects.json", "w") as f:
        json.dump(redirects, f, indent=2)


app = Flask(__name__)
app.secret_key = os.urandom(32)


class RegisterUrlForm(Form):
    name = "Create short url"
    url = TextField("Url", [validators.DataRequired(),
                            validators.URL()])
    key = TextField("Key", [validators.Length(min=0, max=16),
                            validators.Optional()])


@app.route("/", methods=["GET", "POST"])
def index():
    form = RegisterUrlForm(request.form)

    if request.method == "POST" and form.validate():
        request_url = url_for("create_url",
                              url=form.url.data,
                              key=form.key.data,
                              _external=True)
        flash(requests.get(request_url).content)

    return render_template("index.html", form=form)


@app.route("/<string:key>")
def access_url(key: str):
    if key not in redirects.keys():
        return f"There is no url bound to key '{key}'\n", 404

    return redirect(redirects[key])


@app.route("/create")
def create_url():
    if not (url := request.args.get("url")):
        return "'url' is a required parameter\n", 400
    url_match = re.match(r"^https?:\/\/\S+$", url)
    if not url_match:
        return f"url '{url}' is invalid", 400

    if not (key := request.args.get("key")):
        key = shortuuid.random(6)
    if not re.match(r"^[a-zA-Z0-9]+$", key):
        return f"key '{key}' is invalid (only alphanumeric allowed)\n", 400

    if key in redirects.keys():
        return f"key '{key}' is already in use ({redirects[key]})\n", 400

    redirects.update({key: url})
    save_redirects()

    return f"registered '{key}' -> '{url}'\n"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

