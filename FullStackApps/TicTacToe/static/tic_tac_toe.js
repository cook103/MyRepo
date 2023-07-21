window.onload = function(){
    
    function fill_square() {
        // fill x and send response to backend
        $(".b").click(function() {
            let elementText = $(this).text(); // Get the text content of the clicked element
            console.log("Element Text: " + elementText);
            //id to find
            let t_id = elementText;
            
            $("#b" + t_id).text("X");
            $("#b" + t_id).css("background", "visible");
            $("#b" + t_id).css("color", "black");
            $("#b" + t_id).css("font-size", "80px");
    
            // Make the POST request and receive the data back as a variable
    
            post_request(elementText)
              .then(responseData => {
                console.log("Received data:", responseData["o"]);
                setTimeout(() => {  
                    
                    $("#b" + responseData["o"]).text("O");
                    $("#b" + responseData["o"]).css("background", "visible");
                    $("#b" + responseData["o"]).css("color", "black");
                    $("#b" + responseData["o"]).css("font-size", "80px");
                
                }, 300);
              })
              .catch(error => {
                console.error('Error:', error);
              });

        });
    }


    function recieve_square(){
        // fill in o's with get request
        o = get_request();
        console.log(o);
    }


    function get_request(){
        // grab the get request

        $.ajax({
            url:'/get_square',
            type: 'GET',
            contentType: "json",
            success: function(data){
                    console.log("Response:", data);

            },

        });
    }

    function post_request(text) {
        return new Promise((resolve, reject) => {
            let dataToSend = { "button": text };
    
            $.ajax({
                url: '/post_square',
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify(dataToSend),
                success: function(response) {
                    console.log("Response:", response);
                    resolve(response); // Resolve the Promise with the received data
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                    reject(error); // Reject the Promise with the error object
                }
            });
        });
    }
    

    fill_square();

}


