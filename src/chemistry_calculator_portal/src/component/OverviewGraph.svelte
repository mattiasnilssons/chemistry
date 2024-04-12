<script>

  import Chart from 'chart.js/auto';
  import {get, writable} from "svelte/store";

  let chart;
  let chartContainer;
  let climateData = writable({});

  async function fetchMoldData() {
    try {
      const response = await fetch('http://localhost:8080/calculate-mould', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Data", data)
        climateData.set(data);
        updateChart();
      } else {
        throw new Error('Failed to fetch');
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  }

  function calculateMoldRisk(RH, temperature) {
    return 20 + RH + 0.5 * temperature; // Simplified example formula
  }

  function updateChart() {
    const data = get(climateData); // Assuming you store fetched data into a Svelte store
    console.log(data); // Check the structure here

    if (!data || typeof data !== 'object') {
        console.error('Invalid or no data available');
        return;
    }

    // Assuming data is structured with these specific object keys
    try {
        const dates = data.dates ? Object.values(data.dates) : [];
        const temperatures = data.temperatures ? Object.values(data['temperatures']) : []; // Example of accessing the °C data
        const humidity = data.humidity ? Object.values(data['humidity']) : []; // Accessing the %RH data

        const moldRisks = humidity.map((rh, index) => calculateMoldRisk(rh, temperatures[index]));

        if (chart) {
            chart.data.labels = dates;
            chart.data.datasets[0].data = temperatures;
            chart.data.datasets[1].data = moldRisks;
            chart.update();
        } else {
            chart = new Chart(chartContainer, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Temperature (°C)',
                        data: temperatures,
                        borderColor: 'blue'
                    }, {
                        label: 'Mold Risk',
                        data: moldRisks,
                        borderColor: 'red'
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error processing data:', error);
    }
}
</script>
<div class="container">
  <div class="main-content">
<button class="btn btn-outline-success" on:click={fetchMoldData}>Fetch Mold Data</button>
<canvas bind:this={chartContainer}></canvas>
</div>
</div>