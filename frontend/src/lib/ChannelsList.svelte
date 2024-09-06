<script lang="ts">
    import type { Chat } from "./client";

    export let channels: Chat[];

    function clipLongName(name: string): string {
        const size = 16;
        return name.length > size ? name.slice(0, size) + "..." : name;
    }
</script>

<div class="overflow-y-auto p-2 m-1">
    <ul>
        {#each channels as channel}
            <li class="w-full">
                <a
                    href="/channels/{channel.source}/{channel.id}"
                    class={"inline-block text-gray-500 dark:text-gray-400 px-2 hover:bg-gray-200 rounded-md p-1 w-full text-left text-nowrap overflow-clip text-clip " +
                        (null === channel ? "bg-gray-300" : "")}
                >
                    <small class="w-full">{clipLongName(channel.name)}</small>
                </a>
            </li>
        {/each}
    </ul>
</div>
