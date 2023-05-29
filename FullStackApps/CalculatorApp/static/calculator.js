window.onload = function(){

    const buttons = document.querySelectorAll('button');
    const screen = document.querySelector('#screen');

    let accValuesArray;
    console.log(buttons);

    let valuesArray = [];
    function calculate(button){
    const value = button.textContent;
    if (value == "C"){
        valuesArray = [];
        screen.value = "";
    }else if(value=="="){
        screen.value = eval(accValuesArray);
    }else{
        valuesArray.push(value);
        accValuesArray = valuesArray.join('');
        screen.value = accValuesArray;
    }
    }
    buttons.forEach(button => button.addEventListener('click',() => calculate(button)));

}