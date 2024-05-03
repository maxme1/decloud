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

<div class="flex-1 min-w-0 pb-3 sm:pb-4 bg-gray-50">
    <div class="flex justify-between">
        <p class="text-sm font-medium text-gray-900 truncate dark:text-white">
            {group[0].from}
        </p>
    </div>
    {#each group as message}
        <MessageContent {message} />
    {/each}
</div>
