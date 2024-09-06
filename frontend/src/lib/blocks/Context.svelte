<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Context } from "$lib/client";
    import Elements from "$lib/elements/Elements.svelte";

    export let block: Context;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<div class="text-sm flex">
    <Elements elements={block.elements} {info}></Elements>
</div>
