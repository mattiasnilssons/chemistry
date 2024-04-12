<script lang="ts">
  import OverviewGrah from './OverviewGraph.svelte';
  import TopBar from './TopBar.svelte'
  export let menuItems = [];
</script>
<TopBar {menuItems} />
  <OverviewGrah />
