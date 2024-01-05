<script lang="ts">
    import { onMount } from 'svelte'; 
    import { createEventDispatcher } from "svelte";
    import { scale, fade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';

    let active = true;

    let init = false;
	
    onMount(() => {
      init = true;
    });

    function GetCurrentStreak()
    {
        return 0;
    }

</script>

{#if active}
<column transition:fade={{ delay: 0, duration: 300 }} class="rounded_border">
    <lord-icon
        src="https://cdn.lordicon.com/sbrtyqxj.json"
        trigger="hover"
        style="width:50px;height:50px">
    </lord-icon>
    <h1>Streak: {GetCurrentStreak()}</h1>
</column>
{/if}
<style>
    h1{
        font-size: 1rem;
        margin: 0;
        margin-top: 10px;
    }

    column{
        row-gap: 0;
        padding: 10px;
    }
</style>