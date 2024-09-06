<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Join } from "$lib/client";
    import User from "$lib/elements/User.svelte";
    import SystemAgents from "$lib/messages/SystemAgents.svelte";

    export let event: Join;
    export let info: ChatInfo;
</script>

<div class="flex items-center">
    <SystemAgents agents={event.agents} {info}></SystemAgents>
    {#if event.by}
        <span> by invitation from </span>
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
