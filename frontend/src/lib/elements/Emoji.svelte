<script lang="ts">
    import type { Emoji, ChatInfo } from "$lib/client";
    import EmojiBase from "$lib/EmojiBase.svelte";

    export let element: Emoji;
    export let info: ChatInfo;

    // src: https://stackoverflow.com/questions/51640509/how-do-i-convert-unicode-to-emoji-in-javascript
</script>

<EmojiBase emoji={element} {info} height={8}></EmojiBase>
