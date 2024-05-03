<script lang="ts">
    import { Indicator, Avatar, Badge, Img, Video } from "flowbite-svelte";
    import type { Message } from "./timeline";
    import { filesRoot } from "$lib";
    import ZoomableImage from "./ZoomableImage.svelte";

    export let message: Message;
    const hasBadge =
        message.edited !== undefined ||
        message.reply_to_message_id !== undefined ||
        message.forwarded_from !== undefined ||
        message.via_bot !== undefined;
</script>

<div class="relative root m-1 rounded">
    <div class="flex flex-col hover:bg-gray-100">
        <!-- media -->
        <div>
            {#if message.photo}
                <ZoomableImage
                    src={filesRoot + message.photo}
                    class="max-h-48"
                />
            {/if}

            {#if message.media_type === "sticker"}
                {#if message.file?.endsWith(".tgs")}
                    <!-- FIXME -->
                    <Img
                        src={filesRoot + message.thumbnail}
                        class="max-h-36"
                        style="filter: drop-shadow(3px 3px 3px #aaa)"
                    />{:else}
                    <Img
                        src={filesRoot + message.file}
                        class="max-h-36"
                        style="filter: drop-shadow(3px 3px 3px #aaa)"
                    />
                {/if}
            {:else if message.media_type === "animation"}
                {#if message.mime_type === "image/gif"}
                    <Img
                        src={filesRoot + message.file}
                        class="max-h-36 rounded"
                    />
                {:else}
                    <Video
                        src={filesRoot + message.file}
                        muted
                        autoplay
                        loop
                        type={message.mime_type ?? "video/mp4"}
                        class="max-h-36 rounded"
                    />
                {/if}
            {:else if message.media_type === "video_file" || message.media_type === "video_message"}
                <Img
                    src={filesRoot + (message.thumbnail ?? message.file)}
                    class="max-h-48 rounded"
                />
            {:else if message.media_type == "audio_file" || message.media_type == "voice_message"}
                <audio controls>
                    <source
                        src={filesRoot + message.file}
                        type={message.mime_type}
                    />
                    Your browser does not support the audio element.
                </audio>
            {:else if message.file}
                {console.log("Unknown media type: " + message.media_type)}
                SOME FILE
            {/if}
        </div>

        {#if message.location_information}
            <div class="flex items">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    {message.location_information.latitude},
                    {message.location_information.longitude}
                </p>
            </div>
        {/if}

        {#if message.contact_information}
            <div class="flex items">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    {message.contact_information.phone_number},
                    {message.contact_information.first_name},
                    {message.contact_information.last_name}
                </p>
            </div>
        {/if}

        {#if message.live_location_period_seconds !== undefined}
            <div class="flex items">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    {message.live_location_period_seconds}
                </p>
            </div>
        {/if}

        <!-- <p class="text-sm text-gray-500 dark:text-gray-400"> -->

        <!-- text -->
        <div>
            {#each message.text_entities as entity}
                {#if entity.type === "plain" || entity.type === "hashtag" || entity.type === "email" || entity.type === "phone" || entity.type === "mention"}
                    <span class="whitespace-pre-line">{entity.text}</span>
                {:else if entity.type === "bold"}
                    <strong>{entity.text}</strong>
                {:else if entity.type === "italic"}
                    <em>{entity.text}</em>
                {:else if entity.type == "link"}
                    <a href={entity.text} class="text-blue-500">{entity.text}</a
                    >
                {:else if entity.type == "text_link"}
                    <a href={entity.href} class="text-blue-500">{entity.text}</a
                    >
                {:else if entity.type === "code"}
                    <span
                        class="whitespace-pre-wrap overflow-auto bg-gray-300 rounded p-0.5"
                        >{entity.text}</span
                    >
                {:else if entity.type === "pre"}
                    <pre
                        class="whitespace-pre-wrap overflow-auto bg-gray-300 rounded p-1.5">{entity.text}</pre>
                {:else}
                    {console.log("Unknown entity type: " + entity.type)}
                {/if}
            {/each}
        </div>
    </div>

    <div class="absolute bottom-0 right-0 flex">
        <small class="overlay">{message.date}</small>

        {#if hasBadge}
            <Badge color="dark" rounded class="px-2.5 py-0.5 ml-auto">
                {#if message.edited !== undefined}
                    <Indicator color="gray" size="xs" class="me-1" />Edited {message.edited}
                {/if}

                {#if message.reply_to_message_id !== undefined}
                    <Indicator color="green" size="xs" class="me-1" />Replied
                {/if}

                {#if message.forwarded_from !== undefined}
                    <Indicator color="green" size="xs" class="me-1" />Forwarded
                    from {message.forwarded_from}
                {/if}
                {#if message.via_bot !== undefined}
                    <Indicator color="green" size="xs" class="me-1" />Via bot {message.via_bot}
                {/if}
            </Badge>
        {/if}
    </div>
</div>

<style>
    .root:not(:hover) .overlay {
        display: none;
    }
</style>
