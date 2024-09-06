<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichText, Sequence } from "$lib/client";
    import Elements from "./Elements.svelte";

    export let element: Sequence;
    export let info: ChatInfo;
</script>

<Elements elements={element.elements} {info}></Elements>
