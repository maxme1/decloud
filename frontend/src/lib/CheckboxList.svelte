<script lang="ts">
    export let values: Map<string, number>;
    export let active: Set<string>;
    export let update: (active: Set<string>) => void;
</script>

{#each values.entries() as entry}
    <button
        class={"text-sm text-gray-500 dark:text-gray-400 rounded-sm p-1 m-1 " +
            (active.has(entry[0]) ? "bg-slate-200" : "bg-slate-100")}
        on:click={() => {
            const newActive = new Set(active);
            if (newActive.has(entry[0])) {
                newActive.delete(entry[0]);
            } else {
                newActive.add(entry[0]);
            }
            update(newActive);
        }}
        on:contextmenu|preventDefault={() => {
            const newActive =
                active.size === 1 && active.has(entry[0])
                    ? new Set(values.keys())
                    : new Set([entry[0]]);

            update(newActive);
        }}
    >
        {entry[0]}: {entry[1]}
    </button>
{/each}
