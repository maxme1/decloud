<script lang="ts">
    import { Img } from "flowbite-svelte";
    import type { Service } from "./timeline";
    import { filesRoot } from "$lib";

    export let group: Service[];

    const simple: Record<string, string> = {
        migrate_to_supergroup: "migrated to supergroup",
        migrate_from_supergroup: "migrated from supergroup",
        migrate_from_group: "migrated from group",
        create_group: "created the group",
        phone_call: "called",
    };
</script>

<div class="flex min-w-0 text-sm text-gray-500 dark:text-gray-400">
    <span>
        {group[0].actor}
    </span>
    <div class="">
        {#each group as message, idx}
            <span class="pl-1">
                {#if message.action === "invite_members"}
                    invited {message.members}
                {:else if message.action === "edit_group_photo"}
                    changed the group photo {#if message.photo}to <Img
                            src={filesRoot + message.photo}
                            class="max-h-12 rounded"
                        />{/if}
                {:else if simple[message.action] !== undefined}
                    {simple[message.action]}
                {:else}
                    {console.log("Unknown action: " + message.action)}
                {/if}
            </span>
            <span
                >{#if idx < group.length - 1},{/if}</span
            >
        {/each}
    </div>
</div>
