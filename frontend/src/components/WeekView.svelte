<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let selectedDate: Date;
    export let hasEntry: boolean[];

    const currentDate = new Date();
    const weekDays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

    const dispatch = createEventDispatcher();

    function NotifyDateSelected(targetDate: Date) {
        dispatch("dateselected", {
            date: targetDate,
        });
    }
</script>

<row_fixed>
    {#each Array.from({ length: 7 }, (v, i) => {
        let d = currentDate.getDay() - i;
        if (d < 0) {
            d += 7;
        }
        return { day: d, idx: 6 - i };
    }).reverse() as index}
        {@const classname =
            index.day == currentDate.getDay() ? "active_day" : ""}
        {@const hasEntryForDay = hasEntry !== undefined && hasEntry[index.idx]}
        <day
            class={classname}
            on:click={() => {
                const date = new Date(currentDate.getTime());
                date.setDate(date.getDate() + index.idx - 6);
                NotifyDateSelected(date);
            }}
            ><column>
                <span>{weekDays[index.day]}</span>
                {#if index.day == currentDate.getDay()}
                    <span>Today</span>
                {/if}
                {#if hasEntryForDay}
                    <dot></dot>
                {/if}
            </column></day
        >
    {/each}
</row_fixed>

<style>
    day {
        width: 60px;
        height: 60px;
        text-align: center;
        font-size: 12px;
        border-radius: 5px;
        position: relative;
        /* box-shadow: 0 0 5px rgba(0, 0, 0, 0.2); */
        margin: 5px;
        border-bottom: 5px solid #ddd;
        background-color: #f5f5f5;
    }

    day:hover {
        background-color: rgb(254, 115, 173);
        border-bottom: 5px solid #9f5b78;
        color: white;
        cursor: pointer;
    }

    .active_day {
        /* background-color: #ff65a5;
        color: white;
        border-bottom: 5px solid #9f5b78; */
    }

    dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        display: block;
        background-color: #ff3f8f;
        position: absolute;
        bottom: 5%;
        right: 50%;
        transform: translate(50%, 0%);
    }

    .future_day {
        background-color: rgba(0, 0, 0, 0.1);
        pointer-events: none;
    }

    row {
        padding: 20px;
    }

    column {
        height: 100%;
        row-gap: 0;
    }
    h2 {
        margin: 0%;
    }

    @media only screen and (max-width: 1000px) {
        day {
            width: 40px;
            height: 40px;
        }
    }
</style>
