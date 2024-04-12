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
    background-color: darkolivegreen; /* Primary Color */
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
    <div class="lead"><Trans text="This tool is designed to provide you with an estimate of how the HeatBooster technology will perform in various applications."/></div>
  <p></p>
  <div class="tagline">
    <div class="fw-bold"><Trans text="Heat Source"/></div>
    <div class="form-text">
    <Trans text="Identify 'Waste Heat' or 'Process Cooling' at your facility. Specify the medium (e.g., Water) and temperatures. In the absence of exact Outlet Temperature data, outlet temperatures will be automatically estimated."/>
    </div>
  </div>

    <div class="tagline">
      <div class="fw-bold"><Trans text="Heat Sink"/></div>
      <div class="form-text">
      <Trans text="Designate 'Useful Heat' or 'Process Heat'. Specify the medium (e.g., Steam) and temperatures. In the absence of exact Inlet Temperature data, inlet temperatures will be automatically estimated."/>
      </div>
      </div>

    <div class="tagline">
      <div class="fw-bold"><Trans text="Heat Pump Details"/></div>
      <div class="form-text">
      <Trans text="Select your Heat Pump model. The HBL4 unit offers a production capacity of up to 2.0 MW, while the HBL16 unit can deliver as much as 8.0 MW. These units operate efficiently within an RPM range of 450 to 1500. All refrigerants have GWP less than 10."/>
      </div>
    </div>

    <div class="tagline">
      <div class="fw-bold"><Trans text="Project Configuration"/></div>
      <div class="form-text">
      <Trans text="Specify the number of Heat Pumps required. For large temperature lifts (about 70°C), 2-stage units may be necessary."/>
      </div>
    </div>

  </section>
</div>
