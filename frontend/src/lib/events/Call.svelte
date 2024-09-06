<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Call } from "$lib/client";

    export let event: Call;
    export let info: ChatInfo;

    // TODO: accessory?
</script>

{#if event.duration}

{/if}
