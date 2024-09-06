<script lang="ts">
    import type { AgentMessage } from "./timeline";
    import { type ChatInfo } from "$lib";
    import MessageContent from "./MessageContent.svelte";
    import type { Agent } from "./client";
    import { Tooltip } from "flowbite-svelte";
    import Icon from "@iconify/svelte";

    export let group: AgentMessage[];
    export let agent: Agent | null;
    export let info: ChatInfo;

    function timeString(timestamp: string) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString(undefined, {
            hour: "2-digit",
            minute: "2-digit",
            hourCycle: "h24",
        });
    }
</script>

<div class="w-full">
    <div class="flex justify-start w-full">
        <!-- first message -->
        <div>
            <img
                src={agent === null ? "" : agent.avatar}
                class="w-8 h-8 max-w-8 max-h-8 rounded"
            />
        </div>
        <div class="ml-1 px-1 w-full">
            <div class="flex justify-start leading-none items-center mb-1">
                <span
                    class="font-semibold text-gray-900 truncate dark:text-white"
                >
                    {#if agent === null}
                        [Unknown user]
                    {:else}
                        {agent.name}
                    {/if}
                </span>
                {#if agent?.is_bot}
                    <Icon
                        icon="lucide:bot"
                        class="ml-1 w-4 h-4 text-gray-500 dark:text-gray-400"
                    ></Icon>
                {/if}
                <small class="px-1">{timeString(group[0].timestamp)}</small>
                <Tooltip>{group[0].timestamp}</Tooltip>
            </div>
            <div class="hover:bg-gray-100 flex w-full rounded">
                <MessageContent message={group[0]} {info} />
            </div>
        </div>
    </div>
    {#each group.slice(1) as message}
        <div class="flex time-parent w-full justify-start">
            <div class="">
                <small class="time-child">{timeString(message.timestamp)}</small
                >
                <Tooltip>{group[0].timestamp}</Tooltip>
            </div>
            <div class="ml-1 px-1 w-full">
                <div class="hover:bg-gray-100 flex w-full rounded">
                    <MessageContent {message} {info} />
                </div>
            </div>
        </div>
    {/each}
</div>

<style>
    .time-parent:not(:hover) .time-child {
        visibility: hidden;
    }
</style>
