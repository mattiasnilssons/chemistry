<script>
  import Chart from 'chart.js/auto';
  import { writable, get } from 'svelte/store';
  import annotationPlugin from 'chartjs-plugin-annotation';
  import 'chartjs-adapter-date-fns';

  const apiUrl = import.meta.env.VITE_BACKEND_HOST;
  Chart.register(annotationPlugin);

  let chart;
  let chartContainer;
  let climateData = writable({});
  let selectedEventIndex = writable(-1);

  const events = [
    { time: '2024-03-26T12:00', description: 'I klassrummet (labbsalen) ligger på bänken' },
    { time: '2024-03-26T19:00', description: 'Transport (i väska)' },
    { time: '2024-03-26T20:30', description: 'Hotellrum' },
    { time: '2024-03-27T08:30', description: 'Dusch' },
    { time: '2024-03-27T10:20', description: 'Transport (i väska)' },
    { time: '2024-03-27T11:00', description: 'Förvaring i skåp (i väska)' },
    { time: '2024-03-27T16:00', description: 'Transport (i väska)' },
    { time: '2024-03-27T23:20', description: 'Ställd i ett rum i Uppsala' },
    { time: '2024-03-30T10:18', description: 'Ställd i ett badrum' },
    { time: '2024-03-31T13:10', description: 'Flyg till Berlin' },
    { time: '2024-04-04T07:20', description: 'Flyg till Munchen' },
    { time: '2024-04-04T09:15', description: 'Flyg till Göteborg' },
    { time: '2024-04-07T18:30', description: 'Svettiga springkläder lagda i samma fack som transponder' },
    { time: '2024-04-08T17:52', description: 'Ställd på ett bord i Linne-hostel' },
    { time: '2024-04-11T08:40', description: 'Transport till GU' },
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
    if (!data || !data.Unit || !data.humidity) {
      console.error('Invalid or no data available');
      return;
    }

    const dates = Object.values(data.Unit).map(date => new Date(date));
    const temperatures = Object.values(data.temperatures);
    const humidity = Object.values(data.humidity);
    const currentIndex = get(selectedEventIndex);

    const eventAnnotations = events.map((event, index) => ({
      type: 'line',
      mode: 'vertical',
      scaleID: 'x',
      value: new Date(event.time),
      borderColor: currentIndex === index ? 'red' : 'orange',
      borderWidth: currentIndex === index ? 4 : 2,
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

  function selectEvent(index) {
    selectedEventIndex.set(index);
    updateChart();
  }
</script>

<style>
  li.selected {
    color: red;
    font-weight: bold;
  }
</style>

  <div class="main-content">
    <div class="row">
      <div class="col-2">
    <button on:click={fetchMoldData}>Hämta klimatdata</button>
    <ul>
      {#each events as event, index}
        <div class="form-text"><li class:selected={index === $selectedEventIndex} on:click={() => selectEvent(index)}>{event.description}</li></div>
      {/each}
    </ul>
        </div>
      <div class="col-9">
    <canvas bind:this={chartContainer}></canvas>
        </div>
      </div>
  </div>
