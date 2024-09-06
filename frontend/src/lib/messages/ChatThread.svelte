<script lang="ts">
    import { ButtonGroup, Button, Tooltip } from "flowbite-svelte";
    import { groupMessages, timeString, type Message } from "../timeline";
    import {
        ChevronLeftOutline,
        ChevronRightOutline,
    } from "flowbite-svelte-icons";
    import type { ChatInfo } from "$lib";
    import MessageContentDispatch from "./MessageContentDispatch.svelte";
    import GroupImage from "./GroupImage.svelte";
    import GroupHeader from "./GroupHeader.svelte";
    import type { AnyMessage } from "../client";

    export let messages: AnyMessage[];
    export let focusedMessage: string | null;
    export let info: ChatInfo;

    // pagination
    let messagesElement: HTMLElement;
    const perPage = 100;
    let maxPage = 0;
    let page = 0;
    let pages: number[] = [];
    let scrollToFocus: string | null = null;

    let groups: AnyMessage[][] = [];

    $: {
        const edges = 2;
        const around = 5;
        maxPage = Math.ceil(messages.length / perPage);

        if (focusedMessage !== null) {
            let index = messages.findIndex((m) => m.id === focusedMessage);
            if (index < 0) {
                index = 0;
            }
            // because the messages are reversed
            page = Math.floor((messages.length - index) / perPage);
            scrollToFocus = focusedMessage;
            focusedMessage = null;
        }
        page = Math.max(Math.min(page, maxPage - 1), 0);
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

    function scrollIntoView(node: any, scroll: any) {
        function update(scroll: any) {
            if (scroll) node.scrollIntoView({ behavior: "smooth" });
        }

        update(scroll);
        return { update };
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
            <ul>
                {#each groups as group}
                    {@const first = group[0]}
                    <li>
                        <div class="flex items-center mb-3">
                            <div class="w-full">
                                <div class="flex justify-start w-full">
                                    <!-- first message -->
                                    <div class="w-10 self-start">
                                        <GroupImage {group} {info} />
                                    </div>
                                    <div class="ml-1 px-1 w-full mb-1">
                                        <div
                                            class="flex justify-start leading-none items-center mb-1"
                                        >
                                            <GroupHeader {group} {info} />
                                            <small class="px-1"
                                                >{timeString(
                                                    first.timestamp,
                                                )}</small
                                            >
                                            <Tooltip>{first.timestamp}</Tooltip>
                                        </div>
                                        <div
                                            class="hover:bg-gray-100 flex w-full rounded"
                                            id={first.id}
                                            use:scrollIntoView={first.id ===
                                                scrollToFocus}
                                            class:bg-yellow-50={first.id ===
                                                scrollToFocus}
                                        >
                                            <MessageContentDispatch
                                                message={first}
                                                {info}
                                            />
                                        </div>
                                    </div>
                                </div>
                                {#each group.slice(1) as message}
                                    <div
                                        class="flex time-parent w-full justify-start"
                                    >
                                        <div class="w-10 flex">
                                            <small class="time-child mx-auto"
                                                >{timeString(
                                                    message.timestamp,
                                                )}</small
                                            >
                                            <Tooltip
                                                >{message.timestamp}</Tooltip
                                            >
                                        </div>
                                        <div class="ml-1 px-1 w-full mb-1">
                                            <div
                                                class="hover:bg-gray-100 flex w-full rounded"
                                                id={message.id}
                                                use:scrollIntoView={message.id ===
                                                    scrollToFocus}
                                                class:bg-yellow-50={message.id ===
                                                    scrollToFocus}
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
                    </li>
                {/each}
                <!-- <InfiniteScroll
        threshold={100}
        on:loadMore={() => console.log("load")}
    /> -->
            </ul>
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
