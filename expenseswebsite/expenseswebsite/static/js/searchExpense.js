const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tableOutputBody = document.querySelector(".table-output-body");
const noResult = document.querySelector(".no-result");

tableOutput.style.display = "none";
noResult.style.display = "none";

searchField.addEventListener('keyup', (event) => {
    const searchValue = event.target.value;

    if (searchValue.trim().length > 0) {

        tableOutputBody.innerHTML = "";

        fetch('/expense-search', {
            body: JSON.stringify({ searchText: searchValue }),
            method: 'POST',
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("data", data);

            paginationContainer.style.display = "none";
            appTable.style.display = "none";
            tableOutput.style.display = "block";

            if (data.length === 0) {
                tableOutput.style.display = "none";
                noResult.style.display = "block";
            } else {
                noResult.style.display = "none";
                data.forEach(element => {
                    tableOutputBody.innerHTML += `
                <tr>
                    <td>${element.amount}</td>
                    <td>${element.category}</td>
                    <td>${element.description}</td>
                    <td>${element.date}</td>
                </tr>
                `;
                });
            }
        })
    } else {
        paginationContainer.style.display = "block";
        appTable.style.display = "block";
        tableOutput.style.display = "none";
    }
})