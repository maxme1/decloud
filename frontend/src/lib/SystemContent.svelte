<script lang="ts">
    import type { SystemMessage } from "./timeline";
    import User from "./elements/User.svelte";
    import Thread from "./Thread.svelte";

    import { type ChatInfo } from "$lib";
    import Blocks from "./blocks/Blocks.svelte";
    import { Badge } from "flowbite-svelte";
    import EmojiBase from "./EmojiBase.svelte";

    export let message: SystemMessage;
    export let info: ChatInfo;

    const users = new Set(["join", "leave"]);
</script>

<div class="flex flex-col">
    <div>
        <Blocks blocks={message.blocks} {info} />
    </div>

    <div class="hover:bg-gray-100 flex w-full rounded">
        <div class="text-sm text-gray-500 dark:text-gray-400">
            <span>
                {#if message.event == "call"}{:else if users.has(message.event)}
                    <div>
                        {#each message.agents as agent}
                            <User
                                element={{ user_id: agent, type: "user" }}
                                {info}
                            />
                        {/each}
                    </div>
                {:else}
                    {message.event}
                    {#each message.agents as agent}
                        <User
                            element={{ user_id: agent, type: "user" }}
                            {info}
                        />
                    {/each}
                {/if}
            </span>
        </div>
    </div>

    <!-- reactions -->
    <div>
        {#if message.reactions.length > 0}
            <div class="flex flex-wrap">
                {#each message.reactions as reaction}
                    <Badge color="blue" rounded
                        ><EmojiBase {info} emoji={reaction.emoji} height={4} />
                        {reaction.users.length}</Badge
                    >
                {/each}
            </div>
        {/if}
    </div>

    <Thread messages={message.thread ?? []} {info}></Thread>
</div>
