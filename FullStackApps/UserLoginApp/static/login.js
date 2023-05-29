function canvas(){
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    var ctx = c.getContext('2d');
    ctx.fillStyle = 'black';
    ctx.fillRect(0,0,300,400);

}

function login(){
    $(document).ready(function(){
        $('#submit').click(function(){   //Onclick return json to server (THIS IS THE SERVER FRAMEWORK I WILL USE!)
            var username = $('#user').val();
            var password = $('#password').val();
            
            if (username!= "" && password!=""){
                $.ajax({
                url:'/submit',
                type: 'POST',
                data:{username:username,password:password,status:"success"},
                success: function(response){
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    }                     
                    $('.container').text(response['status']);
                }
            });  
            }else{alert("Fill in the missing parameters");}

        });

        
        $('.register').click(function(){   //Onclick return json to server (THIS IS THE SERVER FRAMEWORK I WILL USE!)
                $.ajax({
                url:'/signup-link',
                type: 'POST',
                data:{status:"success"},
                success: function(response){
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    }                     
                }
            });  
        });
    });
}

login();
canvas();