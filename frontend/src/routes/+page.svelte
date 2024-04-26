<script lang="ts">
    import { page } from "$app/stores";
    import ChatTimeline from "$lib/ChatTimeline.svelte";
    import type { Message } from "$lib/timeline";
    import {
        Sidebar,
        SidebarGroup,
        SidebarItem,
        SidebarWrapper,
    } from "flowbite-svelte";
    import {
        ChartPieSolid,
        GridSolid,
        MailBoxSolid,
        UserSolid,
    } from "flowbite-svelte-icons";
    import { onMount } from "svelte";
    $: activeUrl = $page.url.pathname;
    let activeClass =
        "flex items-center p-2 text-base font-normal text-primary-900 bg-primary-200 dark:bg-primary-700 rounded-lg dark:text-white hover:bg-primary-100 dark:hover:bg-gray-700";
    let nonActiveClass =
        "flex items-center p-2 text-base font-normal text-green-900 rounded-lg dark:text-white hover:bg-green-100 dark:hover:bg-green-700";

    let chats: [string, string][] = [];
    let activeChat: [string, string] | undefined;
    let messages: Message[] = [];

    async function updateMessages(chat: [string, string] | undefined) {
        if (chat === undefined) {
            messages = [];
        } else {
            const result = await (
                await fetch(`http://localhost:3000/${chat[0]}.json`)
            ).json();
            messages = result["messages"];
        }
        activeChat = chat;
    }

    onMount(async () => {
        const response = await (
            await fetch("http://localhost:3000/chats.json")
        ).json();
        for (let chat in response) {
            chats.push([chat, response[chat]]);
        }
        chats = [...chats];
        await updateMessages(chats[0]);
    });
</script>

<div class="h-screen">
    <div class="flex">
        <Sidebar {activeUrl} {activeClass} {nonActiveClass}>
            <SidebarWrapper>
                <SidebarGroup>
                    {#each chats as chat}
                        <SidebarItem
                            label={chat[1]}
                            on:click={() => updateMessages(chat)}
                        >
                            <!-- <svelte:fragment slot="icon">
                            <ChartPieSolid class="w-5 h-5" />
                        </svelte:fragment> -->
                        </SidebarItem>
                    {/each}
                </SidebarGroup>
            </SidebarWrapper>
        </Sidebar>

        {#if activeChat !== undefined}
            <!-- <div class="flex-1 min-w-0">
            <p class="text-lg font-semibold text-gray-900 dark:text-white">
                {activeChat[1]}
            </p>
        </div> -->

            <div class="p-2 w-full h-screen flex flex-col">
                <ChatTimeline {messages} chatName={activeChat[1]} />
            </div>
        {/if}
    </div>
</div>
