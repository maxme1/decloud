<script lang="ts">
    import {
        Indicator,
        Avatar,
        Badge,
        Img,
        Video,
        Checkbox,
        Pagination,
        ButtonGroup,
        Button,
    } from "flowbite-svelte";
    import { List, Li } from "flowbite-svelte";
    import { onMount, afterUpdate } from "svelte";
    import {
        groupMessages,
        type AnyMessage,
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

    export let messages: AnyMessage[];
    export let chatName: string;

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
    let allUsers: string[] = [];
    let allMedia: string[] = [];
    const allTypes = ["message", "service"];
    let users = new Set<string>();
    let media = new Set<string>();
    let types = new Set<string>(allTypes);

    $: {
        const realMessages = messages.filter(
            (message): message is Message => message.type === "message",
        );
        allUsers = Array.from(
            new Set(
                messages
                    .filter(
                        (message): message is Message =>
                            message.type === "message",
                    )
                    .map((message) => message.from),
            ),
        );
        allMedia = Array.from(
            new Set(
                realMessages.map((message) => message.media_type ?? "none"),
            ),
        );
    }

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
            if (!types.has(message.type)) {
                return false;
            }
            // message-specific
            if (message.type == "message") {
                if (!media.has(message.media_type ?? "none")) {
                    return false;
                }
                if (!users.has(message.from)) {
                    return false;
                }
            }

            return true;
        });
        groups = groupMessages(
            filtered
                .reverse()
                .slice(page * perPage, (page + 1) * perPage)
                .reverse(),
        );

        maxPage = Math.ceil(filtered.length / perPage);
        page = Math.min(page, maxPage - 1);

        const edges = 2;
        const around = 5;
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
            <CheckboxList names={allUsers} bind:active={users} />
            <CheckboxList names={allTypes} bind:active={types} />
            <CheckboxList names={allMedia} bind:active={media} />
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
