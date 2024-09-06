<script lang="ts">
    import { Badge } from "flowbite-svelte";
    import type { AgentMessage } from "./timeline";
    import { type ChatInfo } from "$lib";
    import Block from "./blocks/Block.svelte";
    import ChatThread from "./ChatThread.svelte";
    import EmojiBase from "./EmojiBase.svelte";
    import Icon from "@iconify/svelte";
    import Thread from "./Thread.svelte";
    import Blocks from "./blocks/Blocks.svelte";

    export let message: AgentMessage;
    export let info: ChatInfo;
    const hasBadge = false;
    let showShared = message.shared.length == 1;
    // message.edited ||
    // message.reply_to_message_id ||
    // message.forwarded_from ||
    // message.via_bot;
</script>

<div class="flex flex-col">
    <!-- <p class="text-sm text-gray-500 dark:text-gray-400"> -->

    <!-- blocks -->
    <div>
        <Blocks blocks={message.blocks} {info} />
    </div>

    <!-- attachments -->
    <!-- <div>
        {#each message.attachments as attachment}
            {#if attachment.type == "removed"}
                <Icon
                    icon="grommet-icons:document-missing"
                    width="3em"
                    height="3em"
                />
            {:else if attachment.type === "image" && attachment.url}
                <ZoomableImage src={attachment.url} class="max-h-48" />
            {:else}
                [Attachment {attachment.url}]
            {/if}
        {/each}
    </div> -->

    <!-- reactions -->
    {#if message.reactions.length > 0}
        <div class="flex flex-wrap">
            {#each message.reactions as reaction}
                <Badge color="blue" rounded
                    ><EmojiBase {info} emoji={reaction.emoji} height={4} />
                    {reaction.users.length}</Badge
                >
            {/each}
        </div>
    {/if}

    <!-- shared -->
    {#if message.shared.length > 0}
        <hr />
        <div class="flex">
            <button
                class="flex flex-row items-start hover:bg-gray-200 rounded-md p-1"
                on:click={() => {
                    showShared = !showShared;
                }}
            >
                <Icon
                    icon="fluent:calendar-reply-16-filled"
                    width="2em"
                    height="2em"
                    color="black"
                />
                {#if !showShared}
                    <div class="self-center px-1">
                        {message.shared.length} shared
                    </div>
                {/if}
            </button>

            {#if showShared}
                <div class="pl-2 bg-slate-100 w-full">
                    <ChatThread
                        {info}
                        messages={message.shared.map((x) => x.message)}
                    ></ChatThread>
                </div>
            {/if}
        </div>
    {/if}

    <Thread messages={message.thread} {info}></Thread>
</div>

<!-- <div class="absolute bottom-0 right-0 flex">
        <small class="time-child bg-white rounded px-1"
            >{message.timestamp}</small
        >

        {#if hasBadge}
            <Badge color="dark" rounded class="px-2.5 py-0.5 ml-auto relative">
                {#if message.edited !== undefined}
                    <div class="flex items-center badge-parent">
                        <EditOutline size="xs" class="me-1" />
                        <span class="badge-child">{message.edited}</span>
                    </div>
                {/if}
                {#if message.reply_to_message_id !== undefined}
                    <div class="flex items-center badge-parent">
                        <ReplyOutline size="xs" class="me-1" />
                        <span class="badge-child">Replied</span>
                    </div>
                {/if}
                {#if message.forwarded_from !== undefined}
                    <div class="flex items-center badge-parent">
                        <ForwardOutline size="xs" class="me-1" />
                        <span class="badge-child">{message.forwarded_from}</span
                        >
                    </div>
                {/if}
                {#if message.via_bot !== undefined}
                    <div class="flex items-center badge-parent">
                        <ComputerSpeakerOutline size="xs" class="me-1" />
                        <span class="badge-child">{message.via_bot}</span>
                    </div>
                {/if}
            </Badge>
        {/if}
    </div> -->
