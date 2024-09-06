<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Markdown } from "$lib/client";
    import { marked } from "marked";

    export let element: Markdown;
    export let info: ChatInfo;
</script>

<!-- TODO: element style -->
<div>{@html marked(element.text)}</div>
