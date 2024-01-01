<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type * as QueryTypes from "../query";

    const dispatch = createEventDispatcher();

    export let currentDate: Date;
    export let journalEntries: QueryTypes.IJournalEntries;

    function GetActiveDay() {
        return currentDate.getDate();
    }

    var details = {
        weekDays: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
        months: [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    };

    function NotifyDateSelected(targetDate: Date) {
        dispatch("dateselected", {
            date: targetDate,
        });
    }

    function NavigateRight() {
        var targetDate =
            currentDate.getMonth() === 11
                ? new Date(currentDate.getFullYear() + 1, 0)
                : new Date(
                      currentDate.getFullYear(),
                      currentDate.getMonth() + 1,
                  );
        NotifyDateSelected(targetDate);
    }

    function NavigateLeft() {
        var targetDate =
            currentDate.getMonth() === 0
                ? new Date(currentDate.getFullYear() - 1, 11)
                : new Date(
                      currentDate.getFullYear(),
                      currentDate.getMonth() - 1,
                  );
        NotifyDateSelected(targetDate);
    }

    function NavigateToDay(day: number) {
        var targetDate = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            day,
        );
        NotifyDateSelected(targetDate);
    }

    function MonthDays(date: Date) {
        var d = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        return d.getDate();
    }

    const today = new Date();
    function DayIsFuture(day: number) {
        var test = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            day,
        );
        return test > today;
    }
</script>

<column>
    <expand_row>
        <button on:click={NavigateLeft}>&lt;</button>
        <span>{details.months[currentDate.getMonth()]}</span>
        <span>{currentDate.getFullYear().toString()}</span>
        <button on:click={NavigateRight}>&gt;</button>
    </expand_row>
    <table class="table">
        {#each { length: 6 } as _, i}
            {@const start = new Date(
                currentDate.getFullYear(),
                currentDate.getMonth(),
            ).getDay()}
            <tr>
                {#each { length: 7 } as _, j}
                    {@const day = j + i * 7 - 7 + 1 - start}
                    {#if i === 0}
                        <td>{details.weekDays[j]}</td>
                    {:else if day > MonthDays(currentDate)}
                        <td>&nbsp;</td>
                    {:else if i === 1 && j < start}
                        <td>&nbsp;</td>
                    {:else}
                        {@const targetClass = DayIsFuture(day)
                            ? "day future_day"
                            : day === GetActiveDay()
                              ? "day active_day"
                              : "day"}
                        <td
                            class={targetClass}
                            on:click={() => NavigateToDay(day)}
                        >
                            <span>{day}</span>
                            {#if journalEntries !== undefined && journalEntries.data[day] !== undefined}
                                <dot></dot>
                            {/if}
                        </td>
                    {/if}
                {/each}
            </tr>
        {/each}
    </table>
</column>

<style>
    @import "../shared.css";
    .fa {
        font-size: 0.5em;
    }
    th {
        text-align: center;
    }
    td {
        width: 30px;
        height: 30px;
        text-align: center;
        font-size: 12px;
        border-radius: 5px;
        position: relative;
    }
    .day:hover {
        background-color: #ff3f8f;
        color: white;
        cursor: pointer;
    }

    .active_day {
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
    }

    button {
        padding: 10px;
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
</style>
