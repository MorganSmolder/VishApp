<script lang="ts">
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    function NotifyTabChange() {
        dispatch("tabchange", {});
    }

    export let headerA: string;
    export let headerB: string;
    export let headerC: string;

    let activeTab = 0;

    function TabA() {
        activeTab = 0;
        NotifyTabChange();
    }

    function TabB() {
        activeTab = 1;
        NotifyTabChange();
    }

    function TabC(){
        activeTab = 2;
        NotifyTabChange();
    }

    onMount(async () => {});
</script>

    <row>
        <button class="tab {activeTab == 0 ? "selected_tab" : ""}"  on:click={TabA}>{headerA}</button>
        <button class="tab {activeTab == 1 ? "selected_tab" : ""}" on:click={TabB}>{headerB}</button>
        <button class="tab {activeTab == 2 ? "selected_tab" : ""}" on:click={TabC}>{headerC}</button>
    </row>
    <div class="tab_content">
        {#if activeTab == 0}
            <slot name="body_a" />
        {:else if activeTab == 1}
            <slot name="body_b" />
        {:else}
            <slot name="body_c" />
        {/if}
    </div>

<style>
    row{
        align-items: stretch;
        width: 100%;

    }
    
    .tab{
        display: block;
        padding: 20px;
        flex:1;
        cursor: pointer;
        border-radius: 0;
        color: black;
        background-color: #fff;
        /* box-shadow: inset 0 0 10px rgba(0,0,0,.2); */
        border-right: 1px solid rgba(0, 0, 0, .1);
    }

    .tab:hover{
        background-color: #fba2d0;
        color: white;
    }
    
    .selected_tab{
        box-shadow: 0 0 10px rgba(0,0,0,.2);    
        z-index: 1;
        /* color: white; */
        background-color: #ff0069;
        color:white;
    }

    .tab_content{
        z-index: 2;
        background-color: #fff;
        position: relative;
        
        box-shadow: 0 0 10px rgba(0,0,0,.2);   
    }
</style>
