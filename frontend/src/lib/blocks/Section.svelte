<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Section } from "$lib/client";
    import Elements from "$lib/elements/Elements.svelte";

    export let block: Section;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<div>
    <Elements elements={block.elements} {info}></Elements>
</div>
