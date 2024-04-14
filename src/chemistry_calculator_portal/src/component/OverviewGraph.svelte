<script>
  import Chart from 'chart.js/auto';
  import { writable, get } from "svelte/store";
  import annotationPlugin from 'chartjs-plugin-annotation';
  import 'chartjs-adapter-date-fns';
  const apiUrl = import.meta.env.VITE_BACKEND_HOST;
  Chart.register(annotationPlugin);

  let chart;
  let chartContainer;
  let climateData = writable({});

  // Define the events for annotations
  const events = [
    { time: '2024-03-26T12:00', description: 'I klassrummet (labbsalen) ligger på bänken' },
    { time: '2024-03-26T19:00', description: 'Transport (i väska)' },
    { time: '2024-04-11T09:55', description: 'Ställd i klassrummet' }
  ];

  async function fetchMoldData() {
    const response = await fetch(`${apiUrl}/calculate-mould`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    if (response.ok) {
      const data = await response.json();
      climateData.set(data);
      updateChart();
    } else {
      console.error('Failed to fetch data:', await response.text());
    }
  }

  function updateChart() {
    const data = get(climateData);
    console.log("Data",data)
    if (!data || !data.temperatures || !data.humidity) {
      console.error('Invalid or no data available');
      return;
    }

    const dates = Object.keys(data.temperatures).map(date => new Date(date));
    const temperatures = Object.values(data.temperatures);
    const humidity = Object.values(data.humidity);

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
      chart.data.datasets[1].data = humidity;
      chart.options.plugins.annotation.annotations = eventAnnotations;
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
            label: 'Relativ fuktighet (%RH)',
            data: humidity,
            borderColor: 'red'
          }]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                parser: 'yyyy-MM-ddTHH:mm', // Ensure this matches your date input format
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
