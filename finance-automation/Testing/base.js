var createSudokuButton = document.getElementById("createSudoku");

// createSudokuButton.addEventListener("click",createSudoku);

document.onload = createSudoku();

function createSudoku(){
    console.log("So you want to create a sudoku");
    var tableRef = document.getElementById('sudokuTable').getElementsByTagName('tbody')[0];
    var i;
    for(i = 0; i <9; i++){
        var newRow = tableRef.insertRow();
        var j;
        for(j=0;j<9;j++){
            var newCell = newRow.insertCell(j);

            var e = i+","+j

            var randomNumber = Math.floor(Math.random()*10);

            var randomBoxSelector = Math.floor((Math.random()*10))

            numberToPutIn = 0
            if(randomBoxSelector*randomNumber>=9){
                numberToPutIn = randomNumber
                var newText  = document.createTextNode(numberToPutIn);

                newCell.appendChild(newText);   
            }else{
                var x = document.createElement("INPUT");

                x.setAttribute("type", "text");
                x.setAttribute("placeholder", "")

                newCell.appendChild(x);
            }
            newCell.classList.add("numberCell")
        }
    }   

    createSudokuButton.classList.add('disappear')

}