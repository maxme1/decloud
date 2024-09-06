<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Header } from "$lib/client";
    import Element from "$lib/elements/Element.svelte";

    export let element: Header;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<div class="font-semibold">
    <Element element={element.text} {info}></Element>
</div>
