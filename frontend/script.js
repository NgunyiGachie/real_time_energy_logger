// Fetch data from the backend (API endpoint)
const fetchData = async () => {
    try {
        const response = await fetch('http://localhost:5555/energy-data');
        const data = await response.json();

        const tableBody = document.querySelector("#data-table tbody");

        tableBody.innerHTML = '';

        data.forEach(entry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.sensor_id}</td>
                <td>${entry.energy_consumption} kWh</td>
                <td>${entry.timestamp}</td>
            `;
            tableBody.appendChild(row);
        });

        updateChart(data);

    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const updateChart = (data) => {
    const labels = data.map(entry => new Date(entry.timestamp));
    const consumptionData = data.map(entry => entry.energy_consumption);

    const ctx = document.getElementById('consumption-chart').getContext('2d');
    const chart = new chart(ctx, {
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
        }
    });
};
window.onload = fetchData;

setInterval(fetchData, 10000);
