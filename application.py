# from curses.ascii import US
from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

USERS = {}


@app.route("/")
def index():
    return "Index Page"


@app.route("/users/<user>", methods=["PUT"])
def update_user(user):

    if user in USERS:
        update_user = request.get_json()
        USERS[user] = update_user
        return jsonify(USERS[user]["name"])

    return Response(status=400)


@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):

    if username in USERS:
        USERS.pop(username)
        return jsonify({"success": "true"})

    return Response(status=400)


@app.route("/users/", methods=["POST"])
def post_user():

    new_user = request.get_json()

    if new_user:
        USERS.update(new_user)
        return jsonify({"success": "true"}), 201

    return Response(status=400)


@app.route("/users/", methods=["GET"])
def get_users():
    return jsonify(USERS)


@app.route("/users/<username>", methods=["GET"])
def access_users(username):
    if request.method == "GET":
        user_details = USERS.get(username)
        if user_details:
            return jsonify(user_details)
        else:
            return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)
