<script lang="ts">
    import { Tooltip } from "flowbite-svelte";
    import { timeString, type AgentMessage } from "../timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";
    import Thread from "./Thread.svelte";
    import Elements from "../elements/Elements.svelte";
    import AgentHeader from "./AgentHeader.svelte";
    import Reactions from "./Reactions.svelte";
    import type { Shared } from "$lib/client";
    import { activeChannel } from "$lib/store";
    import { base } from "$app/paths";

    export let message: AgentMessage;
    export let info: ChatInfo;
    let showShared = false;
    $: showShared = message.shared.length == 1;

    function unpackShared(shared: Shared) {
        let agent_id = shared.agent_id;
        let timestamp = shared.timestamp;
        let elements = shared.elements;
        if (
            (agent_id === null || timestamp === null || elements === null) &&
            shared.id !== null &&
            // TODO: check channel interface as well
            shared.channel_id === $activeChannel?.channel.id
        ) {
            let message = $activeChannel?.messages.find(
                (m) => m.id === shared.id,
            );
            if (message) {
                timestamp = message.timestamp;
                elements = message.elements;
                if (message.type === "agent") {
                    agent_id = message.agent_id;
                }
            }
        }

        return {
            agent_id,
            timestamp,
            elements,
            channel_id: shared.channel_id,
            message_id: shared.id,
            source: $activeChannel?.channel.source,
        };
    }
</script>

<div class="flex flex-col">
    <!-- blocks -->
    <div class="flex">
        <div>
            <Elements elements={message.elements} {info} />
        </div>

        {#if message.edited}
            <div class="text-xs text-gray-500 dark:text-gray-400 m-1 self-end">
                <div class="flex items-center">
                    <Icon icon="tabler:clock-edit" width="1em" height="1em" />
                    <small class="ml-0.5">edited</small>
                </div>
                <Tooltip>{message.edited}</Tooltip>
            </div>
        {/if}
    </div>

    <!-- reactions -->
    <Reactions reactions={message.reactions} {info}></Reactions>

    <!-- shared -->
    {#if message.shared.length > 0}
        <hr />
        <div class="flex">
            <button
                class="flex flex-row items-start hover:bg-gray-200 rounded-md p-1"
                on:click={() => {
                    showShared = !showShared;
                }}
            >
                <Icon
                    icon="fluent:calendar-reply-16-filled"
                    width="2em"
                    height="2em"
                    color="black"
                />
                {#if !showShared}
                    <div class="self-center px-1">
                        {message.shared.length} shared
                    </div>
                {/if}
            </button>

            {#if showShared}
                <div class="pl-2 bg-slate-100 w-full">
                    {#each message.shared as raw}
                        {@const shared = unpackShared(raw)}
                        <div class="flex items-center mb-3">
                            <div class="w-full">
                                <div class="flex justify-start w-full">
                                    <!-- <div class="w-10 self-start">
                                        <GroupImage {group} {info} />
                                    </div> -->
                                    <div class="ml-1 px-1 w-full mb-1">
                                        <div
                                            class="flex justify-start leading-none items-center mb-1"
                                        >
                                            {#if shared.agent_id}
                                                <AgentHeader
                                                    agent_id={shared.agent_id}
                                                    {info}
                                                />
                                            {/if}
                                            {#if shared.timestamp}
                                                <small class="px-1"
                                                    >{timeString(
                                                        shared.timestamp,
                                                    )}</small
                                                >
                                                <Tooltip
                                                    >{shared.timestamp}</Tooltip
                                                >
                                            {/if}
                                            {#if shared.channel_id && shared.message_id && shared.source}
                                                <a
                                                    class="flex flex-row items-start hover:bg-gray-200 rounded-md p-1"
                                                    href="{base}/channels/{shared.source}/{shared.channel_id}#{shared.message_id}"
                                                >
                                                    <Icon
                                                        icon="fluent:calendar-reply-16-filled"
                                                        color="black"
                                                    />
                                                </a>
                                            {/if}
                                        </div>
                                        <div
                                            class="hover:bg-gray-100 flex w-full rounded"
                                        >
                                            <div>
                                                <Elements
                                                    elements={shared.elements}
                                                    {info}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    {/if}

    <Thread messages={message.thread} {info}></Thread>
</div>
