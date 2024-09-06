<script lang="ts">
    import { page } from "$app/stores";
    import { ApiService, type ChatInfo } from "$lib";
    import ChannelsList from "$lib/ChannelsList.svelte";
    import ChatTimeline from "$lib/messages/ChatTimeline.svelte";
    import { type AnyMessage, type Chat } from "$lib/client";
    import { onMount } from "svelte";
    import { channels } from "$lib/store";

    let channel!: Chat;
    let messages: AnyMessage[] = [];
    let info!: ChatInfo;

    page.subscribe(async (value) => {
        const chatId: string = value.params.id;
        const source: string = value.params.source;

        const msg = await ApiService.messagesMessagesSourceChatIdGet({
            chatId,
            source,
        });
        const _info = {
            ...(await ApiService.infoInfoSourceChatIdGet({
                chatId,
                source,
            })),
            channels: [],
        };
        [messages, info] = [msg, _info];
        channel = $channels.find((c) => c.id === chatId)!;
    });

    onMount(async () => {
        if ($channels.length === 0) {
            $channels = await ApiService.chatsChatsGet();
        }
    });
</script>

<div class="flex h-screen w-screen divide-x">
    <ChannelsList channels={$channels}></ChannelsList>

    {#if channel}
        <div class="p-2 mx-1 w-full flex flex-col overflow-x-hidden">
            <ChatTimeline {channel} {messages} {info} />
        </div>
    {/if}
</div>
