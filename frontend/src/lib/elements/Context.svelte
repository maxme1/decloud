<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Context } from "$lib/client";
    import Elements from "$lib/elements/Elements.svelte";

    export let element: Context;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<div class="text-sm flex">
    <Elements elements={element.elements} {info}></Elements>
</div>
