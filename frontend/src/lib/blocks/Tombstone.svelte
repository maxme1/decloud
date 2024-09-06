<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Tombstone } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let block: Tombstone;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

<div class="flex items-center text-blue-500 cursor-pointer">
    <Icon icon="tabler:file-x" width="3em" height="3em" />
    <span> This file was deleted </span>
</div>
