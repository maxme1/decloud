<script lang="ts">
    import type { EmojiBase, ChatInfo } from "$lib/client";

    export let emoji: EmojiBase;
    export let info: ChatInfo;
    export let height: number;
</script>

<!-- TODO: skin tone -->
{#if emoji.unicode}
    <span style={`font-size: ${height / 6}rem;`}>
        {emoji.unicode}
        <!-- {String.fromCodePoint(
            parseInt(emoji.unicode, 16),
            // parseInt(emoji.skin_tone || 0, 16),
        )} -->
    </span>
{:else if emoji.url}
    <img
        src={emoji.url}
        alt={emoji.name ?? ""}
        class={`inline-block h-${height} w-${height}`}
    />
{:else}
    {console.log("not found emoji", emoji.name, emoji.url)}
    <span style={`font-size: ${height / 6}rem;`}>
        :{emoji.name}:
    </span>
{/if}
