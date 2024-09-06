<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Video as VideoBlock } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let element: VideoBlock;
    export let info: ChatInfo;

    let play: boolean = false;
</script>

{#if element.url && ((element.size && element.size < 500 * 1024) || play)}
    <video
        src={element.url}
        muted
        loop
        autoplay
        class="max-w-36 rounded"
        on:click={() => {
            play = false;
        }}
    />
{:else if element.thumbnail}
    <div class="relative max-w-36">
        <img
            src={element.thumbnail}
            alt={element.name ?? "video"}
            class="rounded"
        />
        <!-- overlay a play button -->
        {#if element.url}
            <div
                on:click={() => {
                    play = true;
                }}
            >
                <Icon
                    icon="grommet-icons:play"
                    class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-12 h-12 text-white hover:text-gray-300 cursor-pointer"
                />
            </div>
        {/if}
    </div>
{:else}
    <Icon icon="tabler:file-x" width="3em" height="3em" />
{/if}
