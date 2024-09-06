<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { RichTextElement } from "$lib/client";
    import Elements from "./Elements.svelte";

    export let element: RichTextElement;
    export let info: ChatInfo;
</script>

<!-- TODO: deal with overflow -->
<pre class="whitespace-pre-wrap overflow-auto bg-gray-300 rounded p-1.5"><Elements elements={element.elements} {info}></Elements></pre>
