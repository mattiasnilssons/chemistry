<script lang="ts">
  import MouldGraph from './MouldGraph.svelte';
  import TopBar from './TopBar.svelte'
  export let menuItems = [];
</script>
<TopBar {menuItems} />
  <MouldGraph />
