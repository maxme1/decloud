<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Broadcast } from "$lib/client";

    export let element: Broadcast;
    export let info: ChatInfo;
</script>

<span class="bg-amber-300 rounded-xl px-0.5">@{element.range}</span>
