from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "password"


# Note: JS is handling the backend functionality
@app.route("/", methods=["POST", "GET"])
def calculatorPage():
    return render_template("calculator.html")


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
