<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichTextElement } from "$lib/client";
    import Elements from "./Elements.svelte";

    export let element: RichTextElement;
    export let info: ChatInfo;
</script>

<div class="flex flex-1 bg-slate-200">
    <div
        class="inline-block w-1 mx-1 rounded-xl self-stretch bg-black"
    ></div>
    <div class="">
        <Elements elements={element.elements} {info}></Elements>
    </div>
</div>
