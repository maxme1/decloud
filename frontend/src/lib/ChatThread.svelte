<script lang="ts">
    import {
        Indicator,
        Avatar,
        Badge,
        ButtonGroup,
        Button,
    } from "flowbite-svelte";
    import { List, Li } from "flowbite-svelte";
    import {
        groupMessages,
        // type AnyMessage,
        type Message,
        type Service,
    } from "./timeline";
    import MessagesGroup from "./MessagesGroup.svelte";
    import ServiceGroup from "./ServiceGroup.svelte";
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

    function isMessage(group: Message[]): group is AgentMessage[] {
        return group[0].type === "agent";
    }
    function isService(group: Message[]): group is SystemMessage[] {
        return group[0].type === "system";
    }
    function getAgent(group: AgentMessage[]): Agent | null {
        if (group[0].agent_id == null) return null;
        const agent = info.agents.find((x) => x.id == group[0].agent_id);
        if (agent === undefined)
            console.log("Unknown agent: " + group[0].agent_id);
        return agent ?? null;
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
                        <div
                            class="flex items-center space-x-4 rtl:space-x-reverse"
                        >
                            {#if isMessage(group)}
                                <MessagesGroup
                                    {group}
                                    {info}
                                    agent={getAgent(group)}
                                />
                            {:else if isService(group)}
                                <ServiceGroup {group} {info} />
                            {:else}
                                {console.log(
                                    "Unknown group type: " + group[0].type,
                                )}
                            {/if}
                            <!-- <div class="flex-shrink-0">
                        <img
                        class="w-8 h-8 rounded-full"
                        src="/images/profile-picture-1.webp"
                        alt="Neil profile"
                        />
                    </div> -->
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
                        <!-- class:font-semibold={p == page} -->
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
