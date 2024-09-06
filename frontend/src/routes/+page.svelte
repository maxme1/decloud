<script lang="ts">
    import ChannelsList from "$lib/ChannelsList.svelte";
    import { onMount } from "svelte";
    import { channels } from "$lib/store";
    import { ApiService } from "$lib";

    onMount(async () => {
        $channels = await ApiService.chatsChatsGet();
    });
</script>

<div class="flex h-screen w-screen divide-x">
    <ChannelsList channels={$channels}></ChannelsList>
</div>
