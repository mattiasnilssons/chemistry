<script>
  import { writable } from "svelte/store";
  import Chart from 'chart.js/auto';
  import Trans from "../library/Trans.svelte";

  let chart;
  let chartContainer;
  let climateData = writable({});
  let riskFactor = writable(75); // Default value for the slider
  // const apiUrl = import.meta.env.VITE_BACKEND_HOST;
  const apiUrl = "http://0.0.0.0:8080";
  const humidityLevels = {
    'Låg': {
      description: 'Under 60% RH: Idealisk för att förhindra alla former av mögeltillväxt.',
      risk: 'Låg',
      baseRisk: 60,
      molds: 'De flesta mögelformer kan inte etablera sig under dessa torra förhållanden.'
    },
    'Måttlig': {
      description: '60-70% RH: Vissa mögelsorter som Aspergillus och Penicillium börjar trivas, speciellt i varmare miljöer.',
      risk: 'Måttlig',
      baseRisk: 65,
      molds: 'Aspergillus och Penicillium trivs i denna fuktighetsnivå.'
    },
    'Hög': {
      description: '70-80% RH: Mögelrisken ökar, och arter som Cladosporium och Stachybotrys (svartmögel) blir mer aktiva.',
      risk: 'Hög',
      baseRisk: 75,
      molds: 'Cladosporium och Stachybotrys (Svartmögel) blir alltmer vanliga.'
    },
    'Mycket hög': {
      description: 'Över 80% RH: Höga fuktighetsnivåer stödjer tillväxten av nästan alla mögelformer, särskilt i dåligt ventilerade områden.',
      risk: 'Mycket hög',
      baseRisk: 80,
      molds: 'Nästan alla mögelarter, inklusive de som är hälsoskadliga, kan växa ostört.'
    }
  };

  let selectedHumidityLevel = writable('');

  function handleHumiditySelection(event) {
    selectedHumidityLevel.set(event.target.value);
    riskFactor.set(humidityLevels[event.target.value].baseRisk);
    updateChart();
  }

  async function fetchMoldData() {
    console.log("apiUrl",apiUrl)
      const response = await fetch(`${apiUrl}/calculate-mould`, {
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
    return factor + 20 * Math.exp(-0.1241 * temperature);
  }

  function updateChart() {
    const data = $climateData;
    const factor = $riskFactor;

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
    <div class="row">
      <div class="col-6">
    <h2><Trans text="Välj relativ fuktighetsnivå"/></h2>
        <div class="mb-4">
    {#each Object.keys(humidityLevels) as level}
      <label class="form-check-label">
        <input type="radio" name="humidity" class="form-check-input" value={level} on:change={handleHumiditySelection}>
        {level}
      </label>
    {/each}
          </div>
        <div class="mb-4">
            <button class="btn btn-outline-primary" on:click={fetchMoldData}>Hämta mögeldata</button>
    <input type="range" min="10" max="90" value={$riskFactor} on:input={(e) => riskFactor.set(+e.target.value)}>
    <div class="lead">Riskfaktor: {$riskFactor}</div>
          </div>
        </div>
      <div class="col-6">
    {#if $selectedHumidityLevel}
      <h2>Om {$selectedHumidityLevel.toLowerCase()} fuktighetsnivå</h2>
      <div class="form-text"><b>Beskrivning:</b> {humidityLevels[$selectedHumidityLevel].description}</div>
      <div class="form-text"><b>Risk för mögel:</b> {humidityLevels[$selectedHumidityLevel].risk}</div>
      <div class="form-text"><b>Favoriserade mögelsorter:</b> {humidityLevels[$selectedHumidityLevel].molds}</div>
    {/if}
        </div>
      </div>

    <canvas bind:this={chartContainer}></canvas>
  </div>
</div>
