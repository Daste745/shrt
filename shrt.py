import json
import re
import shortuuid
from flask import Flask, request, redirect

with open("redirects.json", "r") as f:
    redirects = json.load(f)


def save_redirects() -> None:
    with open("redirects.json", "w") as f:
        json.dump(redirects, f, indent=2)


app = Flask(__name__)


@app.route("/")
def index():
    return """
        <center><h1>Welcome to shrt!<h1></center>
        <h2>This site is under development,
        follow these instructions to use it:</h2>
        Access a short url <b>/somekey</b><br><br>
        Create a short url: <b>/create?url=https://website.com</b><br><br>
        Specify a key: <b>/create?url=https://website.com&key=somekey</b>
        <br><br><br><h3><a href='https://s.daste.me/shrt' target='blank'>
        See shrt on github</a></h3>
    """


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

