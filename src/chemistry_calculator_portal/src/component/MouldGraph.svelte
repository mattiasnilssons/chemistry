<script>
  import { writable } from "svelte/store";
  import Chart from 'chart.js/auto';
  import Trans from "../library/Trans.svelte";

  let chart;
  let chartContainer;
  let climateData = writable({});
  let loading = writable(false);
  let error = writable('');
  let riskFactor = writable(75); // Default value for the slider
  const apiUrl = "https://chemistry-xopabutmga-ez.a.run.app/"; // e.g., "https://chemistry-xopabutmga-ez.a.run.app/";

  const humidityLevels = {
    'Låg': {
      description: 'Under 60% RH: Idealisk för att förhindra alla former av mögeltillväxt.',
      risk: 'Låg',
      baseRisk: 55,
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
    loading.set(true);
    error.set('');
    try {
      const response = await fetch(`${apiUrl}/calculate-mould`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
      });
      if (response.ok) {
        const data = await response.json();
        climateData.set(data);
        updateChart();
      } else {
        throw new Error('Failed to fetch mold data: ' + response.status);
      }
    } catch (e) {
      error.set(e.message);
    } finally {
      loading.set(false);
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
              label: 'Relativ fuktighet (%RH)',
              data: humidity.map((h, i) => ({ x: temperatures[i], y: h })),
              backgroundColor: 'blue'
            }, {
              label: 'Mögelrisk',
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
  const showMoldInfo = writable(false);

  const moldInformation = {
    Aspergillus: 'Ofta funnen på väggar, isolering och pappersprodukter. Kan växa vid lägre fuktighetsnivåer men trivs vid högre fuktighet.',
    Cladosporium: 'Typiskt funnen på tyger och träytor, kan växa i både svala och varma förhållanden.',
    Penicillium: 'Vanligt förekommande i mattor, tapeter och isolering, föredrar måttliga till höga fuktighetsnivåer.',
    Stachybotrys: 'Känd som "svartmögel", ofta funnen på vattenskadade byggnadsmaterial och kräver konstant hög fuktighet för att växa.'
  };
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
    <div class="lead">%RH: {$riskFactor}</div>
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
      <button class="btn btn-outline-primary" on:click={() => showMoldInfo.set(! $showMoldInfo)}>Om mögel</button>

{#if $showMoldInfo}
  <div>
      <!--    <h3>Information om Mögel</h3>-->
    <div class="form-text"><strong>Aspergillus:</strong> {moldInformation.Aspergillus}</div>
    <div class="form-text"><strong>Cladosporium:</strong> {moldInformation.Cladosporium}</div>
    <div class="form-text"><strong>Penicillium:</strong>{moldInformation.Penicillium}</div>
    <div class="form-text"><strong>Stachybotrys:</strong>{moldInformation.Stachybotrys}</div>
  </div>
{/if}

  </div>
</div>
