<script lang="ts">
    import { onMount } from "svelte";

    export let isVisible : Boolean = false;
</script>

{#if isVisible}
<modal_parent>
    <column>
        <modal>
            <slot />
        </modal>
    </column>
</modal_parent>
{/if}

<style>
    @import "../shared.css";

    modal_parent {
        position: fixed;
        z-index: 1;
        display: block;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        top: 0;
        left: 0;
    }

    modal {
        border-radius: 15px;
        background-color: white;
        display: block;
        width: 400px;
        padding: 40px;
    }

    column {
        height: 100%;
        text-align: center;
    }
</style>
