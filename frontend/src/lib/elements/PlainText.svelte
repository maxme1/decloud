<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { PlainText } from "$lib/client";

    export let element: PlainText;
    export let info: ChatInfo;
</script>

<!-- TODO emoji? -->
<span class="whitespace-pre-line">{element.text}</span>
