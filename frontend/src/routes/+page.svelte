<script lang="ts">
    import { type ChatInfo } from "$lib";
    import ChatThread from "$lib/ChatThread.svelte";
    import ChatTimeline from "$lib/ChatTimeline.svelte";
    import { DefaultService, OpenAPI, type Chat } from "$lib/client";
    import type { Message } from "$lib/timeline";
    import { onMount } from "svelte";

    let chats: Chat[] = [];
    let activeChat: Chat | null = null;
    let messages: Message[] = [];
    let info: ChatInfo = { agents: [], channels: [] };

    async function selectChat(chat: Chat | null) {
        if (chat === null) {
            [activeChat, messages, info] = [
                chat,
                [],
                { agents: [], channels: [] },
            ];
        } else {
            const msg = await DefaultService.messagesMessagesSourceChatIdGet({
                chatId: chat.id,
                source: chat.source,
            });
            const _info = {
                ...(await DefaultService.infoInfoSourceChatIdGet({
                    chatId: chat.id,
                    source: chat.source,
                })),
                channels: chats,
            };
            [activeChat, messages, info] = [chat, msg, _info];
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

    function clipLongName(name: string): string {
        const size = 16;
        return name.length > size ? name.slice(0, size) + "..." : name;
    }

    OpenAPI.BASE = "http://localhost:9000";

    onMount(async () => {
        chats = await DefaultService.chatsChatsGet();
        await selectChat(chats[0]);
    });
</script>

<div class="flex h-screen w-screen divide-x">
    <div class="overflow-y-auto p-2 m-1">
        <ul>
            {#each chats as chat}
                <li>
                    <button
                        on:click={() => selectChat(chat)}
                        class={"text-gray-500 dark:text-gray-400 px-2 hover:bg-gray-200 rounded-md p-1 w-full text-left text-nowrap overflow-clip text-clip " +
                            (activeChat === chat ? "bg-gray-300" : "")}
                    >
                        <small>{clipLongName(chat.name)}</small>
                    </button>
                </li>
            {/each}
        </ul>
    </div>

    {#if activeChat !== null}
        <div class="p-2 mx-1 w-full flex flex-col overflow-x-hidden">
            <ChatTimeline chat={activeChat} {messages} {info} />
        </div>
    {/if}
</div>
