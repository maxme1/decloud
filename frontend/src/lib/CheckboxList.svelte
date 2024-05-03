<script lang="ts">
    import { Checkbox } from "flowbite-svelte";

    export let names: string[];
    export let active: Set<string> = new Set();

    $: active = new Set(names);

    function toggleUser(name: string) {
        return () => {
            if (active === undefined) {
                active = new Set(names);
            }

            if (active.has(name)) {
                active.delete(name);
            } else {
                active.add(name);
            }
            active = new Set([...active]);
        };
    }
</script>

<div>
    {#each names as name}
        <Checkbox checked={active.has(name)} on:change={toggleUser(name)}
            >{name}</Checkbox
        >
    {/each}
</div>
