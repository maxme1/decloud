<script lang="ts">
    import { type Message } from "../timeline";
    import { type ChatInfo } from "$lib";
    import MessageContent from "./MessageContent.svelte";
    import SystemContent from "./SystemContent.svelte";

    export let message: Message;
    export let info: ChatInfo;
</script>

{#if message.type == "agent"}
    <MessageContent {message} {info} />
{:else}
    <SystemContent {message} {info} />
{/if}
