window.onload = function(){

    //preset containers to manipulate
    let tStockContainer = $('.stock_container');
    let tCryptoContainer = $('.crypto_container');

    //On page load, instantiate the html with backend data
    tStockContainer.append('<div class="stock_name">' + 
        onload_data["stock_name"] + ": " + onload_data["stock_price"]+  '</div><br>');

    tCryptoContainer.append('<div class="crypto_name">' +  
        onload_data["crypto_name"] + ": " + onload_data["crypto_price"]+ '</div><br>');

    function recurring_data(){
        /*grab updated scraped data every second*/
        setTimeout(recurring_data,1000);

        $.ajax({
        url:'/ReccuringData',
        type: 'GET',
        dataType: "json",
        success: function(data){
                console.log(JSON.stringify(data)); 

                stock_class = $('.stock_name');
                crypto_class = $('.crypto_name');
                
                //during recurring calls, update the html
                stock_class.text(data["stock_name"] +": " + data["stock_price"]);
                crypto_class.text(data["crypto_name"] +": " + data["crypto_price"]);


            }
        });


    }
    recurring_data()

}

