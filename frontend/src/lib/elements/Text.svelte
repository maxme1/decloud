<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Text } from "$lib/client";
    import { text } from "@sveltejs/kit";

    export let element: Text;
    export let info: ChatInfo;
</script>

<span class="whitespace-pre-line">{element.text}</span>
