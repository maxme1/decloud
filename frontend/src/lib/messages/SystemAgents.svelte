<script lang="ts">
    import User from "../elements/User.svelte";
    import { type ChatInfo } from "$lib";

    export let agents: (string | null)[];
    export let info: ChatInfo;
</script>

{#each agents as agent}
    {#if agent}
        <User
            element={{
                user_id: agent,
                type: "user",
                element: null,
            }}
            {info}
        />
    {/if}
{/each}
