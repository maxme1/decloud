<script lang="ts">
    import ChatThread from "./ChatThread.svelte";
    import type { AnyMessage, Chat } from "../client";
    import type { ChatInfo } from "$lib";
    import { elementWalker } from "../utils";

    export let messages: AnyMessage[];
    export let focusedMessage: string | null;
    export let channel: Chat;
    export let info: ChatInfo;

    let element_types = new Map<string, number>();
    let element_enabled = new Set<string>();
    let event_types = new Map<string, number>();
    let event_enabled = new Set<string>();

    $: {
        element_types = new Map<string, number>();
        event_types = new Map<string, number>();
        messages.forEach((message) => {
            let visited = new Set<string>();
            message.elements.forEach((element) => {
                for (const x of elementWalker(element)) {
                    if (!visited.has(x.type)) {
                        element_types.set(
                            x.type,
                            (element_types.get(x.type) ?? 0) + 1,
                        );
                        visited.add(x.type);
                    }
                }
            });
            if (message.type == "system") {
                event_types.set(
                    message.event,
                    (event_types.get(message.event) ?? 0) + 1,
                );
            }
        });
        element_enabled = new Set(element_types.keys());
        event_enabled = new Set(event_types.keys());
    }

    // export let users: string[];
    // export let mediaTypes: string[];
    // export let textTypes: string[];

    // let filtered: AnyMessage[] = [];

    // // display
    // let showStats: boolean = false;

    // // filters
    // let showFilters: boolean = false;
    // let textFilter: string = "";
    // const allTypes = ["message", "service"];
    // let currentUsers = new Set<string>();
    // let currentMedia = new Set<string>();
    // let currentTextTypes = new Set<string>();
    // let currentTypes = new Set<string>(allTypes);
    // let viaBot: boolean | null = null;
    // let replied: boolean | null = null;

    // $: {
    //     filtered = messages.filter((message) => {
    //         // text
    //         if (
    //             textFilter !== "" &&
    //             message.text_entities.find((entity) =>
    //                 entity.text.includes(textFilter),
    //             ) === undefined
    //         ) {
    //             return false;
    //         }
    //         // type
    //         if (!currentTypes.has(message.type)) {
    //             return false;
    //         }
    //         // message-specific
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
    //             if (
    //                 currentTextTypes.size < textTypes.length &&
    //                 !message.text_entities.some((entity) =>
    //                     currentTextTypes.has(entity.type),
    //                 )
    //             ) {
    //                 return false;
    //             }
    //         }

    //         return true;
    //     });
    // }
</script>

<div class="flex-1 min-w-0">
    <p class="text-lg font-semibold text-gray-900 dark:text-white">
        {channel.name}
    </p>
    <div class="flex">
        {#each element_types.entries() as entry}
            <button
                class={"text-sm text-gray-500 dark:text-gray-400 rounded-sm p-1 m-1 " +
                    (element_enabled.has(entry[0])
                        ? "bg-slate-200"
                        : "bg-slate-100")}
                on:click={() => {
                    if (element_enabled.has(entry[0])) {
                        element_enabled.delete(entry[0]);
                    } else {
                        element_enabled.add(entry[0]);
                    }
                    element_enabled = new Set(element_enabled);
                }}
                on:contextmenu|preventDefault={() => {
                    if (
                        element_enabled.size == 1 &&
                        element_enabled.has(entry[0])
                    ) {
                        element_enabled = new Set(element_types.keys());
                    } else {
                        element_enabled = new Set([entry[0]]);
                    }
                }}
            >
                {entry[0]}: {entry[1]}
            </button>
        {/each}
    </div>
    <div class="flex">
        {#each event_types.entries() as entry}
            <button
                class={"text-sm text-gray-500 dark:text-gray-400 rounded-sm p-1 m-1 " +
                    (event_enabled.has(entry[0])
                        ? "bg-slate-200"
                        : "bg-slate-100")}
                on:click={() => {
                    if (event_enabled.has(entry[0])) {
                        event_enabled.delete(entry[0]);
                    } else {
                        event_enabled.add(entry[0]);
                    }
                    event_enabled = new Set(event_enabled);
                }}
                on:contextmenu|preventDefault={() => {
                    if (
                        event_enabled.size == 1 &&
                        event_enabled.has(entry[0])
                    ) {
                        event_enabled = new Set(event_types.keys());
                    } else {
                        event_enabled = new Set([entry[0]]);
                    }
                }}
            >
                {entry[0]}: {entry[1]}
            </button>
        {/each}
    </div>
</div>

<ChatThread
    messages={messages.filter((message) => {
        if (message.type == "agent") {
            return (
                element_types.size == 0 ||
                message.elements.some((element) => {
                    for (const x of elementWalker(element)) {
                        if (element_enabled.has(x.type)) {
                            return true;
                        }
                    }
                    return false;
                })
            );
        } else {
            return event_types.size == 0 || event_enabled.has(message.event);
        }
    })}
    {focusedMessage}
    {info}
/>
