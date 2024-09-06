<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichTextList } from "$lib/client";
    import Element from "./Element.svelte";
    import Elements from "./Elements.svelte";

    export let info: ChatInfo;
    export let element: RichTextList;

    // const listComponents = {
    //     ordered: O,
    //     unordered: ul,
    // };
    if (element.style == "primary") console.log("unknown style", element.style);
</script>

<ul>
    {#each element.elements as entry, i}
        <li>
            {#if element.style == "ordered"}{i + 1}.
            {:else}-
            {/if}<Element element={entry} {info} />
        </li>
    {/each}
</ul>
