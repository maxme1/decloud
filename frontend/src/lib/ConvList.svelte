<script lang="ts">
    import type { Chat } from "./client";
    import { activeChannel } from "./store";
    import ConvLogo from "./ConvLogo.svelte";
    import { base } from "$app/paths";

    export let channels: Chat[];

    function clipLongName(name: string): string {
        const size = 16;
        return name.length > size ? name.slice(0, size) + "..." : name;
    }
</script>

<div class="overflow-y-auto p-1 m-1">
    <ul>
        {#each channels as channel}
            <li class="w-full">
                <a
                    href="{base}/channels/{channel.source}/{channel.id}"
                    class="text-gray-500 dark:text-gray-400 hover:bg-gray-200 rounded-md py-1 px-0.5 w-full text-left flex items-center text-nowrap text-clip"
                    class:bg-gray-300={channel.id ===
                        $activeChannel?.channel.id}
                >
                    <div class="w-4 h-4 mr-1">
                        <ConvLogo conv={channel} />
                    </div>
                    <small>{clipLongName(channel.name)}</small>
                </a>
            </li>
        {/each}
    </ul>
</div>
