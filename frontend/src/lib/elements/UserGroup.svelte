<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { UserGroup } from "$lib/client";

    export let element: UserGroup;
    export let info: ChatInfo;

    let agent;
    if (element.usergroup_id === null) {
        agent = "[Unknown]";
    } else {
        const found = info.agents.find((agent) => agent.id === element.usergroup_id);
        if (found === undefined) {
            console.error(`Unknown agent ID: ${element.usergroup_id}`);
            agent = "[Unknown]";
        } else {
            agent = found.name;
        }
    }
</script>

<span class="bg-amber-300 rounded-xl px-0.5">@{agent}</span>
