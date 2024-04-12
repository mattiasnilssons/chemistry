<script>
  import { writable } from "svelte/store";
  import Chart from 'chart.js/auto';

  let chart;
  let chartContainer;
  let climateData = writable({});
  let riskFactor = writable(20); // Default value for the slider

  async function fetchMoldData() {
    const response = await fetch('http://localhost:8080/calculate-mould', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'}
    });
    if (response.ok) {
      const data = await response.json();
      climateData.set(data);
      updateChart();
    } else {
      console.error('Failed to fetch data:', await response.text());
    }
  }

  function calculateMoldRisk(RH, temperature, factor) {
    return factor + RH + 0.5 * temperature; // Use factor from the slider
  }

  function updateChart() {
    const data = $climateData; // Using the store's auto-subscription feature
    const factor = $riskFactor; // Dynamic risk factor from the slider

    if (data && data.temperatures && data.humidity) {
      const temperatures = Object.values(data.temperatures);
      const humidity = Object.values(data.humidity);
      const moldRisks = humidity.map((rh, index) => calculateMoldRisk(rh, temperatures[index], factor));

      if (chart) {
        chart.data.labels = temperatures;
        chart.data.datasets[0].data = humidity;
        chart.data.datasets[1].data = moldRisks;
        chart.update();
      } else {
        chart = new Chart(chartContainer, {
          type: 'scatter',
          data: {
            labels: temperatures,
            datasets: [{
              label: 'Relative Humidity (%RH)',
              data: humidity.map((h, i) => ({ x: temperatures[i], y: h })),
              backgroundColor: 'blue'
            }, {
              label: 'Mold Risk',
              data: moldRisks.map((m, i) => ({ x: temperatures[i], y: m })),
              backgroundColor: 'red'
            }]
          },
          options: {
            scales: {
              x: {
                type: 'linear',
                position: 'bottom'
              },
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    }
  }
</script>

<div class="container">
  <div class="main-content">
    <button on:click={fetchMoldData}>Fetch Mold Data</button>
    <input type="range" min="10" max="30" value={$riskFactor} on:input={(e) => riskFactor.set(+e.target.value)}>
    <p>Risk Factor: {$riskFactor}</p>
    <canvas bind:this={chartContainer}></canvas>
  </div>
</div>
