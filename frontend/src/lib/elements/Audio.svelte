<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Audio } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let element: Audio;
    export let info: ChatInfo;
</script>

{#if element.url}
    <audio controls>
        <source src={element.url} />
        Your browser does not support the audio element.
    </audio>
{:else}
    <Icon icon="grommet-icons:document-missing" width="3em" height="3em" />
{/if}

<!-- TODO -->
<!-- type={message.mime_type ?? "video/mp4"} -->
