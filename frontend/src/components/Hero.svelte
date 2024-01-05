<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import Meditate from "./Meditate.svelte";

    const dispatch = createEventDispatcher();

    function NotifyStart() {
        dispatch("start", {});
    }

</script>

<hero>
    <container>
        <row>
            <Meditate ></Meditate>
            <column class="left">
                <heading> MindSpace </heading>
                <p>A streak-driven journalling experience</p>
                <button class="jumbo_button" on:click={NotifyStart}>Get Started</button>
            </column>
        </row>
    </container>
</hero>

<style>
    hero {
        width: 100%;
        min-height: 400px;
        font-size: 36px;
        background-color: var(--color-bg-2);
        display: block;
        padding-bottom: 20px;
        text-align: center;
    }

    heading {
        color: white;
        background-color: #13132f;
        /* var(--color-theme-1); */
        padding: 20px;
        border-radius: 20px;
        font-weight: bold;

        font-size: 64px;
        text-align: center;

    }

    p {
        margin: 0;
        font-weight: bold;
    }

    .left {
        min-width: 600px;
    }

    button:hover {
        background-color: #ff3f8f;
    }
</style>
