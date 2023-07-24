window.onload = function(){
    let game_array = [];

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
              .then(response => {
                console.log("Received data:", response);
                
                $("#b" + response["o"]).text("O");
                $("#b" + response["o"]).css("background", "visible");
                $("#b" + response["o"]).css("color", "black");
                $("#b" + response["o"]).css("font-size", "80px");
            
                // if the game is over check the board for winning indexes
                if (response["game_over"] == true){
                    //$(".b").prop("disabled", true);
                    // Example usage:
                    const ticTacToeBoard = response["board"];
                    const winningIndexes = checkWinningIndexes(ticTacToeBoard);
                    console.log("Winning indexes:", winningIndexes); 
                    console.log("game is over");
                    console.log(response["game_over"]);
                    
                    display_win(winningIndexes);

                }

              })
              .catch(error => {
                console.error('Error:', error);
              });

        });
    }

    function reset() {
        // fill x and send response to backend
        $("#replay").click(function() {
            //reset the game here
            console.log("reset the game")
            
            for (let index = 0; index<9; index++){
                $("#b" + index).css("background", "transparent");
                $("#b" + index).css("color", "white");
                $("#b" + index).text(index);
                $("#b" + index).removeClass("win");
            }
            
            //$(".b").prop("disabled", false);
            clear();
            
        });
    }


    function display_win(arr){
        arr.forEach((element) => {
            // Code to be executed for each element
            console.log(element);
            $("#b" + element).addClass("win");
          });


    }

    function clear(){
        $.ajax({
            url: "/clear_board",
            type: 'POST',
            contentType: "application/json",
            success: function(response) {
                console.log("Response:", response);
            },
        });

    }

    function checkWinningIndexes(board) {
        const winningCombinations = [
          [0, 1, 2], // Top row
          [3, 4, 5], // Middle row
          [6, 7, 8], // Bottom row
          [0, 3, 6], // Left column
          [1, 4, 7], // Middle column
          [2, 5, 8], // Right column
          [0, 4, 8], // Top-left to bottom-right diagonal
          [2, 4, 6], // Top-right to bottom-left diagonal
        ];
      
        for (const combination of winningCombinations) {
          const [i, j, k] = combination;
          if (board[i] === board[j] && board[j] === board[k]) {
            return combination; // Return the winning combination if found
          }
        }
      
        return null; // Return null if no winning combination is found
    }
    
      
    function post_request(text) {
        return new Promise((resolve, reject) => {
            let dataToSend = { "button": text };
    
            $.ajax({
                url: "/recieve_square",
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify(dataToSend),
                success: function(response) {
                    console.log("Response:", response);
                    resolve(response); // Resolve the Promise with the received data
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                    reject(error); // Reject the Promise with the error object
                }
            });
        });
    }
    

    fill_square();
    reset();

}


