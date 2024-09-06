<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Actions } from "$lib/client";
    import Elements from "$lib/elements/Elements.svelte";

    export let block: Actions;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<br />
<Elements elements={block.elements} {info}></Elements>
