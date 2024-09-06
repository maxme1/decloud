<script lang="ts">
    import { getAgent } from "../timeline";
    import { type ChatInfo } from "$lib";
    import Icon from "@iconify/svelte";

    export let agent_id: string | null;
    export let info: ChatInfo;

    let agent = null;
    $: agent = getAgent(agent_id, info);
</script>

{#if agent === null}
    <Icon icon="tabler:user-question" class="w-full h-full"></Icon>
{:else if agent.avatar === null}
    <div
        class="rounded aspect-square w-full h-full bg-green-300 flex text-center items-center justify-center text-white text-2xl font-bold"
    >
        {(agent.name[0] ?? "?").toUpperCase()}
    </div>
{:else}
    <img alt={agent.name} src={agent.avatar} class="rounded w-full h-full" />
{/if}
