<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Code } from "$lib/client";
    import Element from "./Element.svelte";

    export let element: Code;
    export let info: ChatInfo;
</script>

<!-- TODO: deal with overflow -->
<!-- TODO: language -->
<pre
    class="whitespace-pre-wrap overflow-auto bg-gray-300 rounded p-1.5"><Element
        element={element.element}
        {info}></Element></pre>
