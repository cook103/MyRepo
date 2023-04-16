from flask import Flask,render_template

#Flask Local Host Server For Simple JS Calculator

app = Flask(__name__)
    
@app.route("/",methods=['POST','GET'])
def calculatorPage():
    return render_template('calculator.html')
    
if __name__ == "__main__":
    app.run(debug=True)