<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Sticker } from "$lib/client";
    import Icon from "@iconify/svelte";
    import Element from "./Element.svelte";
    import { onMount } from "svelte";

    // https://github.com/LottieFiles/svelte-lottie-player/issues/7
    // let LottiePlayer: any = undefined;
    // onMount(async () => {
    //     const module = await import("@lottiefiles/svelte-lottie-player");
    //     LottiePlayer = module.LottiePlayer;
    // });

    export let element: Sticker;
    export let info: ChatInfo;
</script>

{#if element.url}
    {#if element.mimetype?.startsWith("image/")}
        <img
            src={element.url}
            alt={element.emoji?.unicode ?? ""}
            class="max-w-36"
        />
    {:else if element.mimetype === "video/tgs"}
        {#if element.emoji}
            <Element element={element.emoji} {info}></Element>
        {:else}
            <Icon icon="tabler:file-x" width="1em" height="1em" />
        {/if}

        <!-- TODO -->
        <!-- {#if LottiePlayer}
            <LottiePlayer
                src={element.url}
                autoplay={true}
                loop={true}
                controls={false}
                renderer="svg"
                background="transparent"
                controlsLayout={[]}
            />
        {/if} -->
    {:else if element.mimetype?.startsWith("video/")}
        <video src={element.url} muted loop autoplay class="max-w-36" />
    {:else}
        <Icon icon="tabler:file-x" width="1em" height="1em" />
    {/if}
{:else if element.emoji}
    <Element element={element.emoji} {info}></Element>
{:else}
    <Icon icon="tabler:file-x" width="1em" height="1em" />
{/if}
