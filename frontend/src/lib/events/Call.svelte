<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Call } from "$lib/client";
    import SystemAgents from "$lib/messages/SystemAgents.svelte";
    import Icon from "@iconify/svelte";
    import humanizeDuration from "humanize-duration";

    export let event: Call;
    export let info: ChatInfo;

    const mapping = new Map([
        ["missed", "tabler:phone-calling"],
        ["declined", "tabler:phone-end"],
        ["hung_up", "tabler:phone-done"],
        ["disconnected", "tabler:phone-end"],
    ]);
</script>

<div class="flex items-center">
    {#if event.status}
        <Icon
            icon={mapping.get(event.status) ?? ""}
            class="mr-1"
            width="1.5em"
            height="1.5em"
        />
    {/if}

    {#if event.duration}
        {humanizeDuration(event.duration * 1000, { round: true })}
    {/if}
</div>
<SystemAgents agents={event.agents} {info}></SystemAgents>
