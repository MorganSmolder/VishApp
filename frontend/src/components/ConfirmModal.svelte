<script lang="ts">
    
    import { createEventDispatcher } from "svelte";
    import Modal from "./Modal.svelte"

    export let active = true;

    export let textContent : string;

    const dispatch = createEventDispatcher();
    
    function NotifySubmit(yes : boolean) {
        dispatch("submit", {
            "yes":yes
        });
    }
</script>
<Modal isVisible={active}>
    <div>
        <column>
            <h2>{textContent}</h2>
            <expand_row style="max-width: 200px;">
                <button on:click={() => NotifySubmit(true)}>Confirm</button>
                <button on:click={() => NotifySubmit(false)}>Cancel</button>
            </expand_row>
        </column>
    </div>
</Modal>
<style>
    div{
        padding: 20px;
    }
</style>