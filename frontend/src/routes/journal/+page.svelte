<script lang="ts">
    import Calender from "../../components/Calender.svelte";
    import WeekView from "../../components/WeekView.svelte";
    import Modal from "../../components/Modal.svelte";
    import StreakCounter from "../../components/StreakCounter.svelte";
    import Query from "../../query";
    import Login from "../../login";
    import GuestToUserConversionForm from "../../components/GuestToUserConversionForm.svelte";
    import { onMount } from "svelte";
    import ConfirmModal from "../../components/ConfirmModal.svelte";

    let activeDate = new Date();
    let entryZone: HTMLTextAreaElement;

    let monthHasEntry: boolean[];
    let weekHasEntries: boolean[] = Array.from({ length: 7 }, () => false);
    let haveEntryForCurrent = false;
    let currentEntry = "";
    let showEditor = false;
    let showConfirm = false;

    onMount(async () => {
        await Login.UpdateSignInStatus();
        await ReadJournalEntriesForMonth();
        await GetActiveEntry();
        await GetEntriesForWeek();

        Query.StartTickingSync();
    });

    async function ReadJournalEntriesForMonth() {
        monthHasEntry = await Query.GlobalDataStore.GetEntriesForMonth(
            activeDate.getFullYear(),
            activeDate.getMonth(),
        );
    }

    async function GetActiveEntry() {
        const entry = await Query.GlobalDataStore.AccessEntry(activeDate);
        currentEntry = entry.textContent;
        haveEntryForCurrent = !StringIsNullOrWhiteSpace(entry.textContent);
        console.log(entry.textContent);
    }

    async function GetEntriesForWeek() {
        let walk = activeDate;
        for (var i = 6; i >= 0; i--) {
            const entry = await Query.GlobalDataStore.AccessEntry(walk);
            weekHasEntries[i] = !StringIsNullOrWhiteSpace(entry.textContent);
            walk = GetDateDayBefore(walk);
        }
    }

    function GetDateDayBefore(date: Date) {
        var dayBefore = new Date(date.getTime());
        dayBefore.setDate(date.getDate() - 1);
        return dayBefore;
    }

    function StringIsNullOrWhiteSpace(s: string | null) {
        if (s === null) {
            return true;
        }

        for (const i of s) {
            if (i !== " ") {
                return false;
            }
        }

        return true;
    }

    async function StoreEntry() {
        await Query.GlobalDataStore.UpdateEntry(activeDate, entryZone.value);
        monthHasEntry[activeDate.getDate() - 1] = entryZone.value !== "";
    }

    async function HandleDateSelect(event: any) {
        const newDate: Date = event.detail.date;

        console.log(newDate);
        var oldDate = activeDate;
        activeDate = newDate;
        if (
            newDate.getMonth() !== oldDate.getMonth() ||
            newDate.getFullYear() !== oldDate.getFullYear()
        ) {
            await ReadJournalEntriesForMonth();
            await GetActiveEntry();
        } else {
            await GetActiveEntry();
        }
    }

    async function CommitJournalEntry(event: any) {
        showConfirm = false;

        const yes: boolean = event.detail.yes;
        if (!yes) {
            return;
        }
        await StoreEntry();
        currentEntry = entryZone.value;
        haveEntryForCurrent = true;
    }

    // async function BeforeUnload() {
    //     console.log("HI");
    //     // Cancel the event as stated by the standard.
    //     event.preventDefault();
    //     // Chrome requires returnValue to be set.
    //     event.returnValue = "";

    //     await Query.SyncData();

    //     // more compatibility
    //     return "...";
    // }
</script>

<!-- <svelte:window on:beforeunload={BeforeUnload} /> -->
<container>
    <column>
        <GuestToUserConversionForm></GuestToUserConversionForm>
        <expand_row class="head">
            <StreakCounter></StreakCounter>
            <WeekView on:dateselected={HandleDateSelect} hasEntry={weekHasEntries} selectedDate={activeDate}
            ></WeekView>
            <Calender
                monthHasJournalEntry={monthHasEntry}
                currentDate={activeDate}
                on:dateselected={HandleDateSelect}
            ></Calender>
        </expand_row>
        <br />
        {#if haveEntryForCurrent}
            <textarea style="pointer-events:none;">{currentEntry}</textarea>
        {:else if !showEditor}
            <lord-icon
                src="https://cdn.lordicon.com/rnqhxxtn.json"
                trigger="hover"
                style="width:250px;height:250px"
            >
            </lord-icon>
            <p>No entry for today!</p>
            <button on:click={() => (showEditor = true)}>Create Entry</button>
        {:else}
            <textarea bind:this={entryZone} placeholder="Today I..."></textarea>
            <button on:click={() => (showConfirm = true)}>Submit</button>
            <ConfirmModal
                active={showConfirm}
                on:submit={CommitJournalEntry}
                textContent="Are you sure you want to save? You cannot edit your entry again afterwards."
            ></ConfirmModal>
        {/if}
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
    .head {
        /* background-color: white; */
        /* var(--color-bg-1); */
        /* border: 3px solid white; */
        /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); */
        margin-top: 20px;
        /* border:4px solid var(--color-bg-2); */
    }

    textarea {
        width: 100%;
        margin: 2rem;
        margin-top: 0;
        min-height: 400px;
        border: none;
        /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); */
        padding: 25px;
        border-radius: 25px;
        resize: none;
        font-size: 22px;
        line-height: 25px;
        /* background-color: var(--color-bg-1); */

        background-color: white;
        /* background: url($lib/images/line.png) repeat; */
        border: 2px solid #ddd;
    }

    textarea:focus-visible {
        border: none;
        outline: none;
        /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); */
        border: 4px solid #ddd;
    }

    h1 {
        margin: 0;
    }

    column {
        height: 100%;
        row-gap: 0;
    }
</style>
