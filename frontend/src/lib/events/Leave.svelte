<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Leave } from "$lib/client";
    import User from "$lib/elements/User.svelte";
    import SystemAgents from "$lib/messages/SystemAgents.svelte";

    export let event: Leave;
    export let info: ChatInfo;
</script>

<div class="flex items-center">
    <SystemAgents agents={event.agents} {info}></SystemAgents>
    {#if event.by}
        <span> removed by </span>
        <User
            element={{
                user_id: event.by,
                type: "user",
                element: null,
            }}
            {info}
        />
    {/if}
</div>
