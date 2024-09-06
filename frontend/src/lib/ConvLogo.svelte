<script lang="ts">
    import Icon from "@iconify/svelte";
    import type { Chat } from "./client";

    export let conv: Chat;
    const logos = new Map([
        ["slack", "tabler:brand-slack"],
        ["telegram-sdk", "tabler:brand-telegram"],
        ["telegram-export", "tabler:brand-telegram"],
    ]);
</script>

<Icon icon={logos.get(conv.source) ?? "tabler:question-mark"}></Icon>
