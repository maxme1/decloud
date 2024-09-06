<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichText } from "$lib/client";
    import Element from "./Element.svelte";

    export let elements: RichText["elements"];
    export let info: ChatInfo;
</script>

{#each elements as element}<Element {element} {info} />{/each}
