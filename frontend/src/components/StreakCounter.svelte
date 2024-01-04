<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type * as QueryTypes from "../query";

    const dispatch = createEventDispatcher();

    function GetCurrentStreak()
    {
        return 0;
    }

</script>
<h1>Current Streak: {GetCurrentStreak()}</h1>

<style>
    h1{
        font-size: 1rem;
    }
</style>