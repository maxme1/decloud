<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Quote } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Quote;
    export let info: ChatInfo;
</script>

<div class="flex">
    <div class="w-2 my-1 self-stretch bg-black rounded-xl"></div>
    <div class="ml-1">
        <Element element={element.element} {info}></Element>
    </div>
</div>
