window.onload = function(){

    //preset containers to manipulate
    let tStockContainer = $('.stock_container');
    let tCryptoContainer = $('.crypto_container');

    //On page load, instantiate the html with backend data
    tStockContainer.append('<div class="stock_name">' + 
        onload_data["stock_name"] + ": " + onload_data["stock_price"]+  '</div><br>');

    tCryptoContainer.append('<div class="crypto_name">' +  
        onload_data["crypto_name"] + ": " + onload_data["crypto_price"]+ '</div><br>');

    function canvas(){
            var canvasB = document.getElementById("canvas_background");
            var canvasH = document.getElementById("canvas_header");

            var ctxB = canvasB.getContext("2d");
            var ctxB = canvasB.getContext('2d');

            var ctxH = canvasH.getContext("2d");
            var ctxH = canvasH.getContext('2d');

            ctxB.fillStyle = 'red';
            ctxB.globalAlpha = 0.4;
            ctxB.fillRect(0,0,1500,300);

            ctxH.fillStyle = 'red';
            ctxH.globalAlpha = 0.4;
            ctxH.fillRect(0,0,200,50);


    
    }

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
    canvas();
    recurring_data();
    

}

