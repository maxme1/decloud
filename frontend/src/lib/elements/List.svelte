<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { List as ListElement } from "$lib/client";
    import { Li, List } from "flowbite-svelte";
    import Element from "./Element.svelte";

    export let info: ChatInfo;
    export let element: ListElement;
</script>

<List tag={element.style === "ordered" ? "ol" : "ul"}>
    {#each element.elements as entry, i}
        <Li>
            <Element element={entry} {info} />
        </Li>
    {/each}
</List>
