<script lang="ts">
    import { Indicator, Avatar, Badge, Img, Video } from "flowbite-svelte";
    import InfiniteScroll from "svelte-infinite-scroll";
    import { List, Li } from "flowbite-svelte";
    import { onMount } from "svelte";
    import type { Message } from "./timeline";
    import { filesRoot } from "$lib";
    import MessageContent from "./MessageContent.svelte";

    export let group: Message[];
</script>

<div class="flex-1 min-w-0">
    <div class="flex justify-between">
        <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
            {group[0].from}
        </p>
    </div>
    {#each group as message}
        <MessageContent {message} />
    {/each}

    <!-- </p> -->
</div>

<!-- <div
                    class="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white"
                >
                    $320
                </div> -->
