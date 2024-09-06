<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Channel } from "$lib/client";
    import { channels } from "$lib/store";

    export let element: Channel;
    export let info: ChatInfo;

    let channel;
    if (element.channel_id === null) {
        channel = "[Unknown]";
    } else {
        const found = $channels.find(
            (channel) => channel.id === element.channel_id,
        );
        if (found === undefined) {
            console.error(`Unknown channel ID: ${element.channel_id}`);
            channel = `[Unknown (${element.channel_id})]`;
        } else {
            channel = found.name;
        }
    }
</script>

<span class="bg-amber-300 rounded-xl px-0.5">#{channel}</span>
