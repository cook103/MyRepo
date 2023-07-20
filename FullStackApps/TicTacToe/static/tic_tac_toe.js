window.onload = function(){

    function fill_square(){
        // fill x and send response to backend
        $(".b").click(function(){
            let text = this.textContent;
            text = (text.toString())
            console.log(text);
            //id to find
            let t_id = "b"+text;
            
            $("#" + t_id).text("X");
            // Make the X element visible to the user
            $("#" + t_id).css("background", "visible");
            $("#" + t_id).css("color", "black");
            $("#" + t_id).css("font-size", "80px");

            post_request(text, function(response){
                console.log(response);

            });
        });
    }

    function recieve_square(){
        // fill in o's with get request
        console.log("TEST");
    }

    function get_request(){
        // grab the get request

        $.ajax({
            url:'/get_square',
            type: 'GET',
            contentType: "json",
            success: function(data){
                    console.log("Response:", data);
                    alert(data);
            },
            error: function(error) {
                console.error("Error:", error);
            }

        });
    }

    function post_request(text, callback){
        // make the post request

        let dataToSend = {"button": text };

        $.ajax({
            url:'/post_square',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(dataToSend),
            success: function(response){
                    console.log("Response:", response);
            },
            error: function(error) {
                console.error("Error:", error);
            }

        });

    }

    fill_square();
    get_request();
}


