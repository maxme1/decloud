<script lang="ts">
    import Block from "./Block.svelte";
    import type { Block as BlockData } from "$lib/client";
    import type { ChatInfo } from "$lib";

    export let blocks: BlockData[];
    export let info: ChatInfo;
</script>

{#each blocks as block}
    <Block {block} {info}></Block>
{/each}
