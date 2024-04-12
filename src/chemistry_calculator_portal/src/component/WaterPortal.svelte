<script lang="ts">
  import WaterGraph from './WaterGraph.svelte';
  import TopBar from './TopBar.svelte'
  export let menuItems = [];
</script>
<TopBar {menuItems} />
  <WaterGraph />
