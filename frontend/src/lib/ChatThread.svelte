<script lang="ts">
    import {
        Indicator,
        Avatar,
        Badge,
        ButtonGroup,
        Button,
        Tooltip,
    } from "flowbite-svelte";
    import { List, Li } from "flowbite-svelte";
    import {
        groupMessages,
        // type AnyMessage,
        type Message,
        type Service,
    } from "./timeline";
    import MessagesGroup from "./MessagesGroup.svelte";
    import ServiceGroup from "./SystemContent.svelte";
    import CheckboxList from "./CheckboxList.svelte";
    import {
        UserSettingsOutline,
        ChartPieOutline,
        ChevronLeftOutline,
        ChevronRightOutline,
    } from "flowbite-svelte-icons";
    import PostGraphs from "./PostGraphs.svelte";
    import CheckBoxBool from "./CheckBoxBool.svelte";
    import {
        type Agent,
        type AgentMessage,
        type SystemMessage,
    } from "$lib/client";
    import type { ChatInfo } from "$lib";
    import MessageContentDispatch from "./MessageContentDispatch.svelte";
    import Icon from "@iconify/svelte";
    import GroupImage from "./GroupImage.svelte";
    import GroupHeader from "./GroupHeader.svelte";

    export let messages: Message[];
    export let info: ChatInfo;

    // pagination
    let messagesElement: HTMLElement;
    const perPage = 100;
    let maxPage = 0;
    let page = 0;
    let pages: number[] = [];

    let groups: Message[][] = [];

    $: {
        const edges = 2;
        const around = 5;
        maxPage = Math.ceil(messages.length / perPage);
        page = Math.min(page, maxPage);
        pages = Array.from(
            new Set([
                ...Array.from(
                    { length: Math.min(edges, maxPage) },
                    (_, i) => i,
                ),
                ...Array.from(
                    { length: Math.min(edges, maxPage) },
                    (_, i) => maxPage - i - 1,
                ),
                ...Array.from(
                    { length: Math.min(around, maxPage) },
                    (_, i) => page + i - 2,
                ).filter((i) => i >= 0 && i < maxPage),
            ]),
        ).toSorted((a, b) => a - b);

        groups = groupMessages(
            messages
                // TODO: optimize
                .toReversed()
                .slice(page * perPage, (page + 1) * perPage)
                .toReversed(),
        );
    }

    function timeString(timestamp: string) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString(undefined, {
            hour: "2-digit",
            minute: "2-digit",
            hourCycle: "h24",
        });
    }
</script>

<div class="flex flex-col overflow-hidden">
    {#if groups.length == 0}
        <div class="flex items-center justify-center p-4">
            <p class="text-lg font-semibold text-gray-900 dark:text-white">
                No messages
            </p>
        </div>
    {:else}
        <div class="overflow-y-auto break-words" bind:this={messagesElement}>
            <List tag="ul" list="none">
                {#each groups as group}
                    <Li>
                        <div class="flex items-center mb-3">
                            <div class="w-full">
                                <div class="flex justify-start w-full">
                                    <!-- first message -->
                                    <div class="w-10">
                                        <GroupImage {group} {info} />
                                    </div>
                                    <div class="ml-1 px-1 w-full mb-1">
                                        <div
                                            class="flex justify-start leading-none items-center mb-1"
                                        >
                                            <GroupHeader {group} {info} />
                                            <small class="px-1"
                                                >{timeString(
                                                    group[0].timestamp,
                                                )}</small
                                            >
                                            <Tooltip
                                                >{group[0].timestamp}</Tooltip
                                            >
                                        </div>
                                        <div
                                            class="hover:bg-gray-100 flex w-full rounded"
                                        >
                                            <MessageContentDispatch
                                                message={group[0]}
                                                {info}
                                            />
                                        </div>
                                    </div>
                                </div>
                                {#each group.slice(1) as message}
                                    <div
                                        class="flex time-parent w-full justify-start"
                                    >
                                        <div class="w-10">
                                            <small class="time-child"
                                                >{timeString(
                                                    message.timestamp,
                                                )}</small
                                            >
                                            <Tooltip
                                                >{group[0].timestamp}</Tooltip
                                            >
                                        </div>
                                        <div class="ml-1 px-1 w-full mb-1">
                                            <div
                                                class="hover:bg-gray-100 flex w-full rounded"
                                            >
                                                <MessageContentDispatch
                                                    {message}
                                                    {info}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    </Li>
                {/each}
                <!-- <InfiniteScroll
        threshold={100}
        on:loadMore={() => console.log("load")}
    /> -->
            </List>
        </div>

        <!-- pagination -->
        {#if maxPage > 1}
            <div class="flex justify-center items-center">
                <ButtonGroup>
                    <Button
                        on:click={() => {
                            page = Math.max(0, page - 1);
                        }}
                    >
                        <span class="sr-only">Previous</span>
                        <ChevronLeftOutline class="w-2.5 h-2.5" />
                    </Button>
                    {#each pages as p}
                        <Button
                            class="px-3 py-1 cursor-pointer"
                            on:click={() => {
                                page = p;
                            }}
                        >
                            <span class:font-semibold={p == page}>
                                {p + 1}
                            </span>
                        </Button>
                    {/each}
                    <Button
                        on:click={() => {
                            page = Math.min(maxPage - 1, page + 1);
                        }}
                    >
                        <span class="sr-only">Next</span>
                        <ChevronRightOutline class="w-2.5 h-2.5" />
                    </Button>
                </ButtonGroup>
            </div>
        {/if}
    {/if}
</div>

<style>
    .time-parent:not(:hover) .time-child {
        visibility: hidden;
    }
</style>
