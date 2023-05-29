function logout(){
    $(document).ready(function(){
        $('#logout').click(function(){   //Onclick return json to server (THIS IS THE SERVER FRAMEWORK I WILL USE!)
            $.ajax({
            url:'/logout',
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
logout();