<script lang="ts">
    import { getAgent, isAgent, isSystem, type Message } from "./timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";

    export let group: Message[];
    export let info: ChatInfo;
</script>

{#if isAgent(group)}
    {@const agent = getAgent(group, info)}
    <span class="font-semibold text-gray-900 truncate dark:text-white">
        {#if agent === null}
            [Unknown user]
        {:else}
            {agent.name}
        {/if}
    </span>
    {#if agent?.is_bot}
        <Icon
            icon="lucide:bot"
            class="ml-1 w-4 h-4 text-gray-500 dark:text-gray-400"
        ></Icon>
    {/if}
{:else if isSystem(group)}{:else}
    {console.error("GroupHeader: group is not an agent or system message")}
{/if}
