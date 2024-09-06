<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Location } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let element: Location;
    export let info: ChatInfo;
</script>

<div class="flex items-center">
    <Icon icon="tabler:map-pin-2" class="w-8 h-8" />
    <div class="flex flex-col ml-2">
        {#if element.address || element.name}
            <small>{element.address ?? ""} {element.name ?? ""}</small>
        {/if}
        {#if element.latitude && element.longitude}
            <small class="flex items-center">
                {element.latitude}, {element.longitude}
            </small>
        {/if}
    </div>
</div>
