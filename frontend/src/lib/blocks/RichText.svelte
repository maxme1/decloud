<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichText } from "$lib/client";
    import Elements from "$lib/elements/Elements.svelte";

    export let block: RichText;
    export let info: ChatInfo;
</script>

<Elements elements={block.elements} {info}></Elements>
