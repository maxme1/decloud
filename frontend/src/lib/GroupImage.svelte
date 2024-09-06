<script lang="ts">
    import { isAgent, getAgent, type Message, isSystem } from "./timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";

    export let group: Message[];
    export let info: ChatInfo;

    const icons = new Map([
        ["call", "tabler:phone-call"],
        ["join", "tabler:door-enter"],
        ["leave", "tabler:door-exit"],
        ["purpose", "tabler:target"],
    ]);
</script>

{#if isAgent(group)}
    {@const agent = getAgent(group, info)}
    {#if agent === null || agent.avatar === null}
        <Icon icon="tabler:user-question" class="w-full h-full"></Icon>
    {:else}
        <img src={agent.avatar} class="rounded" />
    {/if}
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
