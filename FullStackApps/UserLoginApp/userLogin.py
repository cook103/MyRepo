from flask import Flask, request, render_template, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "password"

# Simple Test Data Base
user_list = [
    {"user": "mcookjr", "key": "password"},
]

status = {
    "status": "",
}


@app.route("/")
def login():
    if "user" in session:
        return redirect(url_for("user"))
    return render_template("login.html")


@app.route("/addUser", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        newUsername = request.form["username"]
        newPassword = request.form["password"]
        user_list.append({"user": newUsername, "key": newPassword})
        return jsonify({"redirect": "/"})
    return render_template("signup.html")


@app.route("/signup-link", methods=["POST", "GET"])
def signupLink():
    if request.method == "POST":
        return jsonify({"redirect": "/addUser"})


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for tElem in user_list:
            if username == tElem["user"] and password == tElem["key"]:
                status["status"] = "logged in"
                session["user"] = username
                return jsonify({"redirect": "/user"})
            else:
                status["status"] = "Failed to login"
    return status


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("home.html", user=user)
    else:
        return redirect(url_for("login"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        session.pop("user", None)
        return jsonify({"redirect": "/logout"})
    return redirect(url_for("login"))


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
