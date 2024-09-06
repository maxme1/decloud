<script lang="ts">
    import type { SystemMessage } from "./timeline";
    import User from "./elements/User.svelte";
    import Thread from "./Thread.svelte";

    import { type ChatInfo } from "$lib";
    import { Badge } from "flowbite-svelte";
    import Elements from "./elements/Elements.svelte";
    import Reactions from "./Reactions.svelte";
    import Call from "./events/Call.svelte";

    export let message: SystemMessage;
    export let info: ChatInfo;

    const users = new Set(["join", "leave", "archive", "create"]);
    const components = new Map([["call", Call]]);
</script>

<div class="flex flex-col">
    <div>
        <Elements elements={message.elements} {info} />
    </div>

    <div class="hover:bg-gray-100 flex w-full rounded">
        <div class="text-sm text-gray-500 dark:text-gray-400">
            <span>
                {#if components.has(message.event)}
                    <svelte:component
                        this={components.get(message.event)}
                        event={message}
                        {info}
                    ></svelte:component>
                {:else if users.has(message.event)}
                    <div>
                        {#each message.agents as agent}
                            <User
                                element={{
                                    user_id: agent,
                                    type: "user",
                                    element: null,
                                }}
                                {info}
                            />
                        {/each}
                    </div>
                {:else}
                    {message.event}
                    {#each message.agents as agent}
                        <User
                            element={{
                                user_id: agent,
                                type: "user",
                                element: null,
                            }}
                            {info}
                        />
                    {/each}
                {/if}
            </span>
        </div>
    </div>

    <!-- reactions -->
    <div>
        <Reactions reactions={message.reactions} {info}></Reactions>
    </div>

    <Thread messages={message.thread ?? []} {info}></Thread>
</div>
