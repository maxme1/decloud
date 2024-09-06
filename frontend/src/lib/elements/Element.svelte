<script lang="ts">
    import type { RichText } from "$lib/client";
    import type { ChatInfo } from "$lib";
    import Text from "./Text.svelte";
    import Emoji from "./Emoji.svelte";
    import User from "./User.svelte";
    import Link from "./Link.svelte";
    import List from "./List.svelte";
    import Preformat from "./Preformat.svelte";
    import Channel from "./Channel.svelte";
    import Broadcast from "./Broadcast.svelte";
    import UserGroup from "./UserGroup.svelte";
    import Image from "./Image.svelte";
    import Quote from "./Quote.svelte";
    import Sequence from "./Sequence.svelte";
    import Section from "./Section.svelte";
    import Strike from "./Strike.svelte";
    import Bold from "./Bold.svelte";
    import Italic from "./Italic.svelte";
    import Icon from "./Icon.svelte";
    import Code from "./Code.svelte";
    import Button from "./Button.svelte";

    export let element: RichText["elements"][0];
    export let info: ChatInfo;

    const components = new Map<string, any>([
        ["emoji", Emoji],
        ["user", User],
        ["link", Link],
        ["text", Text],
        ["channel", Channel],
        ["broadcast", Broadcast],
        ["usergroup", UserGroup],

        ["button", Button],

        ["image", Image],
        ["icon", Icon],

        ["sequence", Sequence],
        ["section", Section],
        ["list", List],

        ["pre", Preformat],
        ["quote", Quote],
        ["strike", Strike],
        ["bold", Bold],
        ["italic", Italic],
        ["code", Code],
    ]);
</script>

{#if !components.has(element.type)}
    !!!Element type: {element.type}!!!
    {console.log(`!!!Element type: ${element.type}!!!`, element)}
{:else}
    <svelte:component this={components.get(element.type)} {element} {info}
    ></svelte:component>
{/if}
