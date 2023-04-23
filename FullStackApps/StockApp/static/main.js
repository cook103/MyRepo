window.onload = function(){

    //console.log(data);

    let tStockContainer = $('.stock_container');
    let tCryptoContainer = $('.crypto_container');

    //TODO: need to split name and price into stacked divs or span

    for (let tELem in stock_dict["name"] && stock_dict["price"]){
        tStockContainer.append('<div class="name">' + stock_dict["name"][tELem] +
                 ": " + stock_dict["price"][tELem]+  '</div>');
    }

    for (let tELem in crypto_dict["name"] && crypto_dict["price"]){
        tCryptoContainer.append('<div class="name">' + crypto_dict["name"][tELem] +
                 ": " + crypto_dict["price"][tELem]+  '</div>');
    }
}