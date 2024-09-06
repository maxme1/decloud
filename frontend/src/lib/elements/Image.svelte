<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Image } from "$lib/client";
    import ZoomableImage from "$lib/ZoomableImage.svelte";
    import Icon from "@iconify/svelte";

    export let element: Image;
    export let info: ChatInfo;
</script>

{#if element.url}
    <ZoomableImage
        src={element.url}
        alt={element.name ?? ""}
        class="max-h-48"
    />
{:else}
    <Icon icon="tabler:file-x" width="3em" height="3em" />
{/if}
