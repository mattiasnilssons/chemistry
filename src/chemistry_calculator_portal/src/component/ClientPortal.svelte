<script lang="ts">

  import Welcome from './Welcome.svelte';
  import TopBar from './TopBar.svelte'
  export let menuItems = [];
</script>
<TopBar {menuItems} />
  <Welcome />
