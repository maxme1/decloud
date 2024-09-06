<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { File } from "$lib/client";
    import ZoomableImage from "$lib/ZoomableImage.svelte";
    import Icon from "@iconify/svelte";

    export let block: File;
    export let info: ChatInfo;
</script>

<a href={block.url} target="_blank" class="flex items-center text-blue-500 cursor-pointer">
    {#if block.url}
        <Icon icon="tabler:file" width="3em" height="3em" />
    {:else}
        <Icon icon="tabler:file-x" width="3em" height="3em" />
    {/if}
    {#if block.name}
        <span>
            {block.name}
        </span>
    {/if}
</a>
