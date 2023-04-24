window.onload = function(){

    let tStockContainer = $('.stock_container');
    let tCryptoContainer = $('.crypto_container');

    //TODO: need to split name and price into stacked divs or span
    /*
    for (let tELem in stock_data["name"] && stock_data["price"]){
        tStockContainer.append('<div class="name">' + stock_data["name"][tELem] +
                 ": " + stock_data["price"][tELem]+  '</div>');
    }

    for (let tELem in crypto_data["name"] && crypto_data["price"]){
        tCryptoContainer.append('<div class="name">' + crypto_data["name"][tELem] +
                 ": " + crypto_data["price"][tELem]+  '</div>');
    }
    
    */

    function recurring_data(){
        setTimeout(recurring_data,2000);
        let x = "";

        $.ajax({
        url:'/ReccuringData',
        type: 'GET',
        dataType: "json",
        success: function(data){
                console.log(JSON.stringify(data)); 
                
                for (let tELem in data["crypto_name"] && data["crypto_price"]){
                    tCryptoContainer.append('<div class="name">' + data["crypto_name"][tELem] +
                             ": " + data["crypto_price"][tELem]+  '</div>');
                }
            }
        });

        /*

        */
    


    }
    recurring_data()

}

