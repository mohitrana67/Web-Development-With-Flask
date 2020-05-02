

var createSudokuButton = document.getElementById("createSudoku");

createSudokuButton.addEventListener("click",createSudoku);

function createSudoku(){
    console.log("So you want to create a sudoku");
    // let's create a sudoku
    // var table = document.getElementById("sudokuTable");

    // var row = table.insertRow(0);

    // var cell1 = row.insertCell(0);
    // var cell2 = row.insertCell(1);

    // cell1.innerHTML = "New Cell 1"
    // cell2.innerHTML = "New Cell 2"
    var tableRef = document.getElementById('sudokuTable').getElementsByTagName('tbody')[0];
    var i;
    for(i = 0; i <9; i++){
        var newRow = tableRef.insertRow();
        var j;
        for(j=0;j<9;j++){
            var newCell = newRow.insertCell(j);

            // Append a text node to the cell
            var newText  = document.createTextNode(j);
            newCell.appendChild(newText);
            newCell.classList.add("numberCell")
        }
        // var newCell = newRow.insertCell(0);

        // // Append a text node to the cell
        // var newText  = document.createTextNode('New row');
        // newCell.appendChild(newText);
    }   

    createSudokuButton.classList.add('disappear')

}