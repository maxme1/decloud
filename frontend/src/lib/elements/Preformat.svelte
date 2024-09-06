<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Preformat } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Preformat;
    export let info: ChatInfo;
</script>

<span class="whitespace-pre-line bg-gray-300 rounded p-1.5"
    ><Element element={element.element} {info}></Element></span
>
