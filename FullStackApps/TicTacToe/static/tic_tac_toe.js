window.onload = function(){

    function get_square(){
        $(".b").click(function(){
            let text = this.textContent;
            text = (text.toString())
            console.log(text)
            post_request(text);
        });
    }

    function post_request(text){

        let dataToSend = {"button": text };

        $.ajax({
            url:'/recieve_square',
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


    get_square();
    post_request(text)
}


