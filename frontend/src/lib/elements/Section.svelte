<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Section } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Section;
    export let info: ChatInfo;
</script>

<Element element={element.element} {info} />
