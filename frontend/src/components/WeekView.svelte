<script lang="ts">
    export let selectedDate: Date;

    const currentDate = new Date();
    const weekDays = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];
</script>

<row>
    {#each weekDays as day}
        {@const classname =
            weekDays.indexOf(day) == currentDate.getDay() ? "active_day" : ""}
        <day class={classname}><column>
            <span>{day}</span>
            {#if weekDays.indexOf(day) == currentDate.getDay()}
                <span>Today</span>
            {/if}
        </column></day>
    {/each}
</row>

<style>
    day {
        width: 80px;
        height: 80px;
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
        background-color: #ff65a5;
        color: white;
        border-bottom: 5px solid #9f5b78;
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

    column {
        height: 100%;
        row-gap: 0;
    }
</style>
