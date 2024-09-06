<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { ImageElement } from "$lib/client";
    import ZoomableImage from "$lib/ZoomableImage.svelte";
    import Icon from "@iconify/svelte";

    export let element: ImageElement;
    export let info: ChatInfo;
</script>

{#if element.url}
    <ZoomableImage src={element.url} class="max-h-4" />
{:else}
    <Icon icon="tabler:file-x" width="3em" height="3em" />
{/if}
