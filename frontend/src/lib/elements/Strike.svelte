<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Strike } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Strike;
    export let info: ChatInfo;
</script>

<span
    class:line-through={element.position === "through"}
    class:underline={element.position === "under"}
    class:overline={element.position === "over"}
    ><Element element={element.element} {info}></Element></span
>
