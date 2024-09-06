<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Actions } from "$lib/client";
    import Elements from "$lib/elements/Elements.svelte";

    export let element: Actions;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<br />
<Elements elements={element.elements} {info}></Elements>
