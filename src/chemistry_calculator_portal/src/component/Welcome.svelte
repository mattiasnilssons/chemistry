<script>
  import Trans from '../library/Trans.svelte';
</script>

<style>
  .wrapper {
    max-width: 800px; /* Max-width for optimal reading line length */
    margin-left: auto; /* Center the wrapper */
    margin-right: auto;
    padding: 2rem; /* Padding for breathing room */
    background: #fff; /* White background for the content area */
    border-radius: 5px; /* Slight rounding of corners for a modern look */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Subtle shadow for depth */
  }

  .header {
    background-color: #1f5b83; /* Primary Color */
    color: #ffffff; /* White text for contrast */
    padding: 1rem; /* More padding for a spacious header */
    border-radius: 5px 5px 0 0; /* Continue the border radius on the top of the header */
  }
  .tagline {
    margin-bottom: 1.5rem; /* Increase margin for distinct sections */
    line-height: 1.6; /* Spacing out lines for readability */
  }
</style>

<div class="wrapper">
  <div class="header">
    <h2><Trans text="Presentation av mina klimatdata"/></h2>
  </div>

  <section>
    <div class="lead"><Trans text="Här har du möjligheten att djupdyka i mina klimatdata och se hur de speglar dina förväntningar."/></div>
  <p></p>
  <div class="tagline">
    <div class="fw-bold"><Trans text="Översikt"/></div>
    <div class="form-text">
    <Trans text="På min översiktssida dras paralleller mellan klimatkurvor och dagboksanteckningar. Är förväntningarna på hur relativ fuktighet (RH) och temperatur (T) skulle förändras i linje med det dataloggern samlade in?"/>
    </div>
  </div>

    <div class="tagline">
      <div class="fw-bold"><Trans text="Mögelrisk"/></div>
      <div class="form-text">
      <Trans text="Utforska 'Mögelrisk' för att se diagram som visualiserar hur mina mätvärden står sig mot etablerade gränsvärden. Få en klar bild av riskzonen där mögeltillväxt kan bli ett problem."/>
      </div>
      </div>

    <div class="tagline">
      <div class="fw-bold"><Trans text="Vattenmängd"/></div>
      <div class="form-text">
      <Trans text="Missa inte sidan om 'Vattenmängd' som illustrerar mängden vattenånga i luften – ett viktigt verktyg för att förstå klimat på en molekylär nivå."/>
      </div>
    </div>
  <img src="gu.png" alt="Gothenburg University" id="gu-image">
  </section>
</div>
