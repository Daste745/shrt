import json
import shortuuid
import os
from flask import Flask, request, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, validators
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.urandom(32)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shrt.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class Redirect(db.Model):
    __tablename__ = "redirects"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    key = db.Column(db.String)
    created = db.Column(db.DateTime)

    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.created = datetime.utcnow()


# Create db tables if they don't exist
db.create_all()


class RegisterUrlForm(Form):
    name = "Create short url"
    url = StringField(
        "Url",
        [
            validators.InputRequired(),
            validators.URL(message='Invalid URL, "http(s)://" is required'),
        ],
    )
    key = StringField(
        "Short Url",
        [
            validators.Optional(),
            validators.Length(min=0, max=16, message="Max allowed lenght is 16"),
            validators.Regexp(
                regex=r"^[a-zA-Z0-9]+$", message="Allowed characters: a-z, A-Z, 0-9"
            ),
        ],
    )


@app.route("/", methods=["GET", "POST"])
def index():
    form = RegisterUrlForm(request.form)

    if request.method == "POST" and form.validate():
        if not (key := form.key.data):
            key = shortuuid.random(8)

        if used := Redirect.query.filter(Redirect.key == key).first():
            flash((f"is already in use", used.url, key), "error")
        else:
            record = Redirect(form.url.data, key)
            db.session.add(record)
            db.session.commit()

            registered = url_for("access_url", key=record.key, _external=True)
            flash((f"Created short url", registered), "success")

    return render_template("index.html", form=form)


@app.route("/<string:key>")
def access_url(key: str):
    if not (registered := Redirect.query.filter(Redirect.key == key).first()):
        return f"There is no url bound to key '{key}'\n", 404

    response = redirect(registered.url)
    response.headers.add(
        "Referer",
        url_for(
            "access_url",
            key=registered.key,
            _external=True,
        ),
    )
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
