<script lang="ts">
  // import { loading, translate, translations, translationService } from '../domain/translations';

  const translate = async (text) => {
    return text.replaceAll('_', ' ');
  };

  export let text = '';
  export let showOriginalWhileWaiting = true;

  // (async () => {
  //   if (!$translations.length) {
  //     if (!$loading) {
  //       loading.set(true);
  //       translations.set(await translationService.translations());
  //       loading.set(false);
  //     }
  //   }
  // })();

  const getTrans = async () => {
    return await translate(text);
  };

  const findTrans = async () => {
    // if ($translations.length) return getTrans();
    // if ($loading) {
    //   for (let i = 1; i < 10; i++) {
    //     await new Promise((r) => setTimeout(r, 50));
    //     if ($translations.length) return getTrans();
    //   }
    //   if ($loading) return text;
    // }
    return getTrans();
  };
</script>

{#if showOriginalWhileWaiting}
  {#await findTrans()}{text.replaceAll('_', ' ')}{:then trans}{trans}{/await}
{:else}
  {#await findTrans() then trans}{trans}{/await}
{/if}
