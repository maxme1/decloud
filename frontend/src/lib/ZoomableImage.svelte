<script lang="ts">
    export let src: string;
    let className: string = "";
    export { className as class };

    let zoom: boolean = false;

    function toggleZoom() {
        zoom = !zoom;
    }
</script>

{#if zoom}
    <div
        on:click={toggleZoom}
        class="fixed top-0 left-0 z-10 w-screen h-screen flex justify-center bg-gray-900 bg-opacity-90"
    >
        <img {src} class="p-2 fit" on:click={toggleZoom} />
    </div>
{/if}
<img {src} class={className} on:click={toggleZoom} />

<style>
    .fit {
        object-fit: contain;
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
    }
</style>
