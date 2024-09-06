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
    ]);
</script>

{#if isAgent(group)}
    {@const agent = getAgent(group, info)}
    <img src={agent === null ? "" : agent.avatar} class="rounded" />
{:else if isSystem(group)}
    {@const first = group[0]}
    {#if icons.has(first.event)}
        <Icon icon={icons.get(first.event) ?? ""} class="w-full h-full"></Icon>
    {:else}
        <img class="rounded" src="" />
    {/if}
{:else}
    {console.error("GroupImage: group is not an agent or system message")}
{/if}
