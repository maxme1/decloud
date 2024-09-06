<script lang="ts">
    import ChannelsList from "$lib/ChannelsList.svelte";
    import { DefaultService } from "$lib/client";
    import { onMount } from "svelte";
    import { channels } from "$lib/store";

    onMount(async () => {
        $channels = await DefaultService.chatsChatsGet();
    });
</script>

<div class="flex h-screen w-screen divide-x">
    <ChannelsList channels={$channels}></ChannelsList>
</div>
