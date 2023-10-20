const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");

let myChart;

function updateChart() {
  const startDate = moment(startDateInput.value);
  const endDate = moment(endDateInput.value);

  const filteredData = data.filter(item => {
    const date = moment(item.date); // Assuming you have a "date" property in your data
    return date.isSameOrAfter(startDate, 'day') && date.isSameOrBefore(endDate, 'day');
  });

  // Update the chart data and options
  myChart.data.datasets[0].data = filteredData;
  myChart.update();
}

// Initialize the chart
document.addEventListener('DOMContentLoaded', function() {
  myChart = new Chart(document.getElementById('myChart').getContext('2d'), {
    type: 'line',
    data: data,
    options: options
  });
});

// Add event listeners to date inputs
startDateInput.addEventListener('change', updateChart);
endDateInput.addEventListener('change', updateChart);