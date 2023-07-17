window.onload = function(){

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

        //ctxH.fillStyle = 'red';ls
        //ctxH.globalAlpha = 0.4;
        //ctxH.fillRect(0,0,110,50);

    }
*/

    function update_page(data){
        //update price elements
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


