<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Icon as IconElement } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let element: IconElement;
    export let info: ChatInfo;
</script>

{#if element.url}
    <img src={element.url} class="h-4 m-0.5" alt={element.name ?? ""} />
{:else}
    <Icon icon="tabler:file-x" width="1.5em" height="1.5em" class="m-0.5" />
{/if}
