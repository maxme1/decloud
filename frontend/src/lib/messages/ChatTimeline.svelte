<script lang="ts">
    import ChatThread from "./ChatThread.svelte";
    import type { AnyMessage, Chat } from "../client";
    import type { ChatInfo } from "$lib";
    import { elementWalker } from "../utils";
    import Icon from "@iconify/svelte";
    import ConvLogo from "$lib/ConvLogo.svelte";
    import CheckboxList from "$lib/CheckboxList.svelte";

    export let messages: AnyMessage[];
    export let focusedMessage: string | null;
    export let channel: Chat;
    export let info: ChatInfo;

    let element_types = new Map<string, number>();
    let element_enabled = new Set<string>();
    let event_types = new Map<string, number>();
    let event_enabled = new Set<string>();
    let showSettings: boolean = false;

    $: {
        const newTypes = new Map<string, number>();
        const newEvents = new Map<string, number>();
        messages.forEach((message) => {
            let visited = new Set<string>();
            message.elements.forEach((element) => {
                for (const x of elementWalker(element)) {
                    if (!visited.has(x.type)) {
                        newTypes.set(x.type, (newTypes.get(x.type) ?? 0) + 1);
                        visited.add(x.type);
                    }
                }
            });
            if (message.type == "system") {
                newEvents.set(
                    message.event,
                    (newEvents.get(message.event) ?? 0) + 1,
                );
            }
        });
        element_types = newTypes;
        event_types = newEvents;
        element_enabled = new Set(element_types.keys());
        event_enabled = new Set(event_types.keys());
    }

    function anyType(element: any) {
        for (const x of elementWalker(element)) {
            if (element_enabled.has(x.type)) {
                return true;
            }
        }
        return false;
    }

    //         if (message.type == "message") {
    //             if (!currentMedia.has(message.media_type ?? "none")) {
    //                 return false;
    //             }
    //             if (!currentUsers.has(message.from)) {
    //                 return false;
    //             }
    //             if (viaBot !== null && !!message.via_bot !== viaBot) {
    //                 return false;
    //             }
    //             if (
    //                 replied !== null &&
    //                 !!message.reply_to_message_id !== replied
    //             ) {
    //                 return false;
    //             }
</script>

<div class="flex-1 min-w-0">
    <div class="flex items-center">
        <ConvLogo conv={channel} />
        <p class="text-lg font-semibold text-gray-900 dark:text-white mx-1">
            {channel.name}
        </p>
        <button
            class="cursor-pointer ml-auto"
            on:click={() => {
                showSettings = !showSettings;
            }}
        >
            <Icon icon="tabler:settings" width="1em" height="1em" />
        </button>
    </div>
    {#if showSettings}
        <div class="flex items-center">
            <span>Content</span>
            <CheckboxList
                values={element_types}
                active={element_enabled}
                update={(x) => {
                    element_enabled = x;
                }}
            />
        </div>
        <div class="flex items-center">
            <span>Events</span>
            <CheckboxList
                values={event_types}
                active={event_enabled}
                update={(x) => {
                    event_enabled = x;
                }}
            />
        </div>
    {/if}
</div>

<ChatThread
    messages={messages.filter((message) => {
        if (message.type == "agent") {
            return (
                element_types.size == 0 ||
                (element_types.size == element_enabled.size &&
                    message.elements.length == 0) ||
                message.elements.some(anyType) ||
                message.shared.some((shared) => shared.elements.some(anyType))
            );
        } else {
            return event_types.size == 0 || event_enabled.has(message.event);
        }
    })}
    {focusedMessage}
    {info}
/>
