<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Link } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Link;
    export let info: ChatInfo;
</script>

<a href={element.url} class="text-blue-500"
    >{#if element.element}<Element
            element={element.element}
            {info}
        />{:else}{element.url}{/if}</a
>
