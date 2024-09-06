<script lang="ts">
    import type { AgentMessage } from "$lib/client";
    import type { ChatInfo } from "$lib";
    import Section from "./Section.svelte";
    import RichText from "./RichText.svelte";
    import Call from "./Call.svelte";
    import Image from "./Image.svelte";
    import File from "./File.svelte";
    import Video from "./Video.svelte";
    import Audio from "./Audio.svelte";
    import Actions from "./Actions.svelte";
    import Context from "./Context.svelte";
    import Header from "./Header.svelte";

    export let block: AgentMessage["blocks"][0];
    export let info: ChatInfo;

    const components = new Map<string, any>([
        ["section", Section],
        ["rich_text", RichText],
        ["call", Call],
        ["image", Image],
        ["file", File],
        ["video", Video],
        ["audio", Audio],
        ["actions", Actions],
        ["context", Context],
        ["header", Header],
    ]);
</script>

{#if !components.has(block.type)}
    !!!Block type: {block.type}!!!
    {console.log(`!!!Block type: ${block.type}!!!`)}
{:else}
    <svelte:component this={components.get(block.type)} {block} {info}
    ></svelte:component>
{/if}
<!-- {#if entity.type === "plain" || entity.type === "hashtag" || entity.type === "email" || entity.type === "phone" || entity.type === "mention"}
                {:else if entity.type === "bold"}
                    <strong>{entity.text}</strong>
                {:else if entity.type === "italic"}
                    <em>{entity.text}</em>
                {:else if entity.type === "code"}
                    <span
                        class="whitespace-pre-wrap overflow-auto bg-gray-300 rounded p-0.5"
                        >{entity.text}</span
                    >
                {/if} -->
