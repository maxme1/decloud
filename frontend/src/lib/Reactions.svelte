<script lang="ts">
    import { type ChatInfo } from "$lib";
    import { Badge } from "flowbite-svelte";
    import EmojiBase from "./EmojiBase.svelte";
    import type { Reaction } from "./client";

    export let reactions: Reaction[];
    export let info: ChatInfo;
</script>

{#if reactions.length > 0}
    <div class="flex flex-wrap">
        {#each reactions as reaction}
            <Badge color="blue" rounded
                ><EmojiBase {info} emoji={reaction.emoji} height={4} />
                {reaction.users.length}</Badge
            >
        {/each}
    </div>
{/if}
