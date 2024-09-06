<script lang="ts">
    import { type ChatInfo } from "$lib";
    import ChatThread from "./ChatThread.svelte";
    import Icon from "@iconify/svelte";
    import type { AnyMessage } from "../client";

    export let messages: AnyMessage[];
    export let info: ChatInfo;
    let showThread = false;
</script>

{#if messages.length > 0}
    <hr />
    <div class="flex">
        <button
            class="flex flex-row items-start hover:bg-gray-200 rounded-md p-1"
            on:click={() => {
                showThread = !showThread;
            }}
        >
            <Icon
                icon="system-uicons:thread"
                width="2em"
                height="2em"
                color="black"
            />
            {#if !showThread}
                <div class="self-center px-1">
                    {messages.length} messages
                </div>
            {/if}
        </button>

        {#if showThread}
            <div class="pl-2 bg-slate-100 w-full">
                <ChatThread {info} {messages}></ChatThread>
            </div>
        {/if}
    </div>
{/if}
