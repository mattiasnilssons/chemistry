<script lang="ts">
  export let menuItems = [];
</script>

<style>
  nav {
    background-color: #333; /* A dark background for a professional look */
    padding: 0.5rem 1rem !important;
  }

  ul {
    list-style: none !important;
    padding: 0 !important;
    margin: 0!important;
    display: flex!important;
    justify-content: center!important; /* Center menu items horizontally */
    gap: 20px!important;
  }

  li {
    padding: 0.5rem 0!important;
  }

  a {
    text-decoration: none!important;
    color: #fff!important; /* Light text color for contrast */
    padding: 0.5rem 1rem!important;
    transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out!important;
  }

  a:hover, a:focus {
    background-color: #555!important; /* A slight change on hover/focus for feedback */
    color: #ddd!important;
  }

  @media (max-width: 600px) {
    ul {
      flex-direction: column!important; /* Stack menu items on smaller screens */
    }
  }
</style>

<nav>
  <ul>
    {#each menuItems as {name, link}}
      <li>
        <a href={link}>
          {name}
        </a>
      </li>
    {/each}
  </ul>
</nav>
