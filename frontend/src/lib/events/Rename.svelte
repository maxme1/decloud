<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Rename } from "$lib/client";
    import SystemAgents from "$lib/messages/SystemAgents.svelte";

    export let event: Rename;
    export let info: ChatInfo;
</script>

<div class="flex items-center">
    <SystemAgents agents={event.agents} {info}></SystemAgents>
    <div class="px-1">
        <span>
            renamed to <span
                ><span class="italic">{event.name}</span>
            </span></span
        >
    </div>
</div>
