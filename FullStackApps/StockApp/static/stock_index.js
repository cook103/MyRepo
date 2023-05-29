window.onload = function(){

    //On page load, instantiate the html with backend data
        for (let tElem in onload_data["crypto_name"]){
        $(".c_names").append('<div id="crypto_name' + tElem + '">' + 
            onload_data["crypto_name"][tElem] +  '</div><br>');
    }
    
    
    for (let tElem in onload_data["crypto_price"]){
        $(".c_prices").append('<div id="crypto_price' + tElem + '">' + 
            onload_data["crypto_price"][tElem] +  '</div><br>');
    }

/*
    function canvas(){
        //make shapes on webpage (design)
        var canvasB = document.getElementById("canvas_background");
        //var canvasH = document.getElementById("crypto_header");

        var ctxB = canvasB.getContext("2d");
        var ctxB = canvasB.getContext('2d');

        //var ctxH = canvasH.getContext("2d");
        //var ctxH = canvasH.getContext('2d');

        ctxB.fillStyle = 'red';
        ctxB.globalAlpha = 0.4;
        ctxB.fillRect(0,0,2000,300);

        //ctxH.fillStyle = 'red';
        //ctxH.globalAlpha = 0.4;
        //ctxH.fillRect(0,0,110,50);

    }
*/


    function update_page(data){
        //update price elements
        for (let index in data["crypto_price"]){
            $("#crypto_price" + index).text(data["crypto_price"][index]);
        }

    }

    function recurring_data(){
        /*grab updated scraped data every second*/
        setTimeout(recurring_data,1000);

        $.ajax({
        url:'/ReccuringData',
        type: 'GET',
        dataType: "json",
        success: function(data){
                //console.log(JSON.stringify(data)); 
                update_page(data);
            }
        });


    }

    recurring_data();
    

}

