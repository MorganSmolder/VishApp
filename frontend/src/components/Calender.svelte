<script lang="ts">
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    export let currentDate: Date;
    export let monthHasJournalEntry: Boolean[];

    let calenderVisible = true;

    function GetActiveDay() {
        return currentDate.getDate();
    }

    const details = {
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
        const targetDate =
            currentDate.getMonth() === 11
                ? new Date(currentDate.getFullYear() + 1, 0)
                : new Date(
                      currentDate.getFullYear(),
                      currentDate.getMonth() + 1,
                  );
        NotifyDateSelected(targetDate);
    }

    function NavigateLeft() {
        const targetDate =
            currentDate.getMonth() === 0
                ? new Date(currentDate.getFullYear() - 1, 11)
                : new Date(
                      currentDate.getFullYear(),
                      currentDate.getMonth() - 1,
                  );
        NotifyDateSelected(targetDate);
    }

    function NavigateToDay(day: number) {
        const targetDate = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            day,
        );
        NotifyDateSelected(targetDate);
    }

    function MonthDays(date: Date) {
        const d = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        return d.getDate();
    }

    const today = new Date();
    function DayIsFuture(day: number) {
        const test = new Date(
            currentDate.getFullYear(),
            currentDate.getMonth(),
            day,
        );
        return test > today;
    }
</script>
<div>
    <button on:click={() => calenderVisible = !calenderVisible}>Journal History</button>
    <anchor>
        {#if calenderVisible}
        <table class="calendarParent rounded_border">
            <td>    
                <button on:click={NavigateLeft}>&lt;</button>
            </td>
            <td>
                <span>{details.months[currentDate.getMonth()]}</span>
            </td>
            <td>
                <span>{currentDate.getFullYear().toString()}</span>
            </td>
            <td>
                <button on:click={NavigateRight}>&gt;</button>
            </td>
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
                            {@const targetClass = false//DayIsFuture(day)
                                ? "day future_day"
                                : day === GetActiveDay()
                                  ? "day active_day"
                                  : "day"}
                            <td
                                class={targetClass}
                                on:click={() => NavigateToDay(day)}
                            >
                                <span>{day}</span>
                                {#if monthHasJournalEntry !== undefined && monthHasJournalEntry[day - 1]}
                                    <dot></dot>
                                {/if}
                            </td>
                        {/if}
                    {/each}
                </tr>
            {/each}
        </table>
        {/if}
    </anchor>
</div>
<style>
    .fa {
        font-size: 0.5em;
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
    
    column{
        row-gap: 0;
    }

    table{
        padding: 5px;
    }

    anchor{
        display: block;
        position: relative;
    }

    .calendarParent{
        position: absolute;
        top: 0;
        left: 0;
        background-color: white;
    }
</style>
