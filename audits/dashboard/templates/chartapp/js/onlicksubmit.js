document.addEventListener('DOMContentLoaded', function () {
    const dateForm = document.getElementById('dateForm');
    const submitBtn = document.getElementById('submitBtn');
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    
    // Function to load and render the bar graph
    function loadBarGraph() {
        // Fetch data from your Django view
        fetch('/dashboard/display_severitydata/')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('barGraphContainer').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: [{% for product in app_data %} '{{ product.appd_application_name }}', {% endfor %}],
                        datasets: [{
                            label: 'Data',
                            data: [{% for product in app_data %} '{{ product.apps_count }}', {% endfor %}],
                            backgroundColor: 'rgba(75, 192, 192, 0.2)'
                        }]
                    },
                });
            });
    }

    // Attach an event listener to the form's submit event
    dateForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        // Validate the start and end dates, you can use JavaScript Date methods for this
        if (startDate && endDate) {
            // Activate the submit button and load the graph
            submitBtn.disabled = false;
            loadBarGraph();
        } else {
            alert("Please enter valid start and end dates.");
        }
    });
});
