const renderChart = (data, labels) => {
    var ctx = document.getElementById('myChart').getContext('2d');

    // Create a new Chart instance
    var myChart = new Chart(ctx, {
        type: 'doughnut', // Specify the chart type
        data: {
            labels: labels,
            datasets: [{
                label: 'Income (Last 6 months)', // The label for the dataset (legend label)
                data: data, // Data points for each label
                backgroundColor: [ // Background color for each segment
                    'rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 
                    'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 71, 0.2)', 'rgba(255, 140, 0, 0.2)', 'rgba(255, 215, 0, 0.2)',
                    'rgba(154, 205, 50, 0.2)', 'rgba(0, 128, 0, 0.2)', 'rgba(0, 255, 127, 0.2)',
                    'rgba(64, 224, 208, 0.2)', 'rgba(0, 191, 255, 0.2)', 'rgba(70, 130, 180, 0.2)',
                    'rgba(123, 104, 238, 0.2)', 'rgba(255, 20, 147, 0.2)', 'rgba(199, 21, 133, 0.2)',
                    'rgba(220, 20, 60, 0.2)', 'rgba(255, 69, 0, 0.2)', 'rgba(50, 205, 50, 0.2)',
                    'rgba(0, 255, 255, 0.2)', 'rgba(25, 25, 112, 0.2)', 'rgba(128, 0, 128, 0.2)',
                    'rgba(255, 0, 255, 0.2)', 'rgba(139, 0, 139, 0.2)', 'rgba(255, 105, 180, 0.2)',
                    'rgba(255, 228, 225, 0.2)', 'rgba(105, 105, 105, 0.2)', 'rgba(169, 169, 169, 0.2)'
                ],
                borderColor: [ // Border color for each segment
                    'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 
                    'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 71, 1)', 'rgba(255, 140, 0, 1)', 'rgba(255, 215, 0, 1)',
                    'rgba(154, 205, 50, 1)', 'rgba(0, 128, 0, 1)', 'rgba(0, 255, 127, 1)',
                    'rgba(64, 224, 208, 1)', 'rgba(0, 191, 255, 1)', 'rgba(70, 130, 180, 1)',
                    'rgba(123, 104, 238, 1)', 'rgba(255, 20, 147, 1)', 'rgba(199, 21, 133, 1)',
                    'rgba(220, 20, 60, 1)', 'rgba(255, 69, 0, 1)', 'rgba(50, 205, 50, 1)',
                    'rgba(0, 255, 255, 1)', 'rgba(25, 25, 112, 1)', 'rgba(128, 0, 128, 1)',
                    'rgba(255, 0, 255, 1)', 'rgba(139, 0, 139, 1)', 'rgba(255, 105, 180, 1)',
                    'rgba(255, 228, 225, 1)', 'rgba(105, 105, 105, 1)', 'rgba(169, 169, 169, 1)'
                ],
                borderWidth: 1 // Border width for each segment
            }]
        },
        options: {
            title: {
                display: true,
                text: "Income Category"
            }
        }
    });
}

const getChartData = () => {
fetch('/income/income-summary')
.then(response => response.json())
.then((results) => {
    console.log({'results': results});
    const categoryData = results.income_category_data;
    const [labels, data] = [Object.keys(categoryData), Object.values(categoryData)];
    renderChart(data, labels);
})
}

document.onload = getChartData();