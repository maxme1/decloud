<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Bold } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Bold;
    export let info: ChatInfo;
</script>

<span class="font-bold"
    ><Element element={element.element} {info}></Element></span
>
