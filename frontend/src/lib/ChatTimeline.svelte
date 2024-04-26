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
    import { groupMessages, type Message } from "./timeline";
    import MessagesGroup from "./MessagesGroup.svelte";
    import SystemGroup from "./SystemGroup.svelte";
    import CheckboxList from "./CheckboxList.svelte";
    import {
        UserSettingsOutline,
        ChartPieOutline,
    } from "flowbite-svelte-icons";
    import WeekdaysPostCount from "./WeekdaysPostCount.svelte";

    export let messages: Message[];
    export let chatName: string;

    let messagesElement: HTMLElement;
    let page = 0;
    const perPage = 100;
    let maxPage = Math.ceil(messages.length / perPage);
    let groups: Message[][] = [];
    let filtered: Message[] = [];

    // display
    let showStats: boolean = false;

    // filters
    let showFilters: boolean = false;
    let textFilter: string = "";
    let allUsers: string[] = [];
    let users: Set<string> = new Set();

    const allTypes = ["message", "service"];
    let types = new Set<string>(allTypes);
    const allMedia = [
        "sticker",
        "animation",
        "video_file",
        "audio_file",
        "voice_message",
        "video_message",
        "none",
    ];
    let media = new Set<string>(allMedia);

    $: filtered = messages.filter((message) => {
        // text
        if (
            textFilter !== "" &&
            (message.text == undefined || !message.text.includes(textFilter))
        ) {
            return false;
        }
        // type
        if (!types.has(message.type)) {
            return false;
        }
        // media
        if (!media.has(message.media_type ?? "none")) {
            return false;
        }

        return message.from === undefined || users.has(message.from);
    });
    $: groups = groupMessages(
        filtered
            .reverse()
            .slice(page * perPage, (page + 1) * perPage)
            .reverse(),
    );

    onMount(() => {
        allUsers = Array.from(
            new Set(
                messages
                    .filter((message) => message.from !== undefined)
                    .map((message) => message.from),
            ),
        );
        users = new Set(allUsers);

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
            <div class="flex flex-col p-4">
                <p class="text-lg font-semibold text-gray-900 dark:text-white">
                    Stats
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    Messages: {filtered.length}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    Users: {users.size}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    Types: {types.size}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    Media: {media.size}
                </p>
            </div>
            <WeekdaysPostCount {messages} />
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
            <List
                tag="ul"
                list="none"
                class="divide-y divide-gray-200 dark:divide-gray-700"
            >
                {#each groups as group}
                    <Li class="pb-3 sm:pb-4">
                        <div
                            class="flex items-center space-x-4 rtl:space-x-reverse"
                        >
                            {#if group[0].type == "message"}
                                <MessagesGroup {group} />
                            {:else if group[0].type == "service"}
                                <SystemGroup {group} />
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
