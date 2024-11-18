// Fetch data from the backend (API endpoint)
const fetchData = async () => {
    try {
        const response = await fetch('http://localhost:5555/energy-data'); // Replace with your actual endpoint
        const data = await response.json();

        // Get the table body element
        const tableBody = document.querySelector("#data-table tbody");

        // Clear previous data
        tableBody.innerHTML = '';

        // Insert the fetched data into the table
        data.forEach(entry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.sensor_id}</td>
                <td>${entry.energy_consumption} kWh</td>
                <td>${entry.timestamp}</td>
            `;
            tableBody.appendChild(row);
        });

        // Optionally: Update the chart as well if using Chart.js
        updateChart(data);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

// Update chart with energy data
const updateChart = (data) => {
    const labels = data.map(entry => new Date(entry.timestamp));
    const consumptionData = data.map(entry => entry.energy_consumption);

    const ctx = document.getElementById('consumption-chart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Energy Consumption (kWh)',
                data: consumptionData,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        });
};

// Call fetchData when the page loads
window.onload = fetchData;

// Optionally: Set an interval to fetch data every 10 seconds (real-time)
setInterval(fetchData, 10000);
