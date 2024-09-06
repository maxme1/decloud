<script lang="ts">
    import { page } from "$app/stores";
    import { ApiService } from "$lib";
    import ConvList from "$lib/ConvList.svelte";
    import ChatTimeline from "$lib/messages/ChatTimeline.svelte";
    import { onMount } from "svelte";
    import { activeChannel, channels } from "$lib/store";

    let focusedMessage: string | null = null;

    page.subscribe(async (value) => {
        const chatId: string = value.params.id;
        const source: string = value.params.source;
        if (value.url.hash === "") {
            focusedMessage = null;
        } else {
            focusedMessage = value.url.hash.slice(1);
        }

        if ($channels.length === 0) {
            $channels = await ApiService.chatsChatsGet();
        }

        $activeChannel = {
            channel: $channels.find((c) => c.id === chatId)!,
            messages: await ApiService.messagesMessagesSourceChatIdGet({
                chatId,
                source,
            }),
            info: {
                ...(await ApiService.infoInfoSourceChatIdGet({
                    chatId,
                    source,
                })),
                channels: [],
            },
        };
    });

    onMount(async () => {
        if ($channels.length === 0) {
            $channels = await ApiService.chatsChatsGet();
        }
    });
</script>

<div class="flex h-screen w-screen divide-x">
    <ConvList channels={$channels}></ConvList>

    {#if $activeChannel !== null}
        <div class="p-2 mx-1 w-full flex flex-col overflow-x-hidden">
            <ChatTimeline
                channel={$activeChannel.channel}
                messages={$activeChannel.messages}
                info={$activeChannel.info}
                {focusedMessage}
            ></ChatTimeline>
        </div>
    {/if}
</div>
