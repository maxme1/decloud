<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Icon as IconElement } from "$lib/client";
    import ZoomableImage from "$lib/ZoomableImage.svelte";
    import Icon from "@iconify/svelte";

    export let element: IconElement;
    export let info: ChatInfo;
</script>

{#if element.url}
    <ZoomableImage src={element.url} class="h-4 m-0.5" />
{:else}
    <Icon icon="tabler:file-x" width="1.5em" height="1.5em" class="m-0.5" />
{/if}
