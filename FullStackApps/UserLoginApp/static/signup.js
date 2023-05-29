function register(){
    $(document).ready(function(){
        $('#submit').click(function(){   //Onclick return json to server (THIS IS THE SERVER FRAMEWORK I WILL USE!)
            var newUsername = $('#newUser').val();
            var newPassword = $('#newPassword').val();
            
            if (newUsername!= "" && newPassword!=""){
                $.ajax({
                url:'/addUser',
                type: 'POST',
                data:{username:newUsername,password:newPassword,status:"success"},
                success: function(response){
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    }                     
                    //$('.container').text(JSON.stringify(response['status']));
                }
            });  
            }else{alert("Fill in the missing parameters");}

        });
    });
}
register();