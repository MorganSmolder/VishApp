<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type * as QueryTypes from "../query";

    const dispatch = createEventDispatcher();

    export let journalEntries: QueryTypes.IJournalEntries;

    function GetCurrentStreak()
    {
        if(journalEntries === undefined || journalEntries.lastEntry === null)
        {
            return 0;
        }

        var difference = new Date().getTime()  - journalEntries.lastEntry.getTime() ;
        var days = Math.ceil(difference / (1000 * 3600 * 24));

        return days;
    }

</script>
<h1>Current Streak: {GetCurrentStreak()}</h1>
<style>
    @import "../shared.css";

</style>
