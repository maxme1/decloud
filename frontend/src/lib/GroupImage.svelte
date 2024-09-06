<script lang="ts">
    import { isAgent, type Message, isSystem } from "./timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";
    import AgentImage from "./AgentImage.svelte";

    export let group: Message[];
    export let info: ChatInfo;

    const icons = new Map([
        ["call", "tabler:phone-call"],
        ["join", "tabler:door-enter"],
        ["leave", "tabler:door-exit"],
        ["purpose", "tabler:target"],
        ["create", "tabler:playlist-add"],
        ["archive", "tabler:archive"],
    ]);
</script>

{#if isAgent(group)}
    <AgentImage agent_id={group[0].agent_id} {info} />
{:else if isSystem(group)}
    {@const first = group[0]}
    {#if icons.has(first.event)}
        <Icon icon={icons.get(first.event) ?? ""} class="w-full h-full"></Icon>
    {:else}
        <Icon icon="tabler:timeline-event" class="w-full h-full"></Icon>
    {/if}
{:else}
    {console.error("GroupImage: group is not an agent or system message")}
{/if}
