<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Contact } from "$lib/client";
    import Icon from "@iconify/svelte";

    export let element: Contact;
    export let info: ChatInfo;
</script>

<div class="flex items-center">
    <Icon icon="tabler:address-book" class="w-8 h-8" />
    <div class="flex flex-col ml-2">
        <span>{element.name}</span>
        <small>{element.phone}</small>
    </div>
</div>
