<script lang="ts">
    import { isAgent, isSystem, type Message } from "../timeline";
    import { type ChatInfo } from "$lib";
    import AgentHeader from "./AgentHeader.svelte";

    export let group: Message[];
    export let info: ChatInfo;
</script>

{#if isAgent(group)}
    <AgentHeader agent_id={group[0].agent_id} {info} />
{:else if isSystem(group)}{:else}
    {console.error("GroupHeader: group is not an agent or system message")}
{/if}
