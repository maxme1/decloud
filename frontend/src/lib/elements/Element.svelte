<script lang="ts">
    import type { RichText } from "$lib/client";
    import type { ChatInfo } from "$lib";
    import RichTextSection from "./RichTextSection.svelte";
    import Text from "./Text.svelte";
    import Emoji from "./Emoji.svelte";
    import User from "./User.svelte";
    import Link from "./Link.svelte";
    import RichTextList from "./RichTextList.svelte";
    import RichTextPreformatted from "./RichTextPreformatted.svelte";
    import RichTextQuote from "./RichTextQuote.svelte";
    import Channel from "./Channel.svelte";
    import Broadcast from "./Broadcast.svelte";
    import PlainText from "./PlainText.svelte";
    import UserGroup from "./UserGroup.svelte";
    import Markdown from "./Markdown.svelte";
    import Image from "./Image.svelte";

    export let element: RichText["elements"][0];
    export let info: ChatInfo;

    const components = new Map<string, any>([
        ["emoji", Emoji],
        ["user", User],
        ["link", Link],
        ["text", Text],
        ["plain_text", PlainText],
        ["channel", Channel],
        ["broadcast", Broadcast],
        ["rich_text_preformatted", RichTextPreformatted],
        ["rich_text_section", RichTextSection],
        ["rich_text_quote", RichTextQuote],
        ["rich_text_list", RichTextList],
        ["usergroup", UserGroup],
        ["mrkdwn", Markdown],
        ["image", Image],
    ]);
</script>

{#if !components.has(element.type)}
    !!!Element type: {element.type}!!!
    {console.log(`!!!Element type: ${element.type}!!!`)}
{:else}
    <svelte:component this={components.get(element.type)} {element} {info}
    ></svelte:component>
{/if}
