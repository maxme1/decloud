<script lang="ts">
    import type { Message } from "./timeline";

    export let group: Message[];
</script>

<div class="flex-1 min-w-0">
    {#each group as message}
        {#if message.action === "phone_call"}
            <p class="text-sm text-gray-500 dark:text-gray-400">
                {message.actor}
                {message.action}
                {#if message.discard_reason !== undefined}
                    {message.discard_reason}
                {/if}
            </p>
        {/if}
    {/each}
</div>
