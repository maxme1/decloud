<script lang="ts">
    import { page } from "$app/stores";
    import { filesRoot, type ChatInfo } from "$lib";
    import ChatThread from "$lib/ChatThread.svelte";
    // import ChatTimeline from "$lib/ChatTimeline.svelte";
    import {
        DefaultService,
        OpenAPI,
        type Agent,
        type AgentMessage,
        type Chat,
    } from "$lib/client";
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

    let chats: Chat[] = [];
    let activeChat: Chat | null = null;
    let messages: Message[] = [];
    let info: ChatInfo = { agents: [], emojis: {}, channels: [] };

    async function selectChat(chat: Chat | null) {
        if (chat === null) {
            [activeChat, messages, info] = [
                chat,
                [],
                { agents: [], emojis: {}, channels: [] },
            ];
        } else {
            [activeChat, messages, info] = [
                chat,
                await DefaultService.messagesMessagesSourceChatIdGet({
                    chatId: chat.id,
                    source: chat.source,
                }),
                {
                    ...(await DefaultService.infoInfoSourceChatIdGet({
                        chatId: chat.id,
                        source: chat.source,
                    })),
                    channels: chats,
                },
            ];
        }
    }

    // function extractUsers(messages: Message[]): string[] {
    //     return Array.from(
    //         new Set(
    //             messages
    //                 .filter(
    //                     (message): message is Message =>
    //                         message.type === "message",
    //                 )
    //                 .map((message) => message.from),
    //         ),
    //     );
    // }
    // function extractMediaTypes(messages: Message[]): string[] {
    //     return Array.from(
    //         new Set(
    //             messages
    //                 .filter(
    //                     (message): message is Message =>
    //                         message.type === "message",
    //                 )
    //                 .map((message) => message.media_type ?? "none"),
    //         ),
    //     );
    // }
    // function extractTextTypes(messages: Message[]): string[] {
    //     const types = new Set<string>();
    //     for (let message of messages) {
    //         if (message.type === "message") {
    //             for (let entity of message.text_entities) {
    //                 types.add(entity.type);
    //             }
    //         }
    //     }
    //     return Array.from(types).toSorted();
    // }

    OpenAPI.BASE = "http://localhost:9000";

    onMount(async () => {
        chats = await DefaultService.chatsChatsGet();
        await selectChat(chats[0]);
    });
</script>

<div class="h-screen w-screen">
    <div class="flex h-screen w-screen">
        <div class="overflow-auto">
            <Sidebar
                {activeUrl}
                activeClass="flex items-center p-2 text-base font-normal text-primary-900 bg-primary-200 dark:bg-primary-700 rounded-lg dark:text-white hover:bg-primary-100 dark:hover:bg-gray-700"
                nonActiveClass="flex items-center p-2 text-base font-normal text-green-900 rounded-lg dark:text-white hover:bg-green-100 dark:hover:bg-green-700"
            >
                <SidebarWrapper>
                    <SidebarGroup>
                        {#each chats as chat}
                            <SidebarItem
                                label={chat.name}
                                on:click={() => selectChat(chat)}
                            ></SidebarItem>
                        {/each}
                    </SidebarGroup>
                </SidebarWrapper>
            </Sidebar>
        </div>

        {#if activeChat !== null}
            <div class="p-2 h-screen w-full flex flex-col overflow-x-hidden">
                <div class="flex-1 min-w-0">
                    <p
                        class="text-lg font-semibold text-gray-900 dark:text-white"
                    >
                        {activeChat.name}
                    </p>
                </div>

                <ChatThread {messages} {info} />

                <!-- <ChatTimeline
                    {messages}
                    chatName={activeChat[1]}
                    users={extractUsers(messages)}
                    mediaTypes={extractMediaTypes(messages)}
                    textTypes={extractTextTypes(messages)}
                /> -->
            </div>
        {/if}
    </div>
</div>
