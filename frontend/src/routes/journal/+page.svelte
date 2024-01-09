<script lang="ts">
    import Calender from "../../components/Calender.svelte";
    import Modal from "../../components/Modal.svelte";
    import StreakCounter from "../../components/StreakCounter.svelte";
    import Query from "../../query";
    import Login from "../../login";
    import GuestToUserConversionForm from "../../components/GuestToUserConversionForm.svelte";
    import { onMount } from "svelte";
    import ConfirmModal from "../../components/ConfirmModal.svelte";
    import TabView from "../../components/TabView.svelte";
    import MenuItem from "../../components/MenuItem.svelte";
    import AccountManagement from "../../components/AccountManagement.svelte";
    import Lottie from "../../components/Lottie.svelte";

    let activeDate = new Date();
    let entryZone: HTMLTextAreaElement;

    let calenderVisible: boolean = false;

    let monthHasEntry: boolean[];
    let haveEntryForCurrent = false;
    let currentEntry = "";
    let showEditor = false;
    let showConfirm = false;
    let wordCount = 0;
    const minWordCount = 300;

    let streak = 0;

    onMount(async () => {
        await Login.UpdateSignInStatus();
        await ReadJournalEntriesForMonth();
        await GetActiveEntry();
        await GetStreak();

        Query.StartTickingSync();
    });

    async function GetStreak() {
        streak = await Query.GlobalDataStore.GetStreak(new Date());
    }

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
        let oldDate = activeDate;
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

    function FormatDate(date: Date) {
        const months = [
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
        ];

        const day = date.getDate();
        const month = date.getMonth();
        const monthName = months[month];
        let suffix = "";

        // Add the appropriate suffix for the day
        if (day === 1 || day === 21 || day === 31) {
            suffix = "st";
        } else if (day === 2 || day === 22) {
            suffix = "nd";
        } else if (day === 3 || day === 23) {
            suffix = "rd";
        } else {
            suffix = "th";
        }

        return `${monthName} the ${day}${suffix}`;
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

    function DateIsPast(date: Date) {
        const present = new Date();

        return (
            date.getFullYear() < present.getFullYear() ||
            date.getMonth() < present.getMonth() ||
            date.getDate() < present.getDate()
        );
    }

    function DateIsFuture(date: Date) {
        const present = new Date();

        return (
            date.getFullYear() > present.getFullYear() ||
            date.getMonth() > present.getMonth() ||
            date.getDate() > present.getDate()
        );
    }
</script>

<!-- <svelte:window on:beforeunload={BeforeUnload} /> -->
<container>
    <column>
        <!-- <GuestToUserConversionForm></GuestToUserConversionForm> -->
        <expand_row class="head">
            <row_fixed style="gap: 20px;">
                <MenuItem title="Streak">
                    <lord-icon
                        slot="icon"
                        src="https://cdn.lordicon.com/sbrtyqxj.json"
                        trigger="hover"
                        style="width:50px;height:50px"
                    >
                    </lord-icon>
                    <span slot="visible_content">
                        {streak}
                    </span>
                </MenuItem>
                <MenuItem
                    on:click={() => (calenderVisible = !calenderVisible)}
                    title="History"
                >
                    <lord-icon
                        slot="icon"
                        src="https://cdn.lordicon.com/wmlleaaf.json"
                        trigger="hover"
                        style="width:50px;height:50px"
                    >
                    </lord-icon>
                    <div slot="content">
                        <Calender
                            calenderVisible={true}
                            monthHasJournalEntry={monthHasEntry}
                            currentDate={activeDate}
                            on:dateselected={HandleDateSelect}
                        ></Calender>
                    </div>
                </MenuItem>
                <MenuItem title="Account">
                    <lord-icon
                        slot="icon"
                        src="https://cdn.lordicon.com/hrjifpbq.json"
                        trigger="hover"
                        style="width:50px;height:50px"
                    >
                    </lord-icon>
                    <div slot="content">
                        <AccountManagement></AccountManagement>
                    </div>
                </MenuItem>
                <!-- <StreakCounter></StreakCounter> -->
            </row_fixed>
        </expand_row>
        <row style="margin: 20px; width:100%; gap:20px;">
            <column>
                <h1>{FormatDate(activeDate)}</h1>
                <h3 style="margin: 0;">
                    Characters: {currentEntry.length}/{minWordCount}
                </h3>
            </column>
        </row>
        {#if haveEntryForCurrent}
            <textarea style="pointer-events:none;">{currentEntry}</textarea>
        {:else if !showEditor}
            {#if DateIsPast(activeDate)}
                <Lottie src="https://cdn.lordicon.com/uhstaxbs.json"></Lottie>
                <p>
                    Wow, we're in the past! You didn't write a journal entry on
                    this day.
                </p>
            {:else if DateIsFuture(activeDate)}
                <Lottie src="https://cdn.lordicon.com/pcxpjqjz.json"></Lottie>
                <p>
                    Neato, it's the future! You better write a journal entry
                    when this date comes around!
                </p>
            {:else}
                <Lottie src="https://cdn.lordicon.com/lzgqzxrq.json"></Lottie>
                <p>No entry for today!</p>
                <button on:click={() => (showEditor = true)}
                    >Create Entry</button
                >
            {/if}
        {:else}
            <textarea
                bind:this={entryZone}
                on:input={() => (currentEntry = entryZone.value)}
                placeholder="Today I..."
            ></textarea>
            <button on:click={() => (showConfirm = true)}>Submit</button>
        {/if}

        <ConfirmModal
            active={showConfirm}
            on:submit={CommitJournalEntry}
            textContent="Are you sure you want to save? You cannot edit your entry again afterwards."
        ></ConfirmModal>
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
        justify-content: center;
    }

    textarea {
        width: 80%;
        margin: 20px;
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
        row-gap: 10px;
    }

    p{
        text-align: center;
    }
</style>
