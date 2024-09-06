<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Button as ButtonElement } from "$lib/client";
    import { Button } from "flowbite-svelte";
    import Element from "./Element.svelte";

    export let element: ButtonElement;
    export let info: ChatInfo;
</script>

<Button color="green">
    <Element element={element.text} {info}></Element>
</Button>
