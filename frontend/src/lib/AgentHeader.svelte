<script lang="ts">
    import { getAgent } from "./timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";

    export let agent_id: string | null;
    export let info: ChatInfo;

    let agent = null;
    $: agent = getAgent(agent_id, info);
</script>

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
