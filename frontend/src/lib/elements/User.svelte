<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { User } from "$lib/client";

    export let element: User;
    export let info: ChatInfo;

    let agent;
    if (element.user_id === null) {
        agent = "[Unknown @]";
    } else {
        const found = info.agents.find((agent) => agent.id === element.user_id);
        if (found === undefined) {
            console.error(`Unknown agent ID: ${element.user_id}`);
            agent = `[Unknown @${element.user_id}]`;
        } else {
            agent = `@${found.name}`;
        }
    }
</script>

<span class="bg-amber-300 rounded-xl px-0.5">{agent}</span>
