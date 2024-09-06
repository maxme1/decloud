<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Element } from "$lib/client";
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
    import Video from "./Video.svelte";
    import Audio from "./Audio.svelte";
    import Call from "./Call.svelte";
    import Actions from "./Actions.svelte";
    import Context from "./Context.svelte";
    import Header from "./Header.svelte";
    import File from "./File.svelte";
    import Contact from "./Contact.svelte";
    import Location from "./Location.svelte";
    import Sticker from "./Sticker.svelte";

    export let element: Element;
    export let info: ChatInfo;

    const components = new Map<string, any>([
        ["user", User],
        ["channel", Channel],
        ["broadcast", Broadcast],
        ["usergroup", UserGroup],

        ["contact", Contact],
        ["location", Location],

        ["button", Button],
        // ["call", Call],
        ["actions", Actions],
        ["context", Context],
        ["header", Header],

        ["image", Image],
        ["icon", Icon],
        ["video", Video],
        ["audio", Audio],
        ["file", File],
        ["sticker", Sticker],

        ["sequence", Sequence],
        ["section", Section],
        ["list", List],

        ["pre", Preformat],
        ["quote", Quote],
        ["strike", Strike],
        ["bold", Bold],
        ["italic", Italic],
        ["code", Code],
        ["emoji", Emoji],
        ["link", Link],
        ["text", Text],
    ]);
</script>

{#if !components.has(element.type)}
    !!!Element type: {element.type}!!!
    {console.log(`!!!Element type: ${element.type}!!!`, element)}
{:else}
    <svelte:component this={components.get(element.type)} {element} {info}
    ></svelte:component>
{/if}
