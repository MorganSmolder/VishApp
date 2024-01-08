<script lang="ts">
    import { createEventDispatcher } from "svelte";
    
    let contentActive = false;

    const dispatch = createEventDispatcher();

    function NotifyClick() {
        dispatch("click", {});
    }

    export let title: string;
</script>

<button
    on:mouseenter={() => contentActive = true}
    on:mouseleave={() => contentActive = false}
    class="rounded_border"
>
    <slot name="icon" />
    <slot name="visible_content" />
    <h1>{title}</h1>
    {#if contentActive}
        <slot name="content" />
    {/if}
</button>

<style>
    h1 {
        font-size: 1rem;
        margin: 0;
        margin-top: 10px;
    }

    button {
        display: flex;
        flex-direction: column;
        row-gap: 0;
        padding: 10px;
        width: 80px;
        height: 80px;
        cursor: pointer;
        background-color: white;
        color: black;
        font-size: 100%;
        align-items: center;
        justify-content: center;
    }

    button:hover {
        border-bottom: 5px solid #13132f;
        border-left: 2px solid #13132f;
        border-right: 2px solid #13132f;
        border-top: 1px solid #13132f;
    }
</style>
