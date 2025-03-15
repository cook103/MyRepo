window.onload = function() {
    const $replySpan = $('.reply-data');
    const rateInput = document.getElementById('rate');
    const rateLabel = document.querySelector('label[for="growth-rate"]');

    $('#dcf').click(function(e) {
        e.preventDefault(); // Prevent default button action
        const multiple_button = document.getElementById('multiple');
        multiple_button.style.color = 'black';
        multiple_button.style.backgroundColor = 'white';
        e.target.style.backgroundColor = '#4CAF50';
        e.target.style.color = 'white'; 
        rateInput.style.display = 'inline';
        rateLabel.style.display = 'inline';
        handleModelChange('dcf');
    });

    $('#multiple').click(function(e) {
        e.preventDefault(); // Prevent default button action
        const dcf_button = document.getElementById('dcf');
        dcf_button.style.color = 'black';
        dcf_button.style.backgroundColor = 'white';
        e.target.style.backgroundColor = '#4CAF50';
        e.target.style.color = 'white'; 
        rateInput.style.display = 'none';
        rateLabel.style.display = 'none';
        handleModelChange('multiple');
    });

    $('#submit').click(function(e) {
        var ticker_input = $('#ticker').val();
        var rate_input = $('#rate').val();
        e.preventDefault(); // Prevent default button action
        submitForm(ticker_input, rate_input);
    });

    function submitForm(t, r) {
        // show loading icon and lock events
        $('#loadingIcon').show();
        $('.form-container').css('pointer-events', 'none');
        
        $.ajax({
            url: '/acceptForm',
            type: 'POST',
            dataType: 'json',
            data: { ticker: t, rate: r },
            success: function(response) {
                // form response data is received here
                const responseMap = new Map(Object.entries(response));
                if ("error" in response) {
                    console.log(response["error"]);
                    alert(response["error"]);
                } else {
                    // hide loading icon and unlock events
                    $('#loadingIcon').hide();
                    $('.form-container').css('pointer-events', '');
                    // clear out previous data if it exists
                    $replySpan.empty();
                    var model = response['model'];
                    if (model == "dcf") {
                        $replySpan.append('<h2>' + response['ticker'] + ': ' + response['over_undervalued'] + '</h2>');
                        $replySpan.append('<li>Current Price: ' + response['current_price'] + '</li>');
                        $replySpan.append('<li>Intrinsic Value: ' + response['intrinsic_value'] + '</li>');
                        $replySpan.append('<li>Wall Street Estimate: ' + response['wall_street_estimate'] + '</li>');
                        $replySpan.append('<p>Margin of Safety Increments</p>');
                        const mosMap = new Map(Object.entries(response['intrinsic_value_with_mos']));
                        for (const [k, v] of mosMap) {
                            $replySpan.append('<li>' + k + ': ' + v + '</li>');
                        }
                        $replySpan.append('<br>');
                    } else if (model == "multiple") {
                        $replySpan.append('<h2>' + response['ticker'] + ': ' + response['over_undervalued'] + '</h2>');
                        $replySpan.append('<li>Current Price: ' + response['current_price'] + '</li>');
                        $replySpan.append('<li>Intrinsic Value: ' + response['intrinsic_value'] + '</li>');
                        $replySpan.append('<li>Wall Street Estimate: ' + response['wall_street_estimate'] + '</li>');
                        $replySpan.append('<br>');
                    } else {
                        console.log('Error: invalid return reponse received');
                    }
                }
            },
            error: function(error) {
                // hide loading icon and unlock events
                $('#loadingIcon').hide();
                $('.form-container').css('pointer-events', '');
                console.log('Error:', error);
                alert('There was an error submiting your request.');
            }
        });
    }

    function handleModelChange(button) {
        $.ajax({
            url: '/handle_model_change',
            type: 'POST',
            dataType: 'json',
            data: { selected_button: button },
            success: function(response) {
                // clear the reply if model change
                $replySpan.empty();
                if ("error" in response) {
                    console.log(response["error"]);
                    alert(response["error"])
                } 
            },
            error: function(error) {
                console.log('Error:', error);
                alert('There was an error processing your request.');
            }
        });
    }
}
