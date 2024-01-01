<script lang="ts">
    import Calender from "../../components/Calender.svelte";
    import Modal from "../../components/Modal.svelte";
    import StreakCounter from "../../components/StreakCounter.svelte";
    import Query from "../../query";
    import type * as QueryTypes from "../../query";
    import { onMount } from "svelte";

    let activeDate = new Date();
    let entryZone: HTMLTextAreaElement;
    let journalEntries: QueryTypes.IJournalEntries;
    let loading = true;

    onMount(async () => {
        ReadJournalEntriesForMonth();
    });

    function ReadJournalEntriesForMonth() {
        loading = true;
        journalEntries = Query.GetJournalEntries(
            activeDate.getFullYear(),
            activeDate.getMonth(),
        );

        UpdateUiForActiveDate();
        loading = false;
    }

    function UpdateUiForActiveDate() {
        entryZone.value = "";

        var entryToday = journalEntries.data[activeDate.getDate()];
        if (entryToday && entryToday.textContent !== null) {
            entryZone.value = entryToday.textContent;
        }
    }

    function StoreEntry() {
        if (loading) {
            return;
        }
        journalEntries.data[activeDate.getDate()] = {
            textContent: entryZone.value,
        };
        journalEntries.lastEntry = activeDate;
        Query.WriteJournalEntries(
            activeDate.getFullYear(),
            activeDate.getMonth(),
            journalEntries,
        );
    }

    function HandleDateSelect(event: any) {
        console.assert(!loading);
        const newDate: Date = event.detail.date;

        var oldDate = activeDate;
        activeDate = newDate;
        if (
            newDate.getMonth() !== oldDate.getMonth() ||
            newDate.getFullYear() !== oldDate.getFullYear()
        ) {
            ReadJournalEntriesForMonth();
        } else {
            UpdateUiForActiveDate();
        }
    }
</script>

<container>
    <column>
        <expand_row>
            <Calender
                {journalEntries}
                currentDate={activeDate}
                on:dateselected={HandleDateSelect}
            ></Calender>
            <StreakCounter {journalEntries}></StreakCounter>
        </expand_row>
        <textarea bind:this={entryZone} on:input={StoreEntry}> </textarea>
    </column>
</container>
<Modal isVisible={false}>
    <column>
        <h1>How This Works</h1>
        <row>
            <column>
                <h2>Log In Every Day</h2>
            </column>
            <column>
                <h2>Write A Journal Entry</h2>
            </column>
            <column>
                <h2>Keep Your Streak Going</h2>
            </column>
        </row>
    </column>
</Modal>

<style>
    @import "../../shared.css";

    textarea {
        width: 100%;
        margin: 2rem;
        margin-top: 0;
        min-height: 500px;
        border: none;
        /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
        padding: 25px;
        border-radius: 25px;
        resize: none;
        font-size: 22px;
        line-height: 25px;
        background: url($lib/images/line.png) repeat;
    }

    textarea:focus-visible {
        border: none;
        outline: none;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }

    h1 {
        margin: 0;
    }
</style>
