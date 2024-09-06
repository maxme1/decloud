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
        type AnyMessage,
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

    export let messages: AnyMessage[];
    export let chatName: string;
    export let users: string[];
    export let mediaTypes: string[];
    export let textTypes: string[];

    // pagination
    let messagesElement: HTMLElement;
    const perPage = 100;
    let maxPage = 0;
    let page = 0;
    let pages: number[] = [];

    let groups: AnyMessage[][] = [];
    let filtered: AnyMessage[] = [];

    // display
    let showStats: boolean = false;

    // filters
    let showFilters: boolean = false;
    let textFilter: string = "";
    const allTypes = ["message", "service"];
    let currentUsers = new Set<string>();
    let currentMedia = new Set<string>();
    let currentTextTypes = new Set<string>();
    let currentTypes = new Set<string>(allTypes);
    let viaBot: boolean | null = null;
    let replied: boolean | null = null;

    $: {
        filtered = messages.filter((message) => {
            // text
            if (
                textFilter !== "" &&
                message.text_entities.find((entity) =>
                    entity.text.includes(textFilter),
                ) === undefined
            ) {
                return false;
            }
            // type
            if (!currentTypes.has(message.type)) {
                return false;
            }
            // message-specific
            if (message.type == "message") {
                if (!currentMedia.has(message.media_type ?? "none")) {
                    return false;
                }
                if (!currentUsers.has(message.from)) {
                    return false;
                }
                if (viaBot !== null && !!message.via_bot !== viaBot) {
                    return false;
                }
                if (
                    replied !== null &&
                    !!message.reply_to_message_id !== replied
                ) {
                    return false;
                }
                if (
                    currentTextTypes.size < textTypes.length &&
                    !message.text_entities.some((entity) =>
                        currentTextTypes.has(entity.type),
                    )
                ) {
                    return false;
                }
            }

            return true;
        });

        const edges = 2;
        const around = 5;
        maxPage = Math.ceil(filtered.length / perPage);
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
            filtered
                .reverse()
                .slice(page * perPage, (page + 1) * perPage)
                .reverse(),
        );
    }

    function isMessage(group: AnyMessage[]): group is Message[] {
        return group[0].type === "message";
    }
    function isService(group: AnyMessage[]): group is Service[] {
        return group[0].type === "service";
    }
</script>

<div class="flex flex-col overflow-hidden">
    <!-- upper bar -->
    <div class="flex flex-col">
        <div
            class="flex items-center justify-between p-4 bg-white dark:bg-gray-800 dark:border-gray-700"
        >
            <div class="flex">
                <!-- <Avatar
            src="/images/profile-picture-1.webp"
            alt="Neil profile"
            size="lg"
            class="mr-4"
        /> -->
                <p
                    class="text-lg p-2 font-semibold text-gray-900 dark:text-white"
                >
                    {chatName}
                </p>
                <!-- <p class="text-sm text-gray-500 dark:text-gray-400">Online</p> -->

                <input
                    type="text"
                    placeholder="Search"
                    class="w-full p-2 mt-2 border border-gray-200 dark:border-gray-700 rounded-lg"
                    bind:value={textFilter}
                />

                <div class="flex">
                    <button
                        class="text-gray-500 dark:text-gray-400"
                        on:click={() => (showFilters = !showFilters)}
                    >
                        <UserSettingsOutline />
                    </button>
                    <button
                        class="text-gray-500 dark:text-gray-400"
                        on:click={() => (showStats = !showStats)}
                    >
                        <ChartPieOutline />
                    </button>
                </div>
            </div>
        </div>

        <div class="flex flex-row" class:hidden={!showFilters}>
            <div class="mx-1">
                Users
                <CheckboxList names={users} bind:active={currentUsers} />
            </div>
            <div class="mx-1">
                Message types
                <CheckboxList names={allTypes} bind:active={currentTypes} />
            </div>
            <div class="mx-1">
                Media types
                <CheckboxList names={mediaTypes} bind:active={currentMedia} />
            </div>
            <div class="mx-1">
                Text types
                <CheckboxList
                    names={textTypes}
                    bind:active={currentTextTypes}
                />
            </div>
            <div class="mx-1">
                Via bot
                <CheckBoxBool bind:active={viaBot} />
            </div>
            <div class="mx-1">
                Replied
                <CheckBoxBool bind:active={replied} />
            </div>
        </div>
        <hr />
    </div>

    {#if showStats}
        <PostGraphs messages={filtered} />
    {:else if groups.length == 0}
        <div class="flex items-center justify-center p-4">
            <p class="text-lg font-semibold text-gray-900 dark:text-white">
                No messages
            </p>
        </div>
    {:else}
        <div class="overflow-auto" bind:this={messagesElement}>
            <List tag="ul" list="none">
                {#each groups as group}
                    <Li>
                        <div
                            class="flex items-center space-x-4 rtl:space-x-reverse"
                        >
                            {#if isMessage(group)}
                                <MessagesGroup {group} />
                            {:else if isService(group)}
                                <ServiceGroup {group} />
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
</div>
