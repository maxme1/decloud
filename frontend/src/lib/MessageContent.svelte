<script lang="ts">
    import { Tooltip } from "flowbite-svelte";
    import { timeString, type AgentMessage } from "./timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";
    import Thread from "./Thread.svelte";
    import Elements from "./elements/Elements.svelte";
    import AgentHeader from "./AgentHeader.svelte";
    import Reactions from "./Reactions.svelte";

    export let message: AgentMessage;
    export let info: ChatInfo;
    let showShared = message.shared.length == 1;
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
                    {#each message.shared as shared}
                        <div class="flex items-center mb-3">
                            <div class="w-full">
                                <div class="flex justify-start w-full">
                                    <!-- <div class="w-10 self-start">
                                        <GroupImage {group} {info} />
                                    </div> -->
                                    <div class="ml-1 px-1 w-full mb-1">
                                        {#if shared.timestamp}
                                            <div
                                                class="flex justify-start leading-none items-center mb-1"
                                            >
                                                <AgentHeader
                                                    agent_id={shared.agent_id}
                                                    {info}
                                                />
                                                <small class="px-1"
                                                    >{timeString(
                                                        shared.timestamp,
                                                    )}</small
                                                >
                                                <Tooltip
                                                    >{shared.timestamp}</Tooltip
                                                >
                                            </div>
                                        {/if}
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

<!-- <div class="absolute bottom-0 right-0 flex">
        <small class="time-child bg-white rounded px-1"
            >{message.timestamp}</small
        >

        {#if hasBadge}
            <Badge color="dark" rounded class="px-2.5 py-0.5 ml-auto relative">

                {#if message.reply_to_message_id !== undefined}
                    <div class="flex items-center badge-parent">
                        <ReplyOutline size="xs" class="me-1" />
                        <span class="badge-child">Replied</span>
                    </div>
                {/if}


            </Badge>
        {/if}
    </div> -->
