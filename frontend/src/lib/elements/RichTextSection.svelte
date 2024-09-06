<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichTextElement } from "$lib/client";
    import Elements from "./Elements.svelte";

    export let info: ChatInfo;
    export let element: RichTextElement;
</script>

<Elements elements={element.elements} {info}></Elements>
