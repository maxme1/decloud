<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Video as VideoBlock } from "$lib/client";
    import Icon from "@iconify/svelte";
    import { Video } from "flowbite-svelte";

    export let block: VideoBlock;
    export let info: ChatInfo;
</script>

{#if block.thumbnail}
    <img src={block.thumbnail} class="max-h-36 rounded" />
{:else if block.url}
    <Video src={block.url} muted loop class="max-h-36 rounded" />
{:else}
    <Icon icon="grommet-icons:document-missing" width="3em" height="3em" />
{/if}

<!-- type={message.mime_type ?? "video/mp4"} -->
