#!/usr/bin/env python3
from flask import ( 
        Flask,
        render_template,
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

#TODO: make more adaptable, html scrapping is hard coded
def scraped_parsed_data():
    """find and store parsed html data;
    stock index: names, price, dollar change,
    and percent change"""

    stock_data = parse("https://www.google.com/finance/markets/indexes") 
    crypto_data = parse("https://www.google.com/finance/markets/cryptocurrencies")

    stock_index_name = [x.text for x in \
                            stock_data.find_all("div",{"class", "ZvmM7"})]

    stock_index_price = [x.text for x in \
                            stock_data.find_all("span",{"class","JLPHhb"})]

    crypto_name = [x.text for x in \
                            crypto_data.find_all("div",{"class", "ZvmM7"})]

    crypto_price = [x.text for x in \
                            crypto_data.find_all("span",{"class","JLPHhb"})]

    data_dict = {
            'stock_name' : stock_index_name[:6],
            'stock_price' : stock_index_price[:6],
            'crypto_name' : crypto_name[:6],
            'crypto_price' : crypto_price[:6],
    }

    return data_dict

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def return_index():
    """Onload data is sent here"""
    onload_data = scraped_parsed_data()
    return render_template("stock_index.html",  onload_data=onload_data)

@app.route("/ReccuringData",methods=['GET','POST'])
def return_scraped_data():    
    """Reccuring data is sent here"""
    data = scraped_parsed_data()
    print(f"dict data: {data}")
    return json.dumps(data)


def main():
    app.run(debug=True, port="8080")

if __name__ == "__main__":
    main()

#end
