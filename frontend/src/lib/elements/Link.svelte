<script lang="ts">
    import type { ChatInfo } from "$lib";
    import type { Link } from "$lib/client";

    export let element: Link;
    export let info: ChatInfo;
</script>

<!-- TODO: element style -->
<a href={element.url} class="text-blue-500">{element.text ?? element.url}</a>
