<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { File } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let element: File;
    export let info: ChatInfo;
</script>

<a
    href={element.url}
    target="_blank"
    class="flex items-center text-blue-500 cursor-pointer"
>
    {#if element.url}
        <Icon icon="tabler:file" width="3em" height="3em" />
    {:else}
        <Icon icon="tabler:file-x" width="3em" height="3em" />
    {/if}
    {#if element.name}
        <span>
            {element.name}
        </span>
    {/if}
</a>
