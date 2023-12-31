<script lang="ts">
    import Icon from "$lib/images/meditate.png";    
    import { onMount } from "svelte";

    let getStarted : HTMLButtonElement;

    onMount(async () => {
        getStarted.onclick = () =>{
            document.location.href = "./journal";
        }
    });
</script>

<hero>
    <container>
        <expand_row>
            <img src={Icon} alt="Logo of man meditating" />
            <column class="left">
                <heading> MindSpace </heading>
                <br />
                <p>A minimal journalling experience</p>
                <br />
                <button bind:this={getStarted} >Get Started</button>
            </column>
        </expand_row>
    </container>
</hero>

<style>
    @import "./shared.css";
    hero {
        width: 100%;
        height: 500px;
        font-size: 36px;
        background-color: var(--color-bg-2);
        display: block;
    }

    heading {
        color: white;
        background-color: var(--color-theme-1);
        padding: 40px;
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

    button:hover{
        background-color: #ff3f8f;
    }
</style>
