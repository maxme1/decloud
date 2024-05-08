<script lang="ts">
    import { Checkbox } from "flowbite-svelte";

    export let active: boolean | null;
    $: active = null;
</script>

<div>
    <Checkbox
        checked={active == null || active}
        on:change={() => {
            if (active == null || active) {
                active = false;
            } else if (active) {
                active = null;
            }
        }}>Yes</Checkbox
    >
    <Checkbox
        checked={active == null || !active}
        on:change={() => {
            if (active == null || !active) {
                active = true;
            } else {
                active = null;
            }
        }}>No</Checkbox
    >
</div>
