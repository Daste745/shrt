import json
import shortuuid
import os
from flask import Flask, request, redirect, render_template, flash, url_for
from wtforms import Form, StringField, validators


with open("redirects.json", "r") as f:
    redirects = json.load(f)


def save_redirects() -> None:
    with open("redirects.json", "w") as file:
        json.dump(redirects, file, indent=2)


app = Flask(__name__)
app.secret_key = os.urandom(32)


class RegisterUrlForm(Form):
    name = "Create short url"
    url = StringField("Url", [
        validators.InputRequired(),
        validators.URL(message="Invalid URL, \"http(s)://\" is required")
    ])
    key = StringField("Short Url", [
        validators.Optional(),
        validators.Length(min=0, max=16,
                          message="Max allowed lenght is 16"),
        validators.Regexp(regex=r"^[a-zA-Z0-9]+$",
                          message="Allowed characters: a-Z, A-Z, 0.9")
    ])


@app.route("/", methods=["GET", "POST"])
def index():
    form = RegisterUrlForm(request.form)

    if request.method == "POST" and form.validate():
        if not (key := form.key.data):
            key = shortuuid.random(6)

        if key in redirects.keys():
            flash((f"is already in use", redirects[key], key), "error")
        else:
            url = form.url.data
            redirects.update({key: url})
            save_redirects()

            registered_url = url_for('access_url', key=key, _external=True)
            flash((f"Created short url", registered_url), "success")

    return render_template("index.html", form=form)


@app.route("/<string:key>")
def access_url(key: str):
    if key not in redirects.keys():
        return f"There is no url bound to key '{key}'\n", 404

    return redirect(redirects[key])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

