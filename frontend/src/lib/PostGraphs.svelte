<script lang="ts">
    import { type VisualizationSpec } from "svelte-vega";
    import { VegaLite } from "svelte-vega";

    export let messages;
    let data = {};
    $: data = {
        table: messages.filter((message: any) => message["from"] !== undefined),
    };

    const monthly: VisualizationSpec = {
        $schema: "https://vega.github.io/schema/vega-lite/v5.json",
        title: "Messages per month",
        data: {
            name: "table",
        },
        mark: { type: "line", tooltip: { content: "data" } },
        encoding: {
            x: { timeUnit: "yearmonth", field: "date" },
            y: { aggregate: "count" },
        },
    };
    const weekly: VisualizationSpec = {
        $schema: "https://vega.github.io/schema/vega-lite/v5.json",
        title: "Messages per weekday",
        data: {
            name: "table",
        },

        layer: [
            {
                mark: { type: "arc", innerRadius: 20, stroke: "#fff" },
            },
            {
                mark: { type: "text", radiusOffset: -15 },
                encoding: {
                    text: {
                        timeUnit: "day",
                        field: "date",
                        type: "ordinal",
                    },
                    color: { value: "#000" },
                },
            },
            {
                mark: { type: "text", radiusOffset: 15 },
                encoding: {
                    text: { aggregate: "count" },
                    color: { value: "#000" },
                },
            },
        ],
        encoding: {
            theta: {
                timeUnit: "day",
                field: "date",
                type: "ordinal",
                stack: true,
                sort: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                scale: {
                    domain: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                },
            },
            radius: {
                aggregate: "count",
                scale: { type: "sqrt", zero: true, rangeMin: 20 },
            },
            color: {
                timeUnit: "day",
                field: "date",
                type: "ordinal",
                legend: null,
            },
        },

        // mark: { type: "bar", width: { band: 0.7 }, cornerRadiusEnd: 4 },
        // encoding: {
        //     x: {
        //         timeUnit: "day",
        //         field: "date",
        //         type: "ordinal",
        //         sort: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        //         scale: {
        //             domain: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        //         },
        //     },
        //     y: { aggregate: "count" },
        // },
    };
    const daily: VisualizationSpec = {
        $schema: "https://vega.github.io/schema/vega-lite/v5.json",
        title: "Messages per time of day",
        data: {
            name: "table",
        },
        mark: { type: "bar", width: { band: 0.7 }, cornerRadiusEnd: 4 },
        encoding: {
            x: {
                timeUnit: "hours",
                field: "date",
            },
            y: { aggregate: "count" },
        },
    };
</script>

<div class="flex flex-col p-4">
    <p class="text-lg font-semibold text-gray-900 dark:text-white">Stats</p>
    <p class="text-sm text-gray-500 dark:text-gray-400">
        Messages: {messages.length}
    </p>
</div>

<div class="flex">
    <VegaLite {data} spec={monthly} />
    <VegaLite {data} spec={weekly} />
    <VegaLite {data} spec={daily} />
</div>
