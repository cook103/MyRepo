from flask import ( 
        Flask,
        request,
        render_template,
        jsonify,
        redirect,
        url_for,
        session,
        json)

import requests
from bs4 import BeautifulSoup

def parse(url):
    """Parse the given url's html if input type
    is a string"""
    if isinstance(url,str):
        html = requests.get(url)
        soup = BeautifulSoup(html.content,"html.parser")
    else:
        raise TypeError("Must be a string input")
    return soup

def parsed_data(data):
    """find and store parsed html data;
    stock index: names, price, dollar change,
    and percent change"""

    stock_index_name = [x.text for x in \
                            data.find_all("div",{"class", "ZvmM7"})]

    stock_index_price = [x.text for x in \
                            data.find_all("span",{"class","JLPHhb"})]
    """               
    stock_index_dollar_change = [x.text for x in \
                                     data.find_all("span",{"class","P2Luy"})]
    
    stock_index_percent_change = [x.text for x in \
                                     data.find_all("div",{"class","JwB6zf"})]
    """

    data_dict = {
            'name' : stock_index_name[:6],
            'price' : stock_index_price[:6],
             #'dollar_change' : stock_index_dollar_change[:6],
             #'percent_change' : stock_index_percent_change[:6]
    }

    return data_dict

app = Flask(__name__)
app.secret_key = "password"

@app.route("/",methods=['GET','POST'])
def get_scraped_data():
    data = parse("https://www.google.com/finance/markets/indexes") 
    data = parsed_data(data)
    print("data sent")
    return render_template("stock_index.html", data=data)

def main():
    app.run(debug=True, port="8080")

if __name__ == "__main__":
    main()

