<script lang="ts">
    import {
        Indicator,
        Avatar,
        Badge,
        Img,
        Video,
        Checkbox,
    } from "flowbite-svelte";
    import InfiniteScroll from "svelte-infinite-scroll";
    import { List, Li } from "flowbite-svelte";
    import { onMount } from "svelte";
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
    } from "flowbite-svelte-icons";
    import PostGraphs from "./PostGraphs.svelte";

    export let messages: AnyMessage[];
    export let chatName: string;

    let messagesElement: HTMLElement;
    const perPage = 100;
    let maxPage = Math.ceil(messages.length / perPage);
    let page = 0;
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
            new Set(realMessages.map((message) => message.from)),
        );
        users = new Set(allUsers);
        allMedia = Array.from(
            new Set(
                realMessages.map((message) => message.media_type ?? "none"),
            ),
        );
        media = new Set(allMedia);
    }

    $: filtered = messages.filter((message) => {
        // text
        if (textFilter !== "" && !message.text.includes(textFilter)) {
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
    $: groups = groupMessages(
        filtered
            .reverse()
            .slice(page * perPage, (page + 1) * perPage)
            .reverse(),
    );

    function isMessage(group: AnyMessage[]): group is Message[] {
        return group[0].type === "message";
    }
    function isService(group: AnyMessage[]): group is Service[] {
        return group[0].type === "service";
    }

    onMount(() => {
        messagesElement!.scrollTop = messagesElement!.scrollHeight;
    });
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

        {#if showFilters}
            <div class="flex flex-row">
                <CheckboxList names={allUsers} bind:active={users} />
                <CheckboxList names={allTypes} bind:active={types} />
                <CheckboxList names={allMedia} bind:active={media} />
            </div>
        {/if}

        <hr />
    </div>

    <div class="overflow-auto" bind:this={messagesElement}>
        {#if showStats}
            <PostGraphs messages={filtered} />
        {:else}
            {#if groups.length == 0}
                <div class="flex items-center justify-center p-4">
                    <p
                        class="text-lg font-semibold text-gray-900 dark:text-white"
                    >
                        No messages
                    </p>
                </div>
            {/if}
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
        {/if}
    </div>
</div>
