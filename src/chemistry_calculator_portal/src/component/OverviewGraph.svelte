<script>
  import Chart from 'chart.js/auto';
  import { writable, get } from "svelte/store";
  import annotationPlugin from 'chartjs-plugin-annotation'; // Ensure you've installed this
  import 'chartjs-adapter-date-fns'; // Import the adapter

  Chart.register(annotationPlugin); // Register the annotation plugin globally

  let chart;
  let chartContainer;
  let climateData = writable({});

  const events = [
    { time: '2024-03-26T12:00', description: 'I klassrummet (labbsalen) ligger på bänken' },
    { time: '2024-03-26T19:00', description: 'Transport (i väska)' },
    // Add all other events following the same format
    { time: '2024-04-11T09:55', description: 'Ställd i klassrummet' }
  ];

  async function fetchMoldData() {
    const response = await fetch('http://localhost:8080/calculate-mould', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (response.ok) {
      const data = await response.json();
      console.log("Data",data)
      climateData.set(data);
      updateChart();
    } else {
      console.error('Failed to fetch data:', await response.text());
    }
  }

  function calculateMoldRisk(RH, temperature) {
    return 20 + RH + 0.5 * temperature; // Simplified example formula
  }

  function updateChart() {
    const data = get(climateData);
    if (!data || !data.temperatures || !data.humidity) {
      console.error('Invalid or no data available');
      return;
    }

    // Ensure dates are properly converted and formatted
    const dates = Object.keys(data.temperatures).map(date => new Date(date));
    const temperatures = Object.values(data.temperatures).map(temp => temp || 0);  // Fallback for undefined values
    const humidity = Object.values(data.humidity).map(hum => hum || 0);  // Fallback for undefined values

    const moldRisks = humidity.map((rh, index) => calculateMoldRisk(rh, temperatures[index]));

    // Adjust event annotations and ensure valid date formatting
    const eventAnnotations = events.map(event => ({
      type: 'line',
      mode: 'vertical',
      scaleID: 'x',
      value: new Date(event.time),
      borderColor: 'orange',
      borderWidth: 2,
      label: {
        enabled: true,
        content: event.description,
        backgroundColor: 'rgba(255, 204, 0, 0.8)',
        position: "top"
      }
    }));

    if (chart) {
      chart.data.labels = dates;
      chart.data.datasets[0].data = temperatures;
      chart.data.datasets[1].data = moldRisks;
      chart.options.plugins.annotation.annotations = eventAnnotations;
      chart.update();
    } else {
      Chart.register(annotationPlugin);
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
            x: {
              type: 'time',
              time: {
                parser: date => new Date(date),  // Use a custom parser to handle date conversion
                tooltipFormat: 'yyyy-MM-dd HH:mm',
                unit: 'day'
              },
              position: 'bottom'
            },
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            annotation: {
              annotations: eventAnnotations
            }
          }
        }
      });
    }
}

</script>

<div class="container">
  <div class="main-content">
    <button on:click={fetchMoldData}>Hämta klimatdata</button>
    <canvas bind:this={chartContainer}></canvas>
  </div>
</div>
