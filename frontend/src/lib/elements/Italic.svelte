<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Italic } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Italic;
    export let info: ChatInfo;
</script>

<span class="italic"><Element element={element.element} {info}></Element></span>
